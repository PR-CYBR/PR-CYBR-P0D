# Setup Guide for PR-CYBR-P0D

This guide will help you set up the PR-CYBR-P0D podcast synchronization system.

> **For Forks**: If you're setting up your own fork of this repository, see the comprehensive [Forking This Repository](README.md#forking-this-repository) section in the README for customization options and integration alternatives.

## Prerequisites

Before you begin, you'll need:

1. A Notion account with access to create integrations
2. A Notion database for your podcast episodes
3. GitHub repository access with permissions to add secrets
4. Podcast episode MP3 files hosted at accessible URLs

## Step 1: Set Up Notion Database

### Create the Database

1. In Notion, create a new database called **"pr-cyberpod"**
2. Add the following properties:

| Property Name | Type | Required | Description |
|---------------|------|----------|-------------|
| Title | Title | Yes | The default title property |
| Episode Live | Checkbox | Yes | Check this to publish the episode |
| Release Date | Date | Yes | When the episode was/will be released |
| File URL | URL | Yes | Direct link to the MP3 file |
| Episode Number | Number | No | Sequential episode number |
| Description | Text | No | Episode description/show notes |
| Duration | Text | No | Episode length (e.g., "45:30") |

### Example Database Entry

Here's what a sample episode entry looks like:

- **Title**: "Introduction to Cybersecurity"
- **Episode Live**: ☑️ (checked)
- **Release Date**: 2024-01-15
- **File URL**: `https://example.com/podcasts/episode-001.mp3`
- **Episode Number**: 1
- **Description**: "In this episode, we discuss the basics of cybersecurity..."
- **Duration**: "45:30"

## Step 2: Create a Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Configure the integration:
   - **Name**: "PR-CYBR-P0D Sync"
   - **Associated workspace**: Select your workspace
   - **Type**: Internal Integration
   - **Capabilities**: 
     - ☑️ Read content
     - ☐ Update content (not needed)
     - ☐ Insert content (not needed)
4. Click **"Submit"**
5. Copy the **"Internal Integration Token"** (starts with `secret_`)

### Connect Integration to Database

1. Open your "pr-cyberpod" database in Notion
2. Click the **"..."** menu in the top-right corner
3. Scroll down to **"Connections"**
4. Click **"Connect to"** and select your integration
5. The database is now accessible to your integration

## Step 3: Get Your Database ID

You need the database ID to query it from the API.

### Method 1: From Database URL

1. Open your database in Notion
2. Look at the URL in your browser
3. The database ID is the 32-character string after the workspace name and before the `?v=`

Example URL:
```
https://www.notion.so/myworkspace/abc123def456...?v=...
                                  └─────────────┘
                                    Database ID
```

### Method 2: From Share Menu

1. Click **"Share"** in the top-right of your database
2. Click **"Copy link"**
3. The database ID is in the copied link

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add the following secrets:

### NOTION_TOKEN

- **Name**: `NOTION_TOKEN`
- **Value**: Your integration token from Step 2 (starts with `secret_`)

### NOTION_DATABASE_ID

- **Name**: `NOTION_DATABASE_ID`
- **Value**: Your database ID from Step 3 (32-character string)

## Step 5: Create Branch Structure

The repository needs the full branch structure from spec-bootstrap:

1. Go to the **Actions** tab in your repository
2. Select **"Create Branch Structure"** workflow
3. Click **"Run workflow"**
4. Select the branch you want to create branches from (usually `main`)
5. Click **"Run workflow"**

This will create all required branches: `dev`, `spec`, `plan`, `impl`, `design`, `test`, `stage`, `prod`, `pages`, and `codex`.

## Step 6: Test the Sync

### Manual Test

1. Add a test episode to your Notion database
2. Check the **"Episode Live"** checkbox
3. Go to **Actions** → **"Sync Notion Episodes"**
4. Click **"Run workflow"**
5. Select your branch and click **"Run workflow"**
6. Watch the workflow execute
7. Check the `episodes/` directory for your new episode

### Verify the Workflow

