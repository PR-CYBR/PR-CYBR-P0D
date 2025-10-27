# n8n Webhook Integration Guide

This document explains how to integrate PR-CYBR-P0D with n8n for event-driven podcast automation.

## Overview

n8n workflows orchestrate the podcast production pipeline by triggering GitHub Actions workflows at key stages:

1. **Pre-Campaign** - Prepares episode content (transcription, show notes)
2. **Go Live** - Publishes episode (uploads to Archive.org, generates RSS)
3. **Post-Campaign** - Creates recap content and archives

## Architecture

```
Notion Database
  ↓ (Button click or status change)
n8n Workflow
  ↓ (Webhook/API call)
GitHub Actions
  ↓ (Process episode)
Update Notion + Commit to Repo
```

## Webhook Events

### Event Types

| Event Type | Triggered By | Action | GitHub Workflow |
|------------|--------------|--------|-----------------|
| `pre-campaign` | Notion button "Start Production" | Transcribe audio, generate show notes | `pre-release.yml` |
| `go-live` | Notion button "Publish Episode" | Upload to Archive.org, generate RSS | `go-live.yml` |
| `post-campaign` | Scheduled or button | Generate recap, archive episode | `post-campaign.yml` |

### GitHub Repository Dispatch

All events use GitHub's [`repository_dispatch`](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event) API.

**Endpoint:**
```
POST https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches
```

**Authentication:**
```
Authorization: Bearer ghp_xxxxxxxxxxxxxxxxxxxxx
```

## Webhook Payloads

### Pre-Campaign Payload

**Event Type:** `pre-campaign`

```json
{
  "event_type": "pre-campaign",
  "client_payload": {
    "season": 1,
    "episode": 1,
    "notion_page_id": "abc123def456",
    "force": false
  }
}
```

**Fields:**
- `season` (number, required) - Season number
- `episode` (number, required) - Episode number within season
- `notion_page_id` (string, optional) - Notion page ID for updates
- `force` (boolean, optional) - Force re-transcription even if exists

**curl Example:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "pre-campaign",
    "client_payload": {
      "season": 1,
      "episode": 1,
      "notion_page_id": "abc123",
      "force": false
    }
  }'
```

### Go Live Payload

**Event Type:** `go-live`

```json
{
  "event_type": "go-live",
  "client_payload": {
    "season": 1,
    "episode": 1,
    "notion_page_id": "abc123def456",
    "publish_date": "2024-01-15T06:00:00Z"
  }
}
```

**Fields:**
- `season` (number, required) - Season number
- `episode` (number, required) - Episode number within season
- `notion_page_id` (string, optional) - Notion page ID for updates
- `publish_date` (string, optional) - ISO 8601 timestamp for scheduled publish

**curl Example:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "go-live",
    "client_payload": {
      "season": 1,
      "episode": 1,
      "notion_page_id": "abc123"
    }
  }'
```

### Post-Campaign Payload

**Event Type:** `post-campaign`

```json
{
  "event_type": "post-campaign",
  "client_payload": {
    "season": 1,
    "episode": 1,
    "notion_page_id": "abc123def456",
    "generate_recap": true,
    "archive": true
  }
}
```

**Fields:**
- `season` (number, required) - Season number
- `episode` (number, required) - Episode number within season
- `notion_page_id` (string, optional) - Notion page ID for updates
- `generate_recap` (boolean, optional) - Generate recap article (default: true)
- `archive` (boolean, optional) - Mark episode as archived (default: true)

**curl Example:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "post-campaign",
    "client_payload": {
      "season": 1,
      "episode": 1,
      "generate_recap": true
    }
  }'
```

## n8n Workflow Setup

### Prerequisites

1. **n8n instance** - Self-hosted or cloud
2. **GitHub personal access token** - With `repo` scope
3. **Notion integration** - Connected to your database

### Workflow Structure (All Three Workflows)

Each n8n workflow follows this pattern:

```
┌─────────────────┐
│ Notion Trigger  │ Watch for button click or status change
└────────┬────────┘
         │
┌────────▼────────┐
│ Notion Get Page │ Fetch episode details (Season, Episode, etc.)
└────────┬────────┘
         │
┌────────▼────────┐
│ Function Node   │ Build GitHub dispatch payload
└────────┬────────┘
         │
┌────────▼────────┐
│ HTTP Request    │ POST to GitHub API
└────────┬────────┘
         │
