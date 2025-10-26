# Episodes Directory

This directory contains all synchronized podcast episodes from the Notion database.

## Structure

Each episode consists of two files:

1. **Audio File** (`*.mp3`): The podcast episode audio
2. **Metadata File** (`*-metadata.json`): Episode information and metadata

### Naming Convention

Files follow this pattern:

```
episode-{number}-{slug}.mp3
episode-{number}-{slug}-metadata.json
```

Where:
- `{number}` is a 3-digit episode number (e.g., 001, 002, 123)
- `{slug}` is a URL-friendly version of the episode title

**Example:**
```
episode-001-introduction-to-cybersecurity.mp3
episode-001-introduction-to-cybersecurity-metadata.json
```

If no episode number is provided in Notion, a hash-based identifier is used:
```
episode-a1b2c3d4-introduction-to-cybersecurity.mp3
episode-a1b2c3d4-introduction-to-cybersecurity-metadata.json
```

## Metadata File Format

Each metadata JSON file contains:

```json
{
  "title": "Episode Title",
  "release_date": "2024-01-15",
  "episode_number": 1,
  "description": "Episode description and show notes",
  "notion_id": "notion-page-id",
  "file_url": "https://example.com/episode.mp3",
  "downloaded_at": "2024-01-15T12:00:00",
  "file_size": 45678901
}
```

### Fields

- **title**: Episode title from Notion
- **release_date**: Release date in ISO format (YYYY-MM-DD)
- **episode_number**: Sequential episode number (null if not provided)
- **description**: Episode description/show notes
- **notion_id**: Unique identifier from Notion database
- **file_url**: Original URL where the MP3 was downloaded from
- **downloaded_at**: Timestamp when the file was downloaded (UTC)
- **file_size**: Size of the MP3 file in bytes

## Synchronization

Episodes are automatically synchronized from the Notion database when:

1. The "Episode Live" checkbox is checked in Notion
2. The scheduled workflow runs (daily at midnight UTC)
3. The workflow is manually triggered via GitHub Actions

### What Gets Synced

Only episodes that meet these criteria are synced:
- "Episode Live" checkbox is **checked** ✓
- "File URL" field contains a valid URL
- "Title" field is not empty
- Episode has not been previously downloaded

### Duplicate Prevention

The sync script checks if an episode already exists before downloading. Once an episode is synced, it will not be downloaded again, even if the Notion entry is updated.

## File Management

### Adding Episodes

Episodes are automatically added by the sync workflow. Manual additions are not recommended as they won't have proper metadata.

### Removing Episodes

To remove an episode:
1. Delete both the `.mp3` and `-metadata.json` files
2. Commit and push the changes
3. The episode will not be re-downloaded unless you delete it from Notion and re-add it

### Updating Episodes

Episodes are immutable once published. To update an episode:
1. Remove the old episode files
2. Update the Notion entry (or create a new one)
3. Wait for the next sync or trigger manually

## Storage Considerations

### Repository Size

- MP3 files can be large (typically 20-100 MB per episode)
- GitHub repositories have a soft limit of 1 GB
- Consider using [Git LFS](https://git-lfs.github.com/) for large repositories

### Git LFS (Future Enhancement)

If your repository grows beyond 1 GB, consider enabling Git LFS:

```bash
# Install Git LFS
git lfs install

# Track MP3 files
git lfs track "*.mp3"

# Commit the .gitattributes file
git add .gitattributes
git commit -m "chore: enable Git LFS for MP3 files"
```

## Troubleshooting

### Missing Episodes

If episodes aren't appearing:
1. Check that "Episode Live" is checked in Notion
2. Verify the File URL is accessible
3. Review GitHub Actions logs for errors
4. Ensure secrets (NOTION_TOKEN, NOTION_DATABASE_ID) are configured

### Incomplete Metadata

If metadata is missing fields:
1. Check that all required Notion properties exist
2. Verify property names match exactly (case-sensitive)
3. Ensure date fields are properly formatted

### Large Files

If large files fail to download:
1. Check the timeout settings in the sync script
2. Ensure your hosting service supports large file downloads
3. Consider enabling streaming downloads for files > 100 MB

## Best Practices

1. **Consistent Naming**: Use episode numbers for sequential ordering
2. **Complete Metadata**: Fill in all Notion fields for rich metadata
3. **Test First**: Use a test episode before syncing many episodes
4. **Monitor Size**: Keep an eye on repository size
5. **Backup**: Keep backups of your MP3 files elsewhere

## Example Directory

```
episodes/
├── .gitkeep
├── README.md (this file)
├── SAMPLE-metadata.json
├── episode-001-welcome-to-pr-cybr.mp3
├── episode-001-welcome-to-pr-cybr-metadata.json
├── episode-002-cybersecurity-basics.mp3
├── episode-002-cybersecurity-basics-metadata.json
├── episode-003-threat-modeling.mp3
└── episode-003-threat-modeling-metadata.json
```

---

For more information, see the main [README.md](../README.md) or [SETUP.md](../SETUP.md).
