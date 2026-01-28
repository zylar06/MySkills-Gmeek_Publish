# Gmeek Publish Skill

[中文文档](README_CN.md) | [English Documentation](README.md)

This repository contains a **Trae Skill** that automates publishing Markdown files to a Gmeek-based GitHub blog.

## ✨ Why use this Skill?

*   **One-Click Publishing**: No need to manually create Issues on GitHub. Just say "Publish this file" to the AI.
*   **Automatic Updates**: Intelligently detects if an article has been published and automatically **updates the existing Issue** instead of creating a duplicate.
*   **Label Management**: Supports defining labels directly in Front Matter (e.g., `labels: [Tech, Life]`), which are automatically synchronized to GitHub.
*   **Zero Dependencies**: The core script uses only Python standard libraries, requiring no additional `pip install`.


## 📂 Repository Contents

*   `SKILL.md`: The definition file for the Trae Skill.
*   `publish.py`: The Python script that handles the logic of creating/updating GitHub Issues.

## 🚀 How to Use this Skill

### Prerequisites

1.  **GitHub Token**: You need a GitHub Personal Access Token (Classic) with `repo` (public_repo) permissions.
2.  **Environment Variable**: You must export this token as `GITHUB_TOKEN` in your terminal or IDE environment.
3.  **Python 3**: Ensure Python 3 is installed.

### Installation

To install this skill in your Trae IDE manually:

1.  Create a directory: `.trae/skills/Gmeek_Publish/` in your workspace.
2.  Copy `SKILL.md` and `publish.py` from this repository into that directory.

### Usage

Once installed, you can simply ask the AI:

> "Publish the file `_posts/my-article.md`"

The AI will use this skill to run the script and return the result.

## ⚠️ Important Note

This skill requires **write access** to your GitHub repository (via the Token). Please ensure you keep your Token secure and do not commit it to version control.
