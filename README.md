# PR-CYBR-P0D

[![Sync Notion Episodes](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml/badge.svg)](https://github.com/PR-CYBR/PR-CYBR-P0D/actions/workflows/sync-notion-episodes.yml)

The Official PR-CYBR Podcast Repository - Automated podcast episode management and distribution system.

## Overview

PR-CYBR-P0D automatically syncs podcast episodes from a Notion database called "pr-cyberpod" to this repository. When an episode is marked as "Episode Live" in Notion, the system automatically downloads the MP3 file and commits it to the `/episodes/` directory.

## Features

- 🎙️ **Automated Episode Sync**: Episodes marked as live in Notion are automatically downloaded and committed
- 📅 **Scheduled Updates**: Daily synchronization checks for new episodes
- 🔄 **Manual Trigger**: On-demand sync via GitHub Actions workflow_dispatch
- 📊 **Metadata Tracking**: Each episode includes JSON metadata with title, release date, and description
- 🌳 **Full Branch Structure**: Maintains the complete spec-bootstrap branching strategy for proper CI/CD

## Setup

### Prerequisites

1. A Notion database named "pr-cyberpod" with the following properties:
   - **Title** (Title): Episode title
   - **Episode Live** (Checkbox): Publication status
   - **Release Date** (Date): Episode release date
   - **File URL** (URL): Link to MP3 file
   - **Episode Number** (Number): Sequential episode number (optional)
   - **Description** (Text): Episode description (optional)

2. A Notion integration with read access to the database

### Required GitHub Secrets

Configure the following secrets in your repository settings:

- `NOTION_TOKEN`: Your Notion integration token
- `NOTION_DATABASE_ID`: The ID of your pr-cyberpod database

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

### Automatic Sync

The sync workflow runs automatically every day at midnight UTC. No manual intervention is required.

### Manual Sync

To trigger a sync manually:

1. Go to the [Actions tab](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
2. Select "Sync Notion Episodes" workflow
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## Repository Structure

```
PR-CYBR-P0D/
├── .github/
│   └── workflows/
│       └── sync-notion-episodes.yml    # GitHub Actions workflow
├── .specify/
│   ├── constitution.md                  # Project rules and principles
│   ├── spec.md                          # Technical specification
│   ├── plan.md                          # Implementation plan
│   └── tasks/                           # Task breakdown
├── episodes/
│   ├── episode-001-title.mp3           # Episode audio files
│   ├── episode-001-metadata.json       # Episode metadata
│   └── ...
├── scripts/
│   ├── sync_notion.py                  # Notion sync script
│   └── requirements.txt                # Python dependencies
├── BRANCHING.md                        # Branching strategy documentation
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

### Failed Downloads

- The system will retry failed downloads up to 3 times
- Check that the MP3 file URL is publicly accessible
- Verify the file format is valid MP3

## Future Enhancements

- [ ] Notion webhook support for real-time syncing
- [ ] RSS feed generation
- [ ] Episode search and indexing
- [ ] Automated social media announcements
- [ ] Download analytics and tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue in this repository.
