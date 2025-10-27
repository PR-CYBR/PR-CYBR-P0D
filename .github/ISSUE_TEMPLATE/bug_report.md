---
name: Bug Report
about: Report a bug or issue with PR-CYBR-P0D
title: '[BUG] '
labels: bug, needs-triage
assignees: ''

---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Run command '....'
3. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Error Messages

```
Paste any error messages or logs here
```

## Environment

- **Branch**: (e.g., main, dev, feat/episode-schema)
- **Python Version**: (run `python --version`)
- **OS**: (e.g., Ubuntu 22.04, macOS 14, Windows 11)
- **GitHub Actions**: (if applicable, link to failed workflow run)

## Configuration

**Which components are involved?** (check all that apply)
- [ ] Notion sync
- [ ] Episode management
- [ ] Transcription (Whisper)
- [ ] Show notes generation
- [ ] RSS feed generation
- [ ] Archive.org upload
- [ ] GitHub Actions workflows
- [ ] n8n integration
- [ ] Other (specify below)

**Secrets configured?** (don't share actual values!)
- [ ] NOTION_TOKEN
- [ ] NOTION_EPISODES_DB_ID
- [ ] ARCHIVE_ACCESS_KEY
- [ ] ARCHIVE_SECRET_KEY
- [ ] OPENAI_API_KEY (optional)
- [ ] Other (specify)

## Screenshots

If applicable, add screenshots to help explain your problem.

## Additional Context

Add any other context about the problem here.

## Possible Solution

(Optional) If you have ideas on how to fix the issue, share them here.

---

**Before submitting:**
- [ ] I've searched existing issues to avoid duplicates
- [ ] I've included all relevant information above
- [ ] I've removed any sensitive information (API keys, tokens, etc.)
- [ ] I've checked the [troubleshooting guide](../SETUP.md#troubleshooting)
