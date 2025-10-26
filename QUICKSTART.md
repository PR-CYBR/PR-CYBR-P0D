# Quick Start - Configuration Reference

This is a quick reference for configuring PR-CYBR-P0D.

## Required GitHub Secrets

| Secret Name | Description | Where to Get It |
|-------------|-------------|-----------------|
| `NOTION_TOKEN` | Notion API integration token | [Create at notion.so/my-integrations](https://www.notion.so/my-integrations) |
| `NOTION_DATABASE_ID` | Database ID for pr-cyberpod | From your database URL (32-character hex string) |

## Required Notion Database Properties

| Property Name | Type | Required | Example |
|---------------|------|----------|---------|
| Title | Title | ✅ Yes | "Episode 1: Introduction" |
| Episode Live | Checkbox | ✅ Yes | ☑️ |
| Release Date | Date | ✅ Yes | 2024-01-15 |
| File URL | URL | ✅ Yes | https://example.com/ep1.mp3 |
| Episode Number | Number | ❌ No | 1 |
| Description | Text | ❌ No | "In this episode..." |

## Workflow Triggers

### Automatic (Scheduled)
- **When**: Daily at midnight UTC
- **Trigger**: Cron schedule in workflow
- **Action**: Syncs all live episodes

### Manual (On-Demand)
- **Where**: Actions → "Sync Notion Episodes" → Run workflow
- **When**: Anytime you want to sync immediately
- **Action**: Same as scheduled sync

### Webhook (Setup Required)
- **When**: Notion database changes
- **Trigger**: `repository_dispatch` event with type `notion-webhook`
- **Status**: Workflow ready, Notion webhook endpoint setup required
- **Action**: Real-time sync on database updates

## File Naming Pattern

```
episode-{NUM}-{slug}.mp3
episode-{NUM}-{slug}-metadata.json
```

Examples:
- `episode-001-introduction.mp3`
- `episode-042-security-basics.mp3`
- `episode-a1b2c3d4-episode-title.mp3` (no episode number, hash from title)

## First-Time Setup Checklist

- [ ] Create Notion database named "pr-cyberpod"
- [ ] Add required properties to database
- [ ] Create Notion integration
- [ ] Connect integration to database
- [ ] Copy integration token
- [ ] Get database ID from URL
- [ ] Add secrets to GitHub repository
- [ ] Run "Create Branch Structure" workflow
- [ ] Add test episode to Notion
- [ ] Check "Episode Live" checkbox
- [ ] Run "Sync Notion Episodes" workflow
- [ ] Verify episode appears in `/episodes/`

## Common Issues

| Problem | Solution |
|---------|----------|
| Episodes not syncing | Check "Episode Live" is checked |
| Authentication error | Verify `NOTION_TOKEN` is correct |
| Database not found | Verify `NOTION_DATABASE_ID` is correct |
| Download fails | Check File URL is publicly accessible |
| Missing metadata | Ensure all required properties exist |

## Quick Links

- [Full Setup Guide](SETUP.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Branching Strategy](BRANCHING.md)
- [Episodes Directory](episodes/README.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
- **Logs**: [GitHub Actions](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
- **Docs**: [Main README](README.md)
