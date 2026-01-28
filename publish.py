#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gmeek Publisher
A simple script to publish local Markdown files to GitHub Issues for Gmeek blogs.

Usage:
    python gmeek_pub.py <path_to_markdown_file>

Requirements:
    - Python 3.6+
    - GITHUB_TOKEN environment variable set
"""

import os
import sys
import re
import json
import subprocess
import urllib.request
import urllib.error

def get_git_remote_url():
    """
    Tries to retrieve the git remote origin URL from the current directory.
    """
    try:
        # Run git config --get remote.origin.url
        process = subprocess.Popen(['git', 'config', '--get', 'remote.origin.url'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        if process.returncode == 0:
            url = stdout.decode('utf-8').strip()
            # Extract owner/repo
            # Supports:
            # https://github.com/owner/repo.git
            # git@github.com:owner/repo.git
            # https://github.com/owner/repo
            match = re.search(r'github\.com[:/]([^/]+)/([^\s]+)', url)
            if match:
                owner = match.group(1)
                repo = match.group(2)
                if repo.endswith('.git'):
                    repo = repo[:-4]
                return f"{owner}/{repo}"
    except Exception as e:
        print(f"Warning: Failed to detect git remote: {e}")
    return None

def parse_front_matter(content):
    """
    Parses YAML-like front matter from the beginning of the file.
    """
    front_matter = {}
    body = content
    if content.startswith('---'):
        parts = re.split(r'^---$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2].strip()
            for line in raw_fm.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'): continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # Basic list parsing [a, b]
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip().strip("'").strip('"') for v in value[1:-1].split(',') if v.strip()]
                    front_matter[key] = value
    return front_matter, body

def github_api_request(endpoint, method='GET', data=None, token=None):
    """
    Makes a request to the GitHub API.
    """
    url = f"https://api.github.com/repos/{endpoint}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Gmeek-Publisher-CLI'
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"\nGitHub API Error: {e.code} {e.reason}")
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            print(f"Message: {error_json.get('message')}")
        except:
            print(f"Response: {error_body}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python gmeek_pub.py <filepath>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)
        
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        print("Please export GITHUB_TOKEN=your_token_here")
        print("You can generate one at https://github.com/settings/tokens with 'repo' scope.")
        sys.exit(1)
        
    repo = get_git_remote_url()
    if not repo:
        print("Could not detect repository from git config.")
        print("Please make sure you are running this script inside a git repository linked to GitHub.")
        repo_input = input("Or enter repository manually (owner/repo): ").strip()
        if not repo_input:
            sys.exit(1)
        repo = repo_input
    
    print(f"Target Repository: {repo}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    fm, body = parse_front_matter(content)
    
    title = fm.get('title')
    if not title:
        print("Error: 'title' missing in front matter.")
        sys.exit(1)
        
    labels = fm.get('labels', [])
    if isinstance(labels, str):
        # Handle comma-separated string if user didn't use []
        labels = [l.strip() for l in labels.split(',')]
        
    issue_number = fm.get('issue_number')
    
    payload = {
        'title': title,
        'body': body,
        'labels': labels
    }
    
    if issue_number:
        print(f"Updating Issue #{issue_number}...")
        try:
            response = github_api_request(f"{repo}/issues/{issue_number}", method='PATCH', data=payload, token=token)
            print(f"✅ Successfully updated: {response['html_url']}")
        except Exception:
            print("Failed to update. Please check if the issue exists and you have permission.")
            sys.exit(1)
    else:
        print(f"Creating New Issue...")
        response = github_api_request(f"{repo}/issues", method='POST', data=payload, token=token)
        new_issue_number = response['number']
        print(f"✅ Successfully created: {response['html_url']}")
        
        # Append issue_number to front matter in the file
        # We assume standard YAML format we parsed
        lines = content.split('\n')
        # Find the end of front matter
        fm_end_idx = -1
        if lines[0].strip() == '---':
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    fm_end_idx = i
                    break
        
        if fm_end_idx > 0:
            lines.insert(fm_end_idx, f"issue_number: {new_issue_number}")
            new_content = "\n".join(lines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"📝 Local file updated with issue_number: {new_issue_number}")
        else:
            print("Warning: Could not update local file with issue_number (Front matter format issue).")

if __name__ == "__main__":
    main()
