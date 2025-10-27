# Quick Start - Configuration Reference

This is a quick reference for configuring PR-CYBR-P0D, including the new Retrofit Automation System.

## Required GitHub Secrets

### Notion Integration

| Secret Name | Description | Where to Get It |
|-------------|-------------|-----------------|
| `NOTION_TOKEN` | Notion API integration token | [Create at notion.so/my-integrations](https://www.notion.so/my-integrations) |
| `NOTION_DATABASE_ID` | Database ID for pr-cyberpod | From your database URL (32-character hex string) |
| `PR_CYBR_P0D_S1_DB_ID` - `PR_CYBR_P0D_S17_DB_ID` | Per-season database IDs (optional) | Individual season database URLs |

### Google Workspace Integration (NEW)

| Secret Name | Description | Where to Get It |
|-------------|-------------|-----------------|
| `GOOGLE_DRIVE_SERVICE_ACCOUNT` | Service account JSON | [Google Cloud Console](https://console.cloud.google.com) |
| `PR_CYBR_P0D_DRIVE_FOLDER_ID` | Drive folder ID | From folder URL after `/folders/` |

### NotebookLM Integration (NEW)

| Secret Name | Description | Where to Get It |
|-------------|-------------|-----------------|
| `NOTEBOOK_LM_API_KEY` | NotebookLM API key | NotebookLM API console |

## Required Notion Database Properties

### Basic Properties

| Property Name | Type | Required | Example |
|---------------|------|----------|---------|
| Title | Title | ✅ Yes | "Episode 1: Introduction" |
| Episode Live | Checkbox | ✅ Yes | ☑️ |
| Release Date | Date | ✅ Yes | 2024-01-15 |
| File URL | URL | ✅ Yes | https://example.com/ep1.mp3 |
| Episode Number | Number | ❌ No | 1 |
| Description | Text | ❌ No | "In this episode..." |

### Retrofit Automation Properties (NEW)

| Property Name | Type | Required | Example |
|---------------|------|----------|---------|
| Season | Number | ✅ Yes | 1 |
| Episode | Number | ✅ Yes | 1 |
| Status | Select | ✅ Yes | "Not started" / "In progress" / "Complete" |
| Code-Name | Text | ❌ No | "P0D-S01-E001-AXIS-CIPHER" |
| Prompt-Input | Text | ❌ No | "Create an episode about..." (max 5,000 chars) |
| Script-Doc-Link | URL | ❌ No | https://docs.google.com/... |
| Track-Cloud | URL | ❌ No | https://drive.google.com/... |
| Duration | Text | ❌ No | "45:30" |
| Show-Notes-Link | URL | ❌ No | https://docs.google.com/... |

## Workflow Triggers

### Episode Sync (Original)

#### Automatic (Scheduled)
- **When**: Daily at midnight UTC
- **Trigger**: Cron schedule in workflow
- **Action**: Syncs all live episodes

#### Manual (On-Demand)
- **Where**: Actions → "Sync Notion Episodes" → Run workflow
- **When**: Anytime you want to sync immediately
- **Action**: Same as scheduled sync

#### Webhook (Setup Required)
- **When**: Notion database changes
- **Trigger**: `repository_dispatch` event with type `notion-webhook`
- **Status**: Workflow ready, Notion webhook endpoint setup required
- **Action**: Real-time sync on database updates

### Retrofit Automation (NEW)

#### Automatic (Scheduled)
- **When**: Daily at 2 AM UTC
- **Trigger**: Cron schedule in workflow
- **Action**: Process episodes with Status = "Not started"

#### Manual (On-Demand)
- **Where**: Actions → "Retrofit Episodes" → Run workflow
- **Options**:
  - Season filter (optional)
  - Dry run mode (no changes to Notion)
- **Action**: Full retrofit automation pipeline

#### Workflow Call
- **When**: Triggered by other workflows
- **Use**: Integration with other automation systems

## File Naming Pattern

### Episode Files (Original)
```
episode-{NUM}-{slug}.mp3
episode-{NUM}-{slug}-metadata.json
```

Examples:
- `episode-001-introduction.mp3`
- `episode-042-security-basics.mp3`
- `episode-a1b2c3d4-episode-title.mp3` (no episode number, hash from title)

### Episode Code Names (NEW)
```
P0D-S<season>-E<episode>-AXIS-<symbol>
```

Examples:
- `P0D-S01-E001-AXIS-CIPHER`
- `P0D-S02-E015-AXIS-FIREWALL`
- `P0D-S17-E052-AXIS-SENTINEL`

### Prompt Files (NEW)
```
episodes/prompts/prompt_S<season>E<episode>.txt
```

Examples:
- `episodes/prompts/prompt_S01E001.txt`
- `episodes/prompts/prompt_S02E015.txt`

## First-Time Setup Checklist

### Basic Setup
- [ ] Create Notion database named "pr-cyberpod"
- [ ] Add required basic properties to database
- [ ] Create Notion integration
- [ ] Connect integration to database
- [ ] Copy integration token
- [ ] Get database ID from URL
- [ ] Add Notion secrets to GitHub repository
- [ ] Run "Create Branch Structure" workflow
- [ ] Add test episode to Notion
- [ ] Check "Episode Live" checkbox
- [ ] Run "Sync Notion Episodes" workflow
- [ ] Verify episode appears in `/episodes/`

### Retrofit Setup (NEW)
- [ ] Add retrofit properties to Notion database
- [ ] Create Google Cloud project
- [ ] Enable Drive API and Docs API
- [ ] Create service account and download JSON
- [ ] Add Google Drive secrets to GitHub
- [ ] Create Drive folder for episodes
- [ ] Get NotebookLM API access
- [ ] Add NotebookLM secret to GitHub
- [ ] Generate release schedule: `python scripts/populate_release_schedule.py`
- [ ] Generate code names: `python scripts/generate_code_names.py`
- [ ] Test retrofit with dry run mode
- [ ] Create first episode with prompt
- [ ] Run retrofit workflow
- [ ] Verify Google Docs and audio created
- [ ] Check Notion fields updated

## Common Issues

| Problem | Solution |
|---------|----------|
| Episodes not syncing | Check "Episode Live" is checked |
| Authentication error | Verify `NOTION_TOKEN` is correct |
| Database not found | Verify `NOTION_DATABASE_ID` is correct |
| Download fails | Check File URL is publicly accessible |
| Missing metadata | Ensure all required properties exist |
| **Retrofit not processing** | **Check Status = "Not started"** |
| **Google Drive error** | **Verify service account JSON is valid** |
| **NotebookLM fails** | **Check API key and rate limits** |
| **Prompts not loading** | **Check file path and character limit** |
| **Duration not extracted** | **Verify audio file format (MP3)** |

## Quick Commands

### Generate Schedules and Names
```bash
# Generate release schedule (Mon/Wed/Fri 06:00 UTC)
python scripts/populate_release_schedule.py

# Generate episode code names
python scripts/generate_code_names.py
```

### Run Syncs Locally
```bash
# Basic episode sync
export NOTION_TOKEN="secret_..."
export NOTION_DATABASE_ID="..."
python scripts/sync_notion.py

# Enhanced retrofit sync
export GOOGLE_DRIVE_SERVICE_ACCOUNT='{"type":"service_account",...}'
export NOTEBOOK_LM_API_KEY="key_..."
python scripts/sync_notion_enhanced.py
```

### Test Workflows
```bash
# Via GitHub Actions UI
# 1. Go to Actions tab
# 2. Select workflow
# 3. Click "Run workflow"
# 4. Enable dry run mode for testing
```

## Quick Links

- [Full Setup Guide](SETUP.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Branching Strategy](BRANCHING.md)
- [Episodes Directory](episodes/README.md)
- **[Retrofit Guide](retrofitting/docs/RETROFIT_GUIDE.md)** ⭐ NEW
- **[Template Documentation](retrofitting/templates/README.md)** ⭐ NEW

## Key Features Quick Reference

### Basic Sync
- ✅ Automated episode download from Notion
- ✅ Daily scheduled sync at midnight UTC
- ✅ Manual trigger via GitHub Actions
- ✅ Metadata tracking in JSON files

### Retrofit Automation (NEW)
- ✅ AI-powered content generation (5,000-char prompts)
- ✅ Automated Google Docs creation
- ✅ NotebookLM audio generation
- ✅ Systematic episode naming (P0D-S##-E###-AXIS-SYMBOL)
- ✅ Release schedule calculation (Mon/Wed/Fri 06:00 UTC)
- ✅ Bidirectional GitHub ↔ Notion sync
- ✅ Automatic show notes generation
- ✅ Duration extraction from audio
- ✅ Campaign task scheduling

## Support

- **Issues**: [GitHub Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
- **Logs**: [GitHub Actions](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
- **Docs**: [Main README](README.md)