The workflow should:
- ✅ Connect to Notion successfully
- ✅ Find your live episode
- ✅ Download the MP3 file
- ✅ Create a metadata JSON file
- ✅ Commit the files to the repository

## Step 7: Configure Automatic Sync

The workflow is already configured to run daily at midnight UTC. No additional setup is needed!

If you want to change the schedule:

1. Edit `.github/workflows/sync-notion-episodes.yml`
2. Modify the cron expression under `schedule:`
   ```yaml
   schedule:
     - cron: '0 0 * * *'  # Runs at midnight UTC
   ```

### Cron Expression Examples

- Every day at 3 AM UTC: `0 3 * * *`
- Every 6 hours: `0 */6 * * *`
- Every Monday at noon: `0 12 * * 1`

## Troubleshooting

### Episodes Not Syncing

**Problem**: Episodes marked as live aren't appearing in the repository

**Solutions**:
1. Verify the "Episode Live" checkbox is checked in Notion
2. Check that the File URL is valid and accessible
3. Review GitHub Actions logs for errors
4. Verify secrets are correctly configured
5. Ensure the integration is connected to your database

### Authentication Errors

**Problem**: Workflow fails with "unauthorized" or "authentication failed"

**Solutions**:
1. Verify `NOTION_TOKEN` secret is set correctly
2. Check that the integration still exists in Notion
3. Ensure the integration is connected to your database
4. Generate a new integration token if needed

### Download Failures

**Problem**: MP3 files fail to download

**Solutions**:
1. Verify the File URL is publicly accessible
2. Test the URL in a web browser
3. Check file size (very large files may timeout)
4. Ensure the URL is a direct link to the MP3 file
5. Check GitHub Actions logs for specific error messages

### Missing Metadata

**Problem**: Episodes sync but metadata is incomplete

**Solutions**:
1. Ensure all required fields are filled in Notion:
   - Title
   - Episode Live
   - Release Date
   - File URL
2. Check that property names match exactly (case-sensitive)
3. Review the episode metadata JSON file for details

## Hosting Your MP3 Files

Your podcast MP3 files need to be hosted at a publicly accessible URL. Here are some options:

### Option 1: Cloud Storage

- **AWS S3**: Create a public bucket and upload files
- **Google Cloud Storage**: Create a bucket with public access
- **Azure Blob Storage**: Create a container with public access
- **Cloudflare R2**: Cost-effective S3-compatible storage

### Option 2: Podcast Hosting Services

- **Anchor**: Free podcast hosting with distribution
- **Libsyn**: Professional podcast hosting
- **Podbean**: Popular podcast platform
- **Buzzsprout**: User-friendly podcast host

### Option 3: File Hosting

- **Dropbox**: Generate public sharing links
- **Google Drive**: Create shareable links with "Anyone with link can view"
- **OneDrive**: Share files with public links

**Important**: Ensure your links are direct download links, not web pages that display the file.

## Next Steps

After setup is complete:

1. ✅ Create your first episode in Notion
2. ✅ Check the episode live checkbox
3. ✅ Wait for automatic sync (or trigger manually)
4. ✅ Verify the episode appears in `/episodes/`
5. ✅ Set up RSS feed generation (future enhancement)
6. ✅ Configure branch protection rules for production branches

## Support

If you encounter issues not covered in this guide:

1. Check the [GitHub Issues](https://github.com/PR-CYBR/PR-CYBR-P0D/issues)
2. Review the [GitHub Actions logs](https://github.com/PR-CYBR/PR-CYBR-P0D/actions)
3. Open a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Relevant error messages
   - Screenshots if applicable

## Security Best Practices

1. **Never commit secrets**: Always use GitHub Secrets for API tokens
2. **Use read-only tokens**: Notion integration only needs read access
3. **Validate URLs**: The script validates URLs before downloading
4. **Review changes**: Check commits before merging to production branches
5. **Rotate tokens**: Periodically regenerate integration tokens
6. **Monitor usage**: Watch for unexpected API usage or downloads

---

**Congratulations!** Your PR-CYBR-P0D podcast synchronization system is now set up and ready to use. 🎙️
