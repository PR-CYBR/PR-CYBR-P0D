# PR-CYBR-P0D Retrofit Automation System

## Overview

The Retrofit Automation System extends PR-CYBR-P0D's capabilities to provide a complete podcast production pipeline that automates:

- Episode metadata prepopulation
- Systematic code name generation
- Release schedule calculation
- Google Docs integration
- NotebookLM audio generation
- Automatic show notes creation
- Campaign task scheduling

## Architecture

```
┌─────────────────┐
│     Notion      │ ← Central metadata hub
│   (pr-cyberpod) │
└────────┬────────┘
         │ Bidirectional Sync
         ↓
┌─────────────────┐      ┌──────────────────┐
│  GitHub Actions │ ───→ │  Google Drive    │
│  (Workflows)    │      │  (Docs & Audio)  │
└────────┬────────┘      └──────────────────┘
         │                        │
         ↓                        ↓
┌─────────────────┐      ┌──────────────────┐
│    Episodes     │      │   NotebookLM     │
│   Repository    │      │  (Audio Gen)     │
└─────────────────┘      └──────────────────┘
```

## Workflow Components

### 1. Release Schedule Generation

**Script:** `scripts/populate_release_schedule.py`

Generates a complete release schedule for all episodes across all seasons:

- **Pattern:** Monday, Wednesday, Friday at 06:00 UTC
- **Output:** `episodes/release-schedule.txt`
- **Scope:** 17 seasons × 52 episodes = 884 total episodes

**Usage:**
```bash
python scripts/populate_release_schedule.py
```

### 2. Code Name Generation

**Script:** `scripts/generate_code_names.py`

Creates systematic, thematic code names for episodes:

- **Format:** `P0D-S<season>-E<episode>-AXIS-<symbol>`
- **Example:** `P0D-S01-E001-AXIS-CIPHER`
- **Output:** `episodes/episode-code-names.json` and `.txt`

**Symbol Categories:**
- Encryption (AES, RSA, TLS, etc.)
- Security (FIREWALL, SHIELD, GUARD, etc.)
- Attack (BREACH, EXPLOIT, PAYLOAD, etc.)
- Network (PACKET, ROUTER, GATEWAY, etc.)
- Data (STREAM, BUFFER, CACHE, etc.)
- Protocol (HTTP, TCP, UDP, etc.)
- Operation (SCAN, PROBE, TRACE, etc.)
- Status (ACTIVE, IDLE, READY, etc.)

**Usage:**
```bash
python scripts/generate_code_names.py
```

### 3. Enhanced Notion Sync

**Script:** `scripts/sync_notion_enhanced.py`

Extends the original sync with bidirectional capabilities:

**New Notion Fields:**
- `Prompt-Input` (Text) - AI directive for content generation
- `Script-Doc-Link` (URL) - Google Doc with episode script
- `Track-Cloud` (URL) - NotebookLM-generated audio file
- `Show-Notes-Link` (URL) - Google Doc with show notes
- `Code-Name` (Text) - Systematic episode identifier
- `Status` (Select) - Episode production status

**Automation Flow:**

1. **Prompt Processing**
   - Read from `Prompt-Input` field or local file
   - Create Google Doc with script template
   - Update `Script-Doc-Link` in Notion

2. **NotebookLM Integration**
   - Add script document to NotebookLM
   - Generate Audio Overview (podcast episode)
   - Upload audio to Google Drive
   - Update `Track-Cloud` in Notion

3. **Metadata Extraction**
   - Extract duration from audio file
   - Update `Duration` in Notion

4. **Show Notes Generation**
   - Generate show notes from template
   - Create Google Doc
   - Update `Show-Notes-Link` in Notion

### 4. GitHub Actions Workflows

#### retrofit-episodes.yml

**Triggers:**
- **Manual:** `workflow_dispatch` for on-demand execution
- **Scheduled:** Daily at 2 AM UTC
- **Callable:** Can be triggered by other workflows

**Features:**
- Dry run mode for testing
- Season-specific filtering
- Automatic commit and push
- Detailed execution summary

**Manual Execution:**
```bash
# Via GitHub UI:
# Actions → Retrofit Episodes → Run workflow

# With parameters:
# - Season: (optional, e.g., "1")
# - Dry Run: true/false
```

## Configuration

### Required Secrets

Configure in GitHub Settings → Secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `NOTION_TOKEN` | Notion integration token | `secret_...` |
| `NOTION_DATABASE_ID` | pr-cyberpod database ID | `32-char hex` |
| `PR_CYBR_P0D_S1_DB_ID` | Season 1 database ID | (per season) |
| `PR_CYBR_P0D_S2_DB_ID` | Season 2 database ID | (per season) |
| ... | (up to S17) | |
| `GOOGLE_DRIVE_SERVICE_ACCOUNT` | Service account JSON | `{...}` |
| `NOTEBOOK_LM_API_KEY` | NotebookLM API key | `key_...` |
| `PR_CYBR_P0D_DRIVE_FOLDER_ID` | Drive folder ID | `folder_...` |

### Environment Setup

```bash
# Local development
export NOTION_TOKEN="secret_..."
export NOTION_DATABASE_ID="..."
export GOOGLE_DRIVE_SERVICE_ACCOUNT='{"type": "service_account", ...}'
export NOTEBOOK_LM_API_KEY="key_..."
export PR_CYBR_P0D_DRIVE_FOLDER_ID="folder_..."
```

## Usage Examples

### Backfill Existing Episodes

