---
name: "Gmeek_Publish"
description: "Publishes local Markdown files to a Gmeek-based GitHub blog. Invoke when the user wants to publish, update, or upload a post/article."
---

# Gmeek Publisher Skill

This skill allows you to publish a local Markdown file to a GitHub repository that uses the Gmeek framework.

## Usage

When the user asks to publish a file, execute the `publish.py` script located in this skill's directory.

### Command

```bash
python3 .trae/skills/Gmeek_Publish/publish.py <path_to_markdown_file>
```

### Prerequisites

*   **Environment Variable**: `GITHUB_TOKEN` must be set in the current terminal session.
*   **Git Repository**: The script tries to detect the git remote. If run outside a git repo, it may ask for input or fail.
*   **File Format**: The Markdown file must have Front Matter with at least a `title`.

### Example

User: "Publish the file `_posts/hello.md`"
Action:
1. Check if `GITHUB_TOKEN` is set.
2. Run: `python3 .trae/skills/Gmeek_Publish/publish.py _posts/hello.md`
