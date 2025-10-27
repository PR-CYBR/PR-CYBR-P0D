# Notion Database Schema

This document describes the required Notion database schema for PR-CYBR-P0D episode management.

## Database Name

**`pr-cyberpod`** (or your chosen name, configured via `NOTION_EPISODES_DB_ID`)

## Required Properties

### Core Episode Properties

| Property Name | Type | Required | Description | Example |
|---------------|------|----------|-------------|---------|
| **Title** | Title | ✅ Yes | Episode title (Notion's default title property) | "Introduction to Cybersecurity" |
| **Season** | Number | ✅ Yes | Season number (1-17) | 1 |
| **Episode** | Number | ✅ Yes | Episode number within season (1-52) | 1 |
| **Status** | Select | ✅ Yes | Production status | "Not started", "In progress", "Complete" |
| **Release Date** | Date | ✅ Yes | Scheduled release date and time | 2024-01-15 06:00 |

### Publishing Properties

| Property Name | Type | Required | Description | Example |
|---------------|------|----------|-------------|---------|
| **Episode Live** | Checkbox | ✅ Yes | Marks episode as published | ☑️ |
| **File URL** | URL | ⚠️ Conditional | Direct URL to MP3 file (required for publishing) | https://archive.org/download/... |

### Content Properties

| Property Name | Type | Required | Description | Example |
|---------------|------|----------|-------------|---------|
| **Description** | Text | ❌ No | Episode description for RSS feed | "In this episode..." |
| **Code-Name** | Text | ❌ No | Systematic episode identifier | "P0D-S01-E001-AXIS-CIPHER" |
| **Prompt-Input** | Text | ❌ No | AI directive for content generation (max 5,000 chars) | "Create an episode about..." |
| **Duration** | Text | ❌ No | Episode duration | "45:30" |

### Integration Properties

| Property Name | Type | Required | Description | Example |
|---------------|------|----------|-------------|---------|
| **Script-Doc-Link** | URL | ❌ No | Google Doc with episode script | https://docs.google.com/document/... |
| **Show-Notes-Link** | URL | ❌ No | Google Doc with show notes | https://docs.google.com/document/... |
| **Track-Cloud** | URL | ❌ No | NotebookLM-generated audio file | https://drive.google.com/file/... |

### Automation Properties

| Property Name | Type | Required | Description | Example |
|---------------|------|----------|-------------|---------|
| **Episode Number** | Number | ❌ No | Sequential global episode number | 52 |
| **Keywords** | Multi-select | ❌ No | Episode tags/keywords | "security", "networking" |

## Status Values

The **Status** select property should have these options:

- **Not started** - Episode planned but not yet in production
- **In progress** - Content creation in progress
- **Complete** - Ready for publishing
- **Live** - Published and available
- **Archived** - Removed from active distribution

## Property Dependencies

### For Basic Episode Sync
Minimum required:
- Title
- Episode Live (checked)
- File URL
- Release Date

### For Pre-Campaign Automation
Required:
- Title, Season, Episode
- Status = "Not started"
- Optional: Prompt-Input

### For Live Publishing
Required:
- All basic sync properties
- Duration (extracted automatically if not provided)
- Description (for RSS feed)

### For Post-Campaign
Required:
- Episode marked as Live
- X days since Release Date

## Database Views

We recommend creating these views in Notion:

### 1. All Episodes (Default)
- **Filter**: None
- **Sort**: Season (ascending), Episode (ascending)
- **Group By**: Season

### 2. Ready to Publish
- **Filter**: Status = "Complete" AND Episode Live = Unchecked
- **Sort**: Release Date (ascending)

### 3. Live Episodes
- **Filter**: Episode Live = Checked
- **Sort**: Release Date (descending)

### 4. In Production
- **Filter**: Status = "In progress" OR Status = "Not started"
- **Sort**: Season (ascending), Episode (ascending)

### 5. This Week
- **Filter**: Release Date is within "This Week"
- **Sort**: Release Date (ascending)

## Notion API Mapping

### Reading from Notion

The sync script maps Notion properties to `meta.yaml` fields:

```python
# Notion → meta.yaml mapping
meta = {
    "title": notion_page["properties"]["Title"]["title"][0]["plain_text"],
    "season": notion_page["properties"]["Season"]["number"],
    "episode": notion_page["properties"]["Episode"]["number"],
    "status": notion_page["properties"]["Status"]["select"]["name"].lower().replace(" ", "-"),
    "release_date": notion_page["properties"]["Release Date"]["date"]["start"],
    "description": notion_page["properties"]["Description"]["rich_text"][0]["plain_text"],
    "codename": notion_page["properties"]["Code-Name"]["rich_text"][0]["plain_text"],
    "audio_url": notion_page["properties"]["File URL"]["url"],
    "duration": notion_page["properties"]["Duration"]["rich_text"][0]["plain_text"],
    # ... more fields
}
```

### Writing to Notion

After processing, the script updates Notion:

```python
# meta.yaml → Notion update
notion.pages.update(
    page_id=page_id,
    properties={
        "Status": {"select": {"name": "Complete"}},
        "Duration": {"rich_text": [{"text": {"content": "45:30"}}]},
        "File URL": {"url": "https://archive.org/download/..."},
        "Script-Doc-Link": {"url": "https://docs.google.com/..."},
        "Show-Notes-Link": {"url": "https://docs.google.com/..."},
        "Episode Live": {"checkbox": True},
    }
)
```

## Sample Notion Entry

Here's a complete example episode entry:

| Field | Value |
|-------|-------|
| Title | Introduction to Cybersecurity Basics |
| Season | 1 |
| Episode | 1 |
| Status | Complete |
| Release Date | 2024-01-15 06:00 |
| Episode Live | ☑️ |
| File URL | https://archive.org/download/pr-cybr-s01e01/audio.mp3 |
| Description | In this inaugural episode, we explore the fundamentals of cybersecurity, covering key concepts like confidentiality, integrity, and availability. Perfect for beginners! |
| Code-Name | P0D-S01-E001-AXIS-CIPHER |
| Prompt-Input | Create an engaging introduction to cybersecurity covering the CIA triad, common threats, and basic security practices. Target audience is technical professionals new to security. |
| Duration | 42:15 |
| Script-Doc-Link | https://docs.google.com/document/d/abc123/edit |
| Show-Notes-Link | https://docs.google.com/document/d/def456/edit |
| Track-Cloud | https://drive.google.com/file/d/ghi789/view |
| Episode Number | 1 |
| Keywords | security, basics, CIA-triad, introduction |

## Sample Notion API Response

```json
{
  "object": "page",
  "id": "abc123def456",
  "created_time": "2024-01-01T00:00:00.000Z",
  "last_edited_time": "2024-01-14T00:00:00.000Z",
  "properties": {
    "Title": {
      "id": "title",
      "type": "title",
      "title": [
        {
          "type": "text",
          "text": {
            "content": "Introduction to Cybersecurity Basics"
          },
          "plain_text": "Introduction to Cybersecurity Basics"
        }
      ]
    },
    "Season": {
      "id": "prop_season",
      "type": "number",
      "number": 1
    },
    "Episode": {
      "id": "prop_episode",
      "type": "number",
      "number": 1
    },
    "Status": {
      "id": "prop_status",
      "type": "select",
      "select": {
        "id": "opt_complete",
        "name": "Complete",
        "color": "green"
      }
    },
    "Release Date": {
      "id": "prop_release",
      "type": "date",
      "date": {
        "start": "2024-01-15T06:00:00.000Z",
        "end": null
      }
    },
    "Episode Live": {
      "id": "prop_live",
      "type": "checkbox",
      "checkbox": true
    },
    "File URL": {
      "id": "prop_url",
      "type": "url",
      "url": "https://archive.org/download/pr-cybr-s01e01/audio.mp3"
    },
    "Description": {
      "id": "prop_desc",
      "type": "rich_text",
      "rich_text": [
        {
          "type": "text",
          "text": {
            "content": "In this inaugural episode, we explore the fundamentals..."
          },
          "plain_text": "In this inaugural episode, we explore the fundamentals..."
        }
      ]
    }
  }
}
```

## Migration from Existing Schema

If you have an existing Notion database, here's how to migrate:

1. **Add new properties** to your existing database (they'll be empty initially)
2. **Keep old properties** during transition period
3. **Run sync script** - it will handle both old and new formats
4. **Gradually populate** new properties (Season, Episode, Status, etc.)
5. **Update views** to use new schema

The sync script is designed to be backwards compatible during migration.

## Notion Integration Setup

### 1. Create Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Name: "PR-CYBR-P0D Sync"
4. Associated workspace: Your workspace
5. Capabilities:
   - ✅ Read content
   - ✅ Update content
   - ❌ Insert content (not needed)
   - ❌ Comment (not needed)

### 2. Connect to Database

1. Open your "pr-cyberpod" database
2. Click "..." menu → "Connections"
3. Select your integration
4. Database is now accessible via API

### 3. Get Database ID

From the database URL:
```
https://notion.so/workspace/abc123def456?v=xyz
                          └──────────┘
                          Database ID
```

### 4. Configure GitHub Secret

Add to your repository secrets:
```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxx
NOTION_EPISODES_DB_ID=abc123def456
```

## Troubleshooting

### "Could not find database"
- Verify database ID is correct
- Ensure integration is connected to the database
- Check token permissions

### "Property not found"
- Ensure property names match exactly (case-sensitive)
- Check for typos in property names
- Verify property type matches expected type

### "Unauthorized"
- Regenerate integration token
- Ensure token is correctly set in GitHub Secrets
- Check integration still has access to workspace

## Additional Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Notion Database Properties](https://developers.notion.com/reference/property-object)
- [Notion Integration Guide](https://developers.notion.com/docs/create-a-notion-integration)

---

**Last Updated:** 2025-10-27  
**Schema Version:** 1.0
