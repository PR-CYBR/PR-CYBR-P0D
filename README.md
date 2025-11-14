# PR-CYBR-P0D

[![Sync Notion Episodes](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml)
[![Retrofit Episodes](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/retrofit-episodes.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/retrofit-episodes.yml)
[![Verify Environment](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/verify-env-vars.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/verify-env-vars.yml)

The Official PR-CYBR Podcast Repository - Autonomous podcast production system with event-driven workflows, self-hosted RSS, and pluggable distribution.

## Overview

PR-CYBR-P0D is an **autonomous podcast architecture** that orchestrates the complete episode lifecycle from planning to distribution:

1. **Event-driven automation** via n8n workflows and GitHub Actions
2. **Self-hosted RSS** with pluggable storage (Archive.org, Spotify, custom)
3. **AI-powered content** generation using NotebookLM Audio Overviews
4. **Complete replication** - fork and launch in ≤10 minutes

## Architecture

```
Notion Database (Source of Truth)
  ↓ (Status: Not started → In progress → Complete → Live)
n8n Orchestration
  ↓ (Webhooks trigger workflows)
GitHub Actions (Automation)
  ├─ Pre-Campaign: Transcription + Show Notes
  ├─ Go Live: Archive.org Upload + RSS Generation
  └─ Post-Campaign: Recap Generation + Archival
  ↓
Self-Hosted RSS Feed (GitHub Pages)
  └─ Distribution to Apple Podcasts, Spotify, etc.
```

**Key Principles:**
- 🎯 **Notion as orchestration source of truth** - Status flags drive workflows
- 🤖 **n8n for event triggers** - Button clicks and status changes trigger automation
- 📦 **GitHub for content & CI/CD** - Scripts, metadata, transcripts, RSS, docs
- 📡 **Self-hosted distribution** - Free/low-cost RSS + Archive.org (or pluggable adapters)
- 🎓 **NotebookLM for education** - Per-season interactive course notebooks
- 🔄 **Template-ready replication** - Complete fork-and-launch setup

### Production Workflows

**Pre-Campaign (Notion → n8n → GitHub Actions)**
- Trigger: Status changes to "In progress" or button click
- Actions: Transcribe audio (Whisper), generate show notes, commit artifacts
- Output: `transcript.txt`, `shownotes.md` in episode folder

**Go Live (Scheduled or n8n trigger)**
- Trigger: Release date reached or manual publish
- Actions: Upload to Archive.org, generate/update RSS feed, mark as published
- Output: Public RSS feed at `https://pr-cybr.github.io/PR-CYBR-P0D/podcast.xml`

**Post-Campaign (X days after publish)**
- Trigger: Scheduled or manual
- Actions: Generate recap article, create Q&A flashcards, archive episode
- Output: `recap.md` with key takeaways and citations

### Storage & Distribution

**Default Architecture:**
- **Storage**: Internet Archive (free, permanent, S3-compatible)
- **RSS**: Self-hosted via GitHub Pages
- **CDN**: Archive.org's global distribution network

**Pluggable Adapters:**
```python
STORAGE_ADAPTER = "archive"  # or "spotify", "custom"
```
- **archive**: Internet Archive (free, default)
- **spotify**: Spotify for Podcasters (optional)
- **custom**: Your own S3/CDN endpoint

See [Storage & Distribution Docs](docs/storage-distribution.md) for details.

## Key Features

### Core Automation
- 🎙️ **Automated Episode Sync**: Episodes marked as live in Notion are automatically downloaded and committed
- 📅 **Scheduled Updates**: Daily synchronization checks for new episodes
- 🔄 **Manual Trigger**: On-demand sync via GitHub Actions workflow_dispatch
- 📊 **Metadata Tracking**: Each episode includes JSON metadata with title, release date, and description

### Retrofit Automation System (NEW)
- 🤖 **AI Content Generation**: 5,000-character prompts drive NotebookLM audio creation
- 📝 **Automated Documentation**: Google Docs for scripts and show notes
- 🏷️ **Systematic Naming**: Thematic code names (P0D-S##-E###-AXIS-SYMBOL)
- 📆 **Release Scheduling**: Auto-calculated Mon/Wed/Fri 06:00 UTC pattern
- ☁️ **Cloud Integration**: Seamless Google Drive and NotebookLM workflow
- 🔁 **Bidirectional Sync**: GitHub ↔ Notion metadata synchronization

### Infrastructure
- 🌳 **Full Branch Structure**: Maintains the complete spec-bootstrap branching strategy for proper CI/CD
- 🔐 **Secure Integration**: Uses GitHub Secrets for all API credentials
- 📈 **Scalable Design**: Handles 17 seasons × 52 episodes = 884 total episodes

## Live Codebase Mindmap

Auto-generated on each push: **repo-map.html** (via GitHub Pages and CI artifact).
When Pages is enabled, it will be served at: `https://PR-CYBR.github.io/PR-CYBR-P0D/repo-map.html`

## Forking This Repository

Want to create your own podcast automation pipeline? You can fork this repository and customize it for your needs!

### Why Fork This Repo?

This repository provides a complete, production-ready podcast automation system that:
- Syncs episodes from Notion to GitHub automatically
- Generates AI-powered content using NotebookLM
- Manages metadata across multiple platforms
- Automates the entire production pipeline from prompt to published episode

### Quick Start for Forks

1. **Fork the Repository**
   - Click the "Fork" button at the top of this page
   - Choose your GitHub account or organization
   - Optionally rename the repository for your podcast

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-FORK-NAME.git
   cd YOUR-FORK-NAME
   ```

3. **Follow the Setup Instructions**
   - See the [Setup](#setup) section below for detailed configuration
   - Configure your own Notion database
   - Add your API keys as GitHub Secrets
   - Customize the workflows for your needs

### Customization Guide

#### For Basic Episode Sync Only

If you only need basic episode syncing without the full retrofit automation:

1. **Remove Retrofit Components** (optional):
   - Delete or disable `.github/workflows/retrofit-episodes.yml`
   - Remove `retrofitting/` directory if not needed
   - Remove Google Drive and NotebookLM integration code from scripts

2. **Configure Your Notion Database**:
   - Create a Notion database with the basic properties (see [Prerequisites](#prerequisites))
   - You only need: Title, Episode Live, Release Date, File URL, Episode Number, Description

3. **Set Required Secrets**:
   - Only `NOTION_TOKEN` and `NOTION_DATABASE_ID` are required
   - Skip Google Drive and NotebookLM secrets

#### For Full Automation Pipeline

If you want the complete AI-powered content generation system:

1. **Keep All Components**:
   - Keep all workflows and scripts
   - Use the full Notion database schema with retrofit properties

2. **Set Up All Integrations**:
   - Notion API (required)
   - Google Workspace (Drive API, Docs API)
   - NotebookLM API access
   - Configure all required secrets

3. **Customize Content Generation**:
   - Modify `retrofitting/templates/` for your episode format
   - Adjust prompt structure in `scripts/sync_notion_enhanced.py`
   - Customize code naming patterns in `scripts/generate_code_names.py`
   - Update release schedule logic in `scripts/populate_release_schedule.py`

#### Workflow Customization

**Sync Schedule**:
Edit `.github/workflows/sync-notion-episodes.yml`:
```yaml
schedule:
  - cron: '0 0 * * *'  # Change to your preferred schedule
```

**Retrofit Schedule**:
Edit `.github/workflows/retrofit-episodes.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Change to your preferred schedule
```

**Branch Strategy**:
- Keep the full branch structure if you want CI/CD automation
- Or simplify to just `main` and `dev` for basic setups
- Modify `.github/workflows/create-branches.yml` accordingly

#### Branding and Naming

Update these elements to match your podcast:

1. **Repository Name**: Rename in GitHub settings
2. **Episode Naming**: Modify `scripts/sync_notion.py` line ~100-120
3. **Code Name Pattern**: Edit `scripts/generate_code_names.py` to change from "P0D" to your prefix
4. **Documentation**: Update README, SETUP.md, etc. with your project name
5. **Notion Database Name**: Use any name (default "pr-cyberpod" can be changed)

### Integration with Your Tools

#### Using Different Storage

Replace Google Drive with your preferred storage:
- **AWS S3**: Modify `scripts/google_drive_utils.py` to use boto3
- **Azure Blob**: Replace with Azure SDK
- **Local Storage**: Remove cloud upload, keep local files only

#### Using Different AI Services

Replace NotebookLM with alternatives:
- **OpenAI**: Use GPT-4 for content generation
- **Anthropic Claude**: Replace NotebookLM calls with Claude API
- **Local LLMs**: Use Ollama or similar for self-hosted generation

#### Using Different Project Management

Replace Notion with alternatives:
- **Airtable**: Modify `scripts/sync_notion.py` to use Airtable API
- **Google Sheets**: Use Google Sheets API instead
- **Trello**: Integrate with Trello API
- **Jira**: Use Jira API for enterprise setups

### Testing Your Fork

1. **Create a Test Episode**:
   - Add one episode to your Notion database
   - Mark it as "Episode Live"
   - Use a small test MP3 file

2. **Run Manual Sync**:
   - Go to Actions → "Sync Notion Episodes"
   - Click "Run workflow"
   - Verify the episode downloads successfully

3. **Test Retrofit** (if using full automation):
   - Add a prompt to an episode
   - Set Status to "Not started"
   - Run "Retrofit Episodes" workflow in dry run mode
   - Verify documents are created

### Keeping Your Fork Updated

To sync with upstream improvements:

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/PR-CYBR/PR-CYBR-P0D.git

# Fetch and merge updates
git fetch upstream
git checkout main
git merge upstream/main

# Push updates to your fork
git push origin main
```

**Note**: If you've customized heavily, you may need to resolve merge conflicts.

### Community Support

When forking this repository:
- ⭐ Star the original repository to show support
- 📝 Share your use case and modifications in Discussions
- 🐛 Report bugs in your fork or the original project
- 🤝 Contribute improvements back via Pull Requests
- 💬 Join discussions to help other community members

### Licensing

This project is MIT licensed, which means:
- ✅ You can use it commercially
- ✅ You can modify it freely
- ✅ You can distribute it
- ✅ You can use it privately
- ℹ️ Must include the original license
- ℹ️ Must include copyright notice

See [LICENSE](LICENSE) file for full details.

## Setup

### Prerequisites

1. **Notion Database** named "pr-cyberpod" with the following properties:

   **Basic Properties:**
   - **Title** (Title): Episode title
   - **Episode Live** (Checkbox): Publication status
   - **Release Date** (Date): Episode release date
   - **File URL** (URL): Link to MP3 file
   - **Episode Number** (Number): Sequential episode number (optional)
   - **Description** (Text): Episode description (optional)

   **Retrofit Automation Properties (NEW):**
   - **Season** (Number): Season number (1-17)
   - **Episode** (Number): Episode within season (1-52)
   - **Status** (Select): Production status (Not started, In progress, Complete)
   - **Code-Name** (Text): Systematic episode identifier
   - **Prompt-Input** (Text): AI directive for content generation (up to 5,000 chars)
   - **Script-Doc-Link** (URL): Google Doc with episode script
   - **Track-Cloud** (URL): NotebookLM-generated audio file
   - **Duration** (Text): Episode duration (MM:SS)
   - **Show-Notes-Link** (URL): Google Doc with show notes

2. A Notion integration with read/write access to the database

3. Google Cloud Project with Drive API and Docs API enabled

4. NotebookLM API access (for audio generation)

### Required GitHub Secrets

Configure the following secrets in your repository settings:

**Notion Integration:**
- `NOTION_TOKEN`: Your Notion integration token
- `NOTION_DATABASE_ID`: The ID of your pr-cyberpod database
- `PR_CYBR_P0D_S1_DB_ID` through `PR_CYBR_P0D_S17_DB_ID`: Per-season database IDs (optional)

**Google Workspace Integration:**
- `GOOGLE_DRIVE_SERVICE_ACCOUNT`: Service account JSON for Google Drive API
- `PR_CYBR_P0D_DRIVE_FOLDER_ID`: Google Drive folder ID for episode storage

**NotebookLM Integration:**
- `NOTEBOOK_LM_API_KEY`: API key for NotebookLM audio generation

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PR-CYBR/PR-CYBR-P0D.git
   cd PR-CYBR-P0D
   ```

2. Install dependencies (for local testing):
   ```bash
   pip install -r scripts/requirements.txt
   ```

## Usage

### Basic Episode Sync

The original sync workflow runs automatically every day at midnight UTC. No manual intervention is required.

**Manual Sync:**

1. Go to the [Actions tab](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
2. Select "Sync Notion Episodes" workflow
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

### Retrofit Automation (NEW)

The retrofit system automates content generation and metadata management.

**Automatic Operation:**
- Runs nightly at 2 AM UTC
- Detects episodes with `Status = "Not started"`
- Processes through complete automation pipeline
- Updates Notion with generated content

**Manual Trigger:**

1. Go to the [Actions tab](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
2. Select "Retrofit Episodes" workflow
3. Click "Run workflow"
4. Optional: Specify season number or enable dry run mode
5. Click "Run workflow"

**Generate Release Schedule:**
```bash
python scripts/populate_release_schedule.py
# Creates episodes/release-schedule.txt with Mon/Wed/Fri 06:00 UTC pattern
```

**Generate Episode Code Names:**
```bash
python scripts/generate_code_names.py
# Creates episodes/episode-code-names.json and .txt
# Format: P0D-S##-E###-AXIS-SYMBOL
```

**Process Episodes with Prompts:**

1. Add prompt to Notion `Prompt-Input` field (up to 5,000 characters)
2. Or create local prompt file: `episodes/prompts/prompt_S##E###.txt`
3. Run retrofit workflow to:
   - Create Google Doc with script
   - Generate NotebookLM audio
   - Extract duration metadata
   - Create show notes
   - Update all Notion fields

### Automation Pipeline

When an episode enters the retrofit pipeline:

1. **Prompt Processing** → Google Doc created
2. **NotebookLM Integration** → Audio generated from doc
3. **Metadata Extraction** → Duration calculated
4. **Show Notes** → Generated and uploaded
5. **Notion Update** → All fields populated with links

See [Retrofit Guide](retrofitting/docs/RETROFIT_GUIDE.md) for detailed documentation.

## Repository Structure

```
PR-CYBR-P0D/
├── .github/
│   └── workflows/
│       ├── sync-notion-episodes.yml    # Original episode sync
│       ├── retrofit-episodes.yml       # NEW: Retrofit automation
│       └── create-branches.yml         # Branch structure setup
├── .specify/
│   ├── constitution.md                 # Project rules and principles
│   ├── spec.md                         # Technical specification
│   └── plan.md                         # Implementation plan
├── episodes/
│   ├── prompts/                        # NEW: Episode prompt files
│   ├── release-schedule.txt            # NEW: Release dates
│   ├── episode-code-names.json         # NEW: Code names
│   ├── episode-###-title.mp3           # Episode audio files
│   └── episode-###-metadata.json       # Episode metadata
├── retrofitting/                       # NEW: Retrofit automation
│   ├── templates/                      # Document templates
│   │   ├── script-template.md
│   │   ├── show-notes-template.md
│   │   └── README.md
│   └── docs/
│       └── RETROFIT_GUIDE.md           # Complete retrofit documentation
├── scripts/
│   ├── sync_notion.py                  # Original episode sync
│   ├── sync_notion_enhanced.py         # NEW: Bidirectional sync
│   ├── google_drive_utils.py           # NEW: Google Drive integration
│   ├── populate_release_schedule.py    # NEW: Schedule generator
│   ├── generate_code_names.py          # NEW: Code name generator
│   └── requirements.txt                # Python dependencies
├── BRANCHING.md                        # Branching strategy documentation
├── QUICKSTART.md                       # Quick reference guide
└── README.md                           # This file
```

## Automation System

### Fathom → Transcript → Tasks → Agents

This repository implements an automated workflow that transforms meeting transcripts from Fathom AI into actionable tasks distributed across agent repositories.

#### How It Works

```
Zoom Meeting
  ↓ (recorded)
Fathom AI
  ↓ (webhook: fathom_meeting_ended)
.github/workflows/fathom-ingest.yml
  ↓ (processes transcript)
scripts/extract_tasks.py
  ↓ (extracts tasks via LLM)
data/meetings/<meeting_id>/tasks.json
  ↓ (dispatches: create_agent_tasks)
.github/workflows/create-agent-issues.yml
  ↓ (creates issues)
scripts/create_issues.py
  ↓ (routes to agent repos)
PR-CYBR-AGENT-01..12 Issues
  ↓ (labeled: automation/codex)
Codex Autopatch Workflow
  ↓ (creates PR)
.github/workflows/knowledge-sync.yml
  ↓ (on PR merge)
GitHub Discussions + Gist + Notion
```

#### Components

**1. Fathom Webhook Ingestion** (`.github/workflows/fathom-ingest.yml`)
- Triggered by `repository_dispatch` event `fathom_meeting_ended`
- Saves raw transcript to `data/meetings/<meeting_id>/raw.json`
- Calls `scripts/extract_tasks.py` to process transcript
- Outputs structured task list to `tasks.json`
- Dispatches follow-up event `create_agent_tasks`

**2. Task Extraction** (`scripts/extract_tasks.py`)
- Processes meeting transcripts using OpenAI API (or stub mode)
- Identifies actionable tasks from conversation
- Structures tasks with agent assignment, priority, and labels
- Output schema:
  ```json
  {
    "meeting_id": "...",
    "summary": "...",
    "tasks": [
      {
        "task_id": "...",
        "agent": "A-01",
        "repo": "PR-CYBR-AGENT-01",
        "title": "...",
        "description": "...",
        "priority": "high|medium|low",
        "type": "bug|enhancement|documentation",
        "labels": ["automation/codex", "meeting/..."],
        "explicit": true|false
      }
    ]
  }
  ```

**3. Issue Routing** (`.github/workflows/create-agent-issues.yml`)
- Triggered by `create_agent_tasks` dispatch event
- Reads `tasks.json` from meeting directory
- Calls `scripts/create_issues.py` to create GitHub issues
- Routes tasks to appropriate agent repositories

**4. Issue Creation** (`scripts/create_issues.py`)
- Maps agent IDs to repositories using `config/agents.yaml`
- Provides idempotency by checking for existing issues
- Creates or updates issues with proper labels and metadata
- Supports dry-run mode for testing

**5. Agent Repository Mapping** (`config/agents.yaml`)
- Maps A-01 through A-12 to PR-CYBR-AGENT-01 through PR-CYBR-AGENT-12
- Used by `create_issues.py` to route tasks correctly

**6. Codex Autopatch Template** (`.github/workflows/codex-autopatch-template.yml`)
- Reusable workflow for agent repositories
- Triggered by issues labeled `automation/codex`
- Clones repo and runs Codex AI container
- Executes automated code modifications
- Runs tests and creates pull request
- Usage in agent repos:
  ```yaml
  uses: PR-CYBR/PR-CYBR-P0D/.github/workflows/codex-autopatch-template.yml@main
  ```

**7. Knowledge Sync** (`.github/workflows/knowledge-sync.yml`)
- Triggered on PR merge to main branch
- Creates GitHub Discussion with work summary
- Creates public Gist with detailed information
- Syncs results to Notion database via `scripts/notion_sync.py`

**8. Notion Integration** (`scripts/notion_sync.py`)
- Syncs completed work back to Notion
- Uses deterministic UUIDs for idempotency
- Tracks agent, repo, issue, PR, meeting date, and summary
- Automatically updates existing entries

#### File Locations

- **Workflows:** `.github/workflows/fathom-ingest.yml`, `create-agent-issues.yml`, `codex-autopatch-template.yml`, `knowledge-sync.yml`
- **Scripts:** `scripts/extract_tasks.py`, `scripts/create_issues.py`, `scripts/notion_sync.py`
- **Config:** `config/agents.yaml`
- **Data:** `data/meetings/<meeting_id>/` (raw.json, tasks.json)

#### Testing Repository Dispatch Events

**Test Fathom Webhook Ingestion:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "fathom_meeting_ended",
    "client_payload": {
      "meeting_id": "test-meeting-001",
      "transcript": "TODO: Update documentation\nACTION ITEM: Fix bug in agent code",
      "timestamp": "2025-01-15T10:00:00Z"
    }
  }'
```

**Test Issue Creation:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "create_agent_tasks",
    "client_payload": {
      "meeting_id": "test-meeting-001"
    }
  }'
```

**Manual Workflow Trigger:**
```bash
# Via GitHub CLI
gh workflow run fathom-ingest.yml -f meeting_id=test-001 -f transcript="TODO: Test task"

# Via GitHub UI
# Go to Actions → Fathom Meeting Ingest → Run workflow
```

#### Environment Variables

**For Task Extraction:**
- `OPENAI_API_KEY`: OpenAI API key for LLM processing (optional, uses stub if not set)

**For Issue Creation:**
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

**For Notion Sync:**
- `NOTION_TOKEN`: Notion integration token
- `NOTION_DATABASE_ID`: Target Notion database ID

## Branching Strategy

This repository follows the comprehensive branching model from [spec-bootstrap](https://github.com/PR-CYBR/spec-bootstrap). See [BRANCHING.md](BRANCHING.md) for details on:

- Branch purposes and workflows
- Development lifecycle flow
- Automated pull requests between branches
- Branch protection rules

### Branch Overview

- `main` - Stable baseline (production-ready)
- `dev` - Active development
- `spec` - Specifications and requirements
- `plan` - Implementation planning
- `impl` - Implementation work
- `design` - Design artifacts
- `test` - Testing environment
- `stage` - Staging/pre-production
- `prod` - Production deployment
- `pages` - Documentation site
- `codex` - Knowledge base

## Development

### Running Locally

To test the sync script locally:

```bash
export NOTION_TOKEN="your_notion_token"
export NOTION_DATABASE_ID="your_database_id"
python scripts/sync_notion.py
```

### Contributing

1. Follow the specification-driven development workflow (spec → plan → impl → dev → main)
2. Update relevant `.specify/` documents when making changes
3. Ensure all tests pass before submitting PRs
4. Follow the branching strategy outlined in BRANCHING.md

## Troubleshooting

### Episodes Not Syncing

1. Check that "Episode Live" is checked in Notion
2. Verify the File URL is valid and accessible
3. Check GitHub Actions logs for errors
4. Ensure secrets are configured correctly

### Retrofit Automation Issues

1. **Prompts not processing:**
   - Verify `Status` = "Not started" in Notion
   - Check prompt is under 5,000 characters
   - Review workflow logs for errors

2. **Google Drive errors:**
   - Verify service account JSON is valid
   - Check Drive API is enabled
   - Ensure folder ID is correct

3. **NotebookLM failures:**
   - Verify API key is active
   - Check notebook exists for season
   - Review API rate limits

See [Retrofit Guide](retrofitting/docs/RETROFIT_GUIDE.md) for detailed troubleshooting.

### Failed Downloads

- The system will retry failed downloads up to 3 times
- Check that the MP3 file URL is publicly accessible
- Verify the file format is valid MP3

## Documentation

### 📚 Core Documentation
- **[PLAN.md](PLAN.md)** - Comprehensive retrofit roadmap and architecture plan
- **[Quick Start Guide](QUICKSTART.md)** - Quick reference for configuration
- **[Setup Guide](SETUP.md)** - Detailed setup instructions
- **[Contributing Guide](CONTRIBUTING.md)** - Development workflow and guidelines
- **[Security Policy](SECURITY.md)** - Security best practices and vulnerability reporting

### 🏗️ Architecture Documentation
- **[Notion Schema](docs/notion-schema.md)** - Database structure and property definitions
- **[n8n Webhooks](docs/n8n-webhooks.md)** - Webhook integration and payload specifications
- **[Storage & Distribution](docs/storage-distribution.md)** - Storage adapters and RSS hosting
- **[NotebookLM Guide](docs/notebooklm-guide.md)** - AI-powered content generation setup
- **[Fathom Automation Guide](docs/fathom-automation-guide.md)** - Complete guide to Zoom → Fathom → Agent automation system

### 🔧 Technical Documentation
- **[Complete Retrofit Guide](retrofitting/docs/RETROFIT_GUIDE.md)** - Comprehensive automation documentation
- **[Branching Strategy](BRANCHING.md)** - Branch management documentation
- **[Template Documentation](retrofitting/templates/README.md)** - Template system guide

### 🎯 Quick Links
- [`.env.example`](.env.example) - Environment variables reference
- [`CODEOWNERS`](CODEOWNERS) - Code ownership and review assignments
- [GitHub Actions Workflows](.github/workflows/) - CI/CD pipeline definitions

## Replication Guide

Want to create your own autonomous podcast? This repository is designed for easy replication:

### 1. Fork & Configure (5 minutes)
```bash
# Fork this repository
gh repo fork PR-CYBR/PR-CYBR-P0D --clone

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
```

### 2. Set Up Notion (3 minutes)
- Create database using [schema docs](docs/notion-schema.md)
- Create integration and get API token
- Configure GitHub Secrets

### 3. Configure Storage (2 minutes)
- Create Internet Archive account (free)
- Get S3 API keys
- Add to GitHub Secrets

### 4. Launch (immediate)
- Push to your repository
- GitHub Pages automatically deploys RSS feed
- Start creating episodes!

**Total time: ≤10 minutes** ⏱️

See [SETUP.md](SETUP.md) for detailed step-by-step instructions.

## Future Enhancements

- [ ] Notion webhook support for real-time syncing
- [ ] RSS feed generation from episode metadata
- [ ] Episode search and indexing
- [ ] Automated social media announcements
- [ ] Download analytics and tracking
- [ ] Multi-language support for episodes
- [ ] Enhanced AI-assisted show notes
- [ ] Integration with podcast hosting platforms
- [ ] Custom audio processing options
- [ ] Advanced scheduling and campaign management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue in this repository.
