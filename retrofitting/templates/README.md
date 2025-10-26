# Retrofitting Templates

This directory contains templates for automated document generation in the PR-CYBR-P0D retrofit automation system.

## Template Files

### Google Docs Templates

1. **script-template.md** - Template for episode script documents
2. **show-notes-template.md** - Template for episode show notes
3. **campaign-template.md** - Template for pre/post-launch campaign tasks

## How Templates Are Used

Templates are used by the retrofit automation system when:

1. **Prompt Input Processing**: When a prompt is uploaded to Notion, the system creates a Google Doc using the script template
2. **Show Notes Generation**: After audio is generated, show notes are created from the template
3. **Campaign Planning**: Pre-launch and post-launch tasks are generated from campaign template

## Template Variables

Templates support the following variables that are automatically replaced:

- `{{EPISODE_TITLE}}` - Episode title from Notion
- `{{CODE_NAME}}` - Systematic episode code name (e.g., P0D-S01-E001-AXIS-CIPHER)
- `{{SEASON}}` - Season number
- `{{EPISODE}}` - Episode number
- `{{RELEASE_DATE}}` - Scheduled release date
- `{{DESCRIPTION}}` - Episode description
- `{{DURATION}}` - Episode duration
- `{{PROMPT}}` - Original prompt input

## Creating Custom Templates

To create a custom template:

1. Create a new markdown file in this directory
2. Use `{{VARIABLE}}` syntax for dynamic content
3. Update the automation scripts to reference your new template
4. Test with a sample episode to verify variable substitution

## Integration with Google Drive

Templates are converted to Google Docs format when uploaded to Drive. Markdown formatting is preserved where possible:

- Headers (`#`) → Google Docs heading styles
- Bold (`**text**`) → Bold formatting
- Lists (`-` or `1.`) → Bullet/numbered lists
- Links (`[text](url)`) → Hyperlinks

## Maintenance

Templates should be reviewed and updated:

- When episode format changes
- When new metadata fields are added
- When NotebookLM integration requirements change
- Based on feedback from content creators