┌────────▼────────┐
│ Notion Update   │ Update status fields
└─────────────────┘
```

### 1. Pre-Campaign Workflow

**Trigger:** Notion button "Start Production" or Status → "In progress"

**n8n Nodes:**

1. **Notion Trigger**
   - Database: pr-cyberpod
   - Trigger: Database Item Created/Updated
   - Filter: Status = "In progress"

2. **Notion Get Page**
   - Page ID: `{{$json.id}}`
   - Properties to fetch: Season, Episode, Status

3. **Function**
   ```javascript
   return {
     json: {
       event_type: "pre-campaign",
       client_payload: {
         season: $json.properties.Season.number,
         episode: $json.properties.Episode.number,
         notion_page_id: $json.id,
         force: false
       }
     }
   };
   ```

4. **HTTP Request**
   - Method: POST
   - URL: `https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches`
   - Headers:
     - `Accept: application/vnd.github+json`
     - `Authorization: Bearer {{$env.GITHUB_TOKEN}}`
   - Body: `{{$json}}`

5. **Notion Update**
   - Page ID: `{{$node["Notion Trigger"].json.id}}`
   - Properties:
     - Status: "In progress"
     - (Add timestamp or notes as needed)

### 2. Go Live Workflow

**Trigger:** Notion button "Publish Episode" or Status → "Complete"

Same structure as Pre-Campaign, but:
- Event type: `"go-live"`
- Notion Status filter: "Complete"
- Final status update: "Live"

### 3. Post-Campaign Workflow

**Trigger:** Scheduled (X days after publish) or manual button

Same structure, but:
- Event type: `"post-campaign"`
- Notion Status filter: "Live"
- Include time check: `Release Date + X days`
- Final status update: "Archived"

## Importing n8n Workflows

1. **Download workflow JSON**
   - Pre-campaign: `/workflows/n8n/pre-campaign.json`
   - Go Live: `/workflows/n8n/live.json`
   - Post-campaign: `/workflows/n8n/post.json`

2. **Import to n8n**
   - Open n8n
   - Click "Import from File"
   - Select workflow JSON
   - Click "Import"

3. **Configure credentials**
   - Add Notion OAuth2 credentials
   - Add GitHub personal access token
   - Test connections

4. **Activate workflow**
   - Review all nodes
   - Test with a sample episode
   - Click "Active" toggle

## Environment Variables

Set these in n8n or GitHub Secrets:

### In n8n
- `GITHUB_TOKEN` - Personal access token with `repo` scope
- `NOTION_TOKEN` - Already configured in Notion OAuth2

### In GitHub Secrets
- `NOTION_TOKEN` - For workflows to update Notion
- `NOTION_EPISODES_DB_ID` - Database ID
- (All other secrets per `.env.example`)

## Testing

### Manual Testing

1. **Test GitHub Dispatch (without n8n):**
   ```bash
   # Replace with your token
   export GITHUB_TOKEN=ghp_xxxxx
   
   # Test pre-campaign
   curl -X POST \
     -H "Accept: application/vnd.github+json" \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
     -d '{"event_type":"pre-campaign","client_payload":{"season":1,"episode":1}}'
   
   # Check GitHub Actions tab for workflow run
   ```

2. **Test n8n Workflow:**
   - Open workflow in n8n
   - Click "Execute Workflow" button
   - Provide test data
   - Check execution log

3. **End-to-End Test:**
   - Create test episode in Notion
   - Click "Start Production" button (or change status)
   - Verify n8n workflow triggers
   - Verify GitHub Actions workflow runs
   - Check episode files updated in repo

## Notion Button Setup

To add buttons to trigger workflows:

1. **Add Button Property**
   - In Notion database, add property
   - Type: "Button"
   - Name: "Start Production", "Publish Episode", "Archive Episode"

2. **Configure Button**
   - Click button configuration
   - Action: "Webhook"
   - URL: Your n8n webhook endpoint
   - Method: POST
   - Headers: As needed
   - Body: Include page ID

**Alternative:** Use n8n Notion trigger to watch status changes instead of buttons.

## Monitoring & Debugging

### Check GitHub Actions

1. Go to Actions tab in GitHub
2. Find workflow run
3. Check logs for errors
4. Verify payload received

### Check n8n Execution Log

1. Open workflow in n8n
2. Click "Executions" tab
3. Review each node's input/output
4. Check for HTTP errors

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid GitHub token | Regenerate token, ensure `repo` scope |
| 404 Not Found | Wrong repository or workflow | Verify repo name and workflow exists |
| 422 Unprocessable | Invalid payload | Check JSON structure matches expected |
| Workflow doesn't trigger | n8n not watching properly | Check trigger configuration |
| Notion update fails | Invalid page ID | Verify page ID in payload |

## Security Considerations

1. **Tokens**
   - Store GitHub token securely in n8n credentials
   - Use environment variables, not hardcoded values
   - Rotate tokens regularly

2. **Webhook Authentication**
   - If exposing n8n webhooks, use authentication
   - Consider IP whitelisting
   - Use HTTPS only

3. **Notion Permissions**
   - Integration should have minimal permissions
   - Read/update only, no delete

4. **GitHub Token Scope**
   - Limit to `repo` scope
   - Don't use admin or org tokens

## Advanced Configuration

### Conditional Workflows

Use n8n's IF node to add conditions:

```javascript
// Only trigger if release date is in the future
const releaseDate = new Date($json.properties["Release Date"].date.start);
const now = new Date();

return [{
  json: {
    shouldTrigger: releaseDate > now
  }
}];
```

### Error Handling

Add error workflow to notify on failures:

1. Add "On Error" trigger
2. Send notification (Slack, email, etc.)
3. Log to database
4. Update Notion with error status

### Batch Processing

Process multiple episodes:

1. Use Notion "Filter" to get multiple episodes
2. Loop through results
3. Trigger workflows for each
4. Rate limit to avoid API throttling

## Workflow Files

Pre-built n8n workflow exports are available in `/workflows/n8n/`:

- `pre-campaign.json` - Pre-production workflow
- `live.json` - Publishing workflow
- `post.json` - Post-campaign workflow
- `README.md` - Import instructions

These are templates with placeholders. Customize for your setup.

## Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [GitHub API - Repository Dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Notion API](https://developers.notion.com/)
- [GitHub Actions - Webhook Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch)

---

**Last Updated:** 2025-10-27  
**Version:** 1.0
