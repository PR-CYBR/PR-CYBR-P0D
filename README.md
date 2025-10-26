# PR-CYBR-P0D

[![Sync Notion Episodes](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml)
[![Retrofit Episodes](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/retrofit-episodes.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/retrofit-episodes.yml)

The Official PR-CYBR Podcast Repository - Automated podcast episode management, content generation, and distribution system with AI-assisted production pipeline.

## Overview

PR-CYBR-P0D is a comprehensive podcast automation system that:

1. **Syncs episodes** from Notion to GitHub automatically
2. **Generates content** using AI-powered prompts and NotebookLM
3. **Manages metadata** across Notion, GitHub, and Google Workspace
4. **Automates production** from prompt to published episode

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

- **[Complete Retrofit Guide](retrofitting/docs/RETROFIT_GUIDE.md)** - Comprehensive automation documentation
- **[Quick Start Guide](QUICKSTART.md)** - Quick reference for configuration
- **[Setup Guide](SETUP.md)** - Detailed setup instructions
- **[Branching Strategy](BRANCHING.md)** - Branch management documentation
- **[Template Documentation](retrofitting/templates/README.md)** - Template system guide

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