```bash
# Generate schedules and code names
python scripts/populate_release_schedule.py
python scripts/generate_code_names.py

# Run retrofit automation
python scripts/sync_notion_enhanced.py
```

### Process New Episode

1. **In Notion:**
   - Create new episode entry
   - Set `Status` = "Not started"
   - Fill in `Title`, `Season`, `Episode`
   - Optionally add `Prompt-Input` (5,000 chars max)

2. **Automatic Processing:**
   - Workflow runs nightly at 2 AM UTC
   - Detects new episodes with "Not started" status
   - Processes through automation pipeline
   - Updates Notion fields with generated assets

3. **Manual Trigger:**
   - Go to Actions → Retrofit Episodes
   - Click "Run workflow"
   - Select options and run

### Add Custom Prompt

```bash
# Create prompt file
mkdir -p episodes/prompts
cat > episodes/prompts/prompt_S01E001.txt << 'EOF'
Create a comprehensive introduction to cybersecurity fundamentals...
(up to 5,000 characters)
EOF

# Run enhanced sync
python scripts/sync_notion_enhanced.py
```

## Template System

Templates are stored in `retrofitting/templates/`:

- **script-template.md** - Episode script structure
- **show-notes-template.md** - Show notes format
- **README.md** - Template documentation

### Template Variables

Templates support automatic variable substitution:

```markdown
{{EPISODE_TITLE}}   - Episode title
{{CODE_NAME}}       - Episode code name
{{SEASON}}          - Season number
{{EPISODE}}         - Episode number
{{RELEASE_DATE}}    - Scheduled release date
{{DESCRIPTION}}     - Episode description
{{DURATION}}        - Episode duration
{{PROMPT}}          - Original prompt input
```

## Integration Points

### Google Drive API

**Authentication:** Service Account JSON

**Operations:**
- Create Google Docs from templates
- Upload audio files
- Manage folder structure
- Generate shareable links

**Folder Structure:**
```
PR-CYBR-P0D/
├── Season-01/
│   ├── S01E001-script.gdoc
│   ├── S01E001-audio.mp3
│   └── S01E001-shownotes.gdoc
├── Season-02/
│   └── ...
└── ...
```

### NotebookLM API

**Authentication:** API Key

**Operations:**
- Create/manage notebooks (one per season)
- Add documents as sources
- Trigger Audio Overview generation
- Retrieve generated audio files

**Notebook Naming:** `PR-CYBR-P0D-Season-##`

### Notion API

**Authentication:** Integration Token

**Operations:**
- Query episodes by status
- Update episode properties
- Read prompt inputs
- Write generated links

## Troubleshooting

### Common Issues

**Issue:** Episodes not processing

**Solutions:**
- Verify `Status` field is set to "Not started"
- Check secrets are configured correctly
- Review workflow logs in Actions tab
- Ensure Notion integration has database access

**Issue:** Google Drive authentication failed

**Solutions:**
- Verify service account JSON is valid
- Check service account has Drive API enabled
- Ensure folder ID is correct and accessible
- Review IAM permissions

**Issue:** NotebookLM audio generation fails

**Solutions:**
- Verify API key is valid and active
- Check notebook exists for the season
- Ensure source document is accessible
- Review NotebookLM API limits

**Issue:** Templates not rendering correctly

**Solutions:**
- Check template file exists in `retrofitting/templates/`
- Verify template variable names match exactly
- Ensure template encoding is UTF-8
- Review template syntax for errors

## Development

### Adding New Features

1. **Add Notion Field:**
   - Update database schema in Notion
   - Add property parsing in `sync_notion_enhanced.py`
   - Update documentation

2. **Add Template:**
   - Create `.md` file in `retrofitting/templates/`
   - Define variables in template
   - Add processing logic in scripts
   - Document in template README

3. **Add Automation Step:**
   - Implement function in `sync_notion_enhanced.py`
   - Add to `retrofit_episode()` method
   - Update workflow if needed
   - Add tests and documentation

### Testing

```bash
# Test schedule generation
python scripts/populate_release_schedule.py
cat episodes/release-schedule.txt

# Test code name generation
python scripts/generate_code_names.py
cat episodes/episode-code-names.txt

# Test enhanced sync (requires credentials)
export NOTION_TOKEN="test_token"
export NOTION_DATABASE_ID="test_db"
python scripts/sync_notion_enhanced.py
```

## Best Practices

1. **Prompt Writing:**
   - Keep prompts under 5,000 characters
   - Be specific about topic and structure
   - Include key points to cover
   - Specify tone and style

2. **Template Customization:**
   - Maintain consistent variable naming
   - Test with sample data before deploying
   - Keep templates version-controlled
   - Document custom variables

3. **Workflow Execution:**
   - Use dry run mode for testing
   - Process one season at a time initially
   - Monitor execution logs
   - Verify Notion updates after each run

4. **Security:**
   - Never commit secrets to repository
   - Rotate API keys regularly
   - Use read-only tokens where possible
   - Review service account permissions

## Future Enhancements

- [ ] RSS feed generation from episode metadata
- [ ] Automated social media post creation
- [ ] Analytics and download tracking
- [ ] Multi-language support
- [ ] Custom audio processing options
- [ ] Enhanced show notes with AI assistance
- [ ] Integration with podcast hosting platforms

## Support

For issues or questions:

1. Check this documentation
2. Review workflow logs in Actions
3. Check [GitHub Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
4. Open a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Relevant logs and error messages
   - Environment details

---

**Last Updated:** 2024-01-01  
**Version:** 1.0.0
