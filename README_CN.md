# Gmeek 发布技能 (Gmeek Publish Skill)

[English Documentation](README.md) | [中文文档](README_CN.md)

本仓库包含一个 **Trae Skill (技能)**，用于自动化将 Markdown 文件发布到基于 Gmeek 框架的 GitHub 博客。

## ✨ 为什么使用此技能？

*   **一键发布**: 告别繁琐的 GitHub 网页操作。只需对 AI 说“发布这篇文章”，即可自动完成。
*   **自动更新**: 智能识别文章是否已发布，自动**更新现有 Issue** 而非重复创建，避免版本混乱。
*   **标签管理**: 支持在 Front Matter 中直接定义标签（如 `labels: [技术, 生活]`），自动同步到 GitHub Issue。
*   **零依赖**: 核心脚本仅使用 Python 标准库，无需 `pip install` 任何第三方包，轻量纯净。


## 📂 仓库内容

*   `SKILL.md`: Trae Skill 的定义文件。
*   `publish.py`: 处理创建/更新 GitHub Issues 逻辑的 Python 脚本。

## 🚀 如何使用此技能

### 前置条件

1.  **GitHub Token**: 你需要一个 GitHub Personal Access Token (Classic)，并勾选 `repo` (或 public_repo) 权限。
2.  **环境变量**: 你必须在终端或 IDE 环境中将此 Token 导出为 `GITHUB_TOKEN` 环境变量。
3.  **Python 3**: 确保已安装 Python 3。

### 安装方法

要在你的 Trae IDE 中手动安装此技能：

1.  在你的工作区中创建一个目录：`.trae/skills/Gmeek_Publish/`。
2.  将本仓库中的 `SKILL.md` 和 `publish.py` 复制到该目录下。

### 使用说明

安装完成后，你只需直接告诉 AI：

> "帮我发布 `_posts/my-article.md` 这个文件"

AI 就会自动调用此技能来运行脚本并返回结果。

## ⚠️ 重要提示

此技能需要你 GitHub 仓库的 **写入权限** (通过 Token)。请务必保管好你的 Token，不要将其提交到版本控制系统中。
