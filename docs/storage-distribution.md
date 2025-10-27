# Storage & Distribution Architecture

This document describes the podcast episode storage and distribution system for PR-CYBR-P0D.

## Overview

PR-CYBR-P0D uses a **self-hosted RSS + pluggable storage** architecture for maximum control and minimal cost.

### Key Principles

1. **Self-hosted RSS feed** - Full control over feed, hosted via GitHub Pages
2. **Pluggable storage** - Swap storage backends without changing workflows
3. **Free/low-cost priority** - Default to Internet Archive (free, permanent)
4. **Adapter pattern** - Easy to add new storage providers

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Episode Production                     │
│  (Notion → GitHub Actions → Transcription/Show Notes)   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Storage Adapter Layer                   │
│  (Selectable via STORAGE_ADAPTER environment variable)  │
└───────────────────────┬─────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ Archive  │   │ Spotify  │   │  Custom  │
  │   .org   │   │   for    │   │ Storage  │
  │          │   │ Podcasts │   │          │
  └────┬─────┘   └────┬─────┘   └────┬─────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼ (Returns canonical URL)
         ┌────────────────────────┐
         │   RSS Feed Generator   │
         │ (docs/podcast.xml)     │
         └────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │    GitHub Pages        │
         │  (Public Distribution) │
         └────────────────────────┘
```

## Default: Internet Archive + Self-Hosted RSS

### Why Internet Archive?

✅ **Pros:**
- Completely free
- Permanent storage (non-profit mission)
- S3-compatible API
- High availability
- No bandwidth limits
- Open access philosophy aligns with podcast goals
- Automatic backups and mirrors

❌ **Cons:**
- Not specifically designed for podcasting
- No built-in analytics
- Upload speed can be slow
- Less "professional" perception
- No automated distribution to Apple/Spotify

### Implementation

**Upload Script:** `scripts/upload_archive.py`

**Features:**
- S3-compatible API via `internetarchive` Python library
- Uploads MP3 with metadata
- Returns canonical URL for RSS feed
- Supports retry logic
- Validates file before upload

**Configuration:**
```bash
ARCHIVE_ACCESS_KEY=your_access_key
ARCHIVE_SECRET_KEY=your_secret_key
ARCHIVE_IDENTIFIER_PREFIX=pr-cybr-pod
ARCHIVE_COLLECTION=opensource_audio
```

**Episode Identifier Format:**
```
{PREFIX}-s{SEASON}-e{EPISODE}
Example: pr-cybr-pod-s01-e001
```

**Archive.org URL Format:**
```
https://archive.org/download/{identifier}/{filename}
Example: https://archive.org/download/pr-cybr-pod-s01-e001/episode.mp3
```

### RSS Feed via GitHub Pages

**Generator:** `scripts/generate_rss.py`

**Output:** `docs/podcast.xml`

**Hosting:** GitHub Pages (free, automatic HTTPS)

**Feed URL:**
```
https://pr-cybr.github.io/PR-CYBR-P0D/podcast.xml
```

**Features:**
- RSS 2.0 compliant
- Podcast namespace support
- iTunes/Apple Podcasts tags
- Proper `<enclosure>` with length/type
- Stable `<guid>` (episode codename)
- RFC-822 dates
- Chapter markers (future)

## Alternative: Spotify for Podcasters

**Status:** Supported via adapter (to be implemented)

**When to use:**
- Need professional distribution
- Want Spotify-specific features
- Require analytics dashboard
- Desire automatic distribution to multiple platforms

**Configuration:**
```bash
STORAGE_ADAPTER=spotify
SPOTIFY_API_CLIENT_ID=xxxxx
SPOTIFY_API_CLIENT_SECRET=xxxxx
SPOTIFY_SHOW_ID=xxxxx
```

**Implementation:**
```python
# scripts/upload_archive.py
if STORAGE_ADAPTER == "spotify":
    from adapters.spotify import SpotifyAdapter
    adapter = SpotifyAdapter()
    result = adapter.upload(audio_file, metadata)
```

**Pros:**
- Professional hosting
- Built-in analytics
- Auto-distribution to Spotify, Apple, Google
- Monetization options

**Cons:**
- Subject to platform terms
- Less control
- Potential for platform changes
- Not truly "self-hosted"

## Custom Storage Adapter

**Status:** Interface defined, implementation flexible

**When to use:**
- Enterprise requirements
- Existing storage infrastructure
- Special compliance needs
- Custom CDN

**Configuration:**
```bash
STORAGE_ADAPTER=custom
CUSTOM_STORAGE_ENDPOINT=https://your-storage.com/api
CUSTOM_STORAGE_TOKEN=xxxxx
```

**Interface:**

All storage adapters must implement this interface:

```python
class StorageAdapter(ABC):
    @abstractmethod
    def upload(self, audio_file: Path, metadata: dict) -> dict:
        """
        Upload audio file to storage.
        
        Args:
            audio_file: Path to MP3 file
            metadata: Episode metadata dict
            
        Returns:
            {
                "url": "https://...",      # Canonical media URL
                "length": 65432100,        # File size in bytes
                "type": "audio/mpeg",      # MIME type
                "duration": "45:30"        # Optional: HH:MM:SS
            }
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Check if adapter is configured correctly."""
        pass
    
    @abstractmethod
    def get_info(self, identifier: str) -> dict:
        """Get info about already-uploaded file."""
        pass
```

**Example Custom Implementation:**

```python
# adapters/s3.py
import boto3
from .base import StorageAdapter

class S3Adapter(StorageAdapter):
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )
        self.bucket = os.getenv('S3_BUCKET')
        
    def upload(self, audio_file, metadata):
        key = f"episodes/{metadata['season']}/{metadata['episode']}.mp3"
        self.s3.upload_file(str(audio_file), self.bucket, key)
        
        url = f"https://{self.bucket}.s3.amazonaws.com/{key}"
        size = audio_file.stat().st_size
        
        return {
            "url": url,
            "length": size,
            "type": "audio/mpeg"
        }
```

## Adapter Selection Logic

**Configuration:** `STORAGE_ADAPTER` environment variable

```python
# scripts/upload_archive.py

def get_storage_adapter():
    adapter_type = os.getenv("STORAGE_ADAPTER", "archive")
    
    if adapter_type == "archive":
        from adapters.archive import ArchiveAdapter
        return ArchiveAdapter()
    elif adapter_type == "spotify":
        from adapters.spotify import SpotifyAdapter
        return SpotifyAdapter()
    elif adapter_type == "custom":
        from adapters.custom import CustomAdapter
        return CustomAdapter()
    else:
        raise ValueError(f"Unknown storage adapter: {adapter_type}")

# Usage
adapter = get_storage_adapter()
result = adapter.upload(audio_file, episode_metadata)
```

## RSS Feed Generation

### Process

1. **Scan episodes** - Read all `meta.yaml` files
2. **Filter published** - Only include episodes with `status: live`
3. **Sort** - By release date (newest first)
4. **Generate XML** - RSS 2.0 + Podcast namespace
5. **Validate** - Ensure feed is valid
6. **Write** - Output to `docs/podcast.xml`
7. **Commit** - GitHub Actions commits to repo
8. **Deploy** - GitHub Pages auto-publishes

### RSS Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>PR-CYBR Podcast</title>
    <link>https://pr-cybr.github.io/PR-CYBR-P0D</link>
    <language>en</language>
    <description>...</description>
    
    <atom:link href="https://pr-cybr.github.io/PR-CYBR-P0D/podcast.xml" 
               rel="self" type="application/rss+xml"/>
    
    <itunes:image href="https://pr-cybr.github.io/PR-CYBR-P0D/assets/logo.png"/>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:author>PR-CYBR Team</itunes:author>
    
    <!-- Episodes -->
    <item>
      <title>Introduction to Cybersecurity</title>
      <description>...</description>
      <pubDate>Mon, 15 Jan 2024 06:00:00 GMT</pubDate>
      <guid isPermaLink="false">P0D-S01-E001-AXIS-CIPHER</guid>
      
      <enclosure url="https://archive.org/download/pr-cybr-s01-e001/episode.mp3" 
                 length="65432100" 
                 type="audio/mpeg"/>
      
      <itunes:duration>45:30</itunes:duration>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:season>1</itunes:season>
      <itunes:episode>1</itunes:episode>
    </item>
    
    <!-- More episodes... -->
  </channel>
</rss>
```

## GitHub Pages Setup

### Enable GitHub Pages

1. **Repository Settings** → **Pages**
2. **Source:** Deploy from branch
3. **Branch:** `main` (or your default branch)
4. **Folder:** `/docs`
5. **Save**

Pages URL: `https://pr-cybr.github.io/PR-CYBR-P0D`

### Custom Domain (Optional)

1. Add `CNAME` file to `/docs/`:
   ```
   podcast.pr-cybr.com
   ```

2. Configure DNS:
   ```
   CNAME podcast.pr-cybr.com -> pr-cybr.github.io
   ```

3. Enable HTTPS in GitHub Pages settings

## Distribution Workflow

### Complete Flow

```
1. Episode ready for publishing
   ↓
2. go-live.yml workflow triggered
   ↓
3. Check: release_date <= now?
   ↓
4. Upload audio to storage (via adapter)
   ↓ (Returns: URL, length, type)
5. Update meta.yaml with media info
   ↓
6. Run generate_rss.py
   ↓
7. Write docs/podcast.xml
   ↓
8. Commit changes
   ↓
9. GitHub Pages auto-deploys
   ↓
10. RSS feed live at public URL
```

### Manual Publishing

```bash
# 1. Upload episode
python scripts/upload_archive.py --season 1 --episode 1

# 2. Update RSS
python scripts/generate_rss.py

# 3. Commit
git add episodes/season-01/ep01/meta.yaml docs/podcast.xml
git commit -m "feat: publish S01E01"
git push

# 4. Wait for Pages deployment (~1 minute)
```

## Submit to Podcast Directories

Once RSS feed is live, submit to directories:

### Apple Podcasts

1. Go to [Podcasts Connect](https://podcastsconnect.apple.com/)
2. Click "+"
3. Enter feed URL: `https://pr-cybr.github.io/PR-CYBR-P0D/podcast.xml`
4. Validate and submit

### Spotify

1. Go to [Spotify for Podcasters](https://podcasters.spotify.com/)
2. "Add your podcast"
3. Enter feed URL
4. Claim and verify

### Google Podcasts

1. Go to [Google Podcasts Manager](https://podcastsmanager.google.com/)
2. Add feed URL
3. Verify ownership

### Other Directories

- Pocket Casts
- Overcast
- Castro
- Podcast Addict
- (Most auto-discover from Apple)

## Cost Analysis

### Internet Archive (Default)

| Item | Cost |
|------|------|
| Storage | Free |
| Bandwidth | Free |
| Total | **$0/month** |

### Spotify for Podcasters

| Item | Cost |
|------|------|
| Hosting | Free |
| Distribution | Free |
| Analytics | Included |
| Total | **$0/month** |

**Note:** Free but platform-dependent

### AWS S3 + CloudFront (Custom)

| Item | Cost (est.) |
|------|-------------|
| S3 Storage | $0.023/GB/month |
| CloudFront | $0.085/GB (first 10TB) |
| Total (100 episodes, 1000 downloads/month) | **~$10/month** |

### Comparison

| Feature | Archive.org | Spotify | Custom S3 |
|---------|-------------|---------|-----------|
| Cost | Free | Free | ~$10/mo |
| Control | Full | Limited | Full |
| Permanence | Forever | Platform-dependent | Your choice |
| Analytics | Basic | Professional | Custom |
| Effort | Low | Low | Medium |

**Recommendation:** Start with Archive.org, move to custom if growth requires it.

## Monitoring & Analytics

### RSS Feed Validation

Use these tools to validate your feed:

- [Cast Feed Validator](https://castfeedvalidator.com/)
- [Podbase Feed Validator](https://podba.se/validate/)
- [iTunes Feed Validator](https://podcastsconnect.apple.com/)

### Download Statistics

**Archive.org:**
- Dashboard: https://archive.org/details/{identifier}
- Shows downloads and views
- Basic geographic data

**Custom Analytics:**
- Use CloudFront logs
- Parse nginx logs
- Third-party services (Podtrac, Chartable)

### RSS Subscribers

Track subscriber counts:
- Apple Podcasts Connect
- Spotify for Podcasters
- Google Podcasts Manager

## Troubleshooting

### RSS Not Updating

1. Check GitHub Pages deployment status
2. Verify `podcast.xml` committed to repo
3. Clear CDN cache (if using)
4. Test with `curl https://pr-cybr.github.io/PR-CYBR-P0D/podcast.xml`

### Archive.org Upload Fails

1. Verify credentials in secrets
2. Check identifier not already taken
3. Ensure file is valid MP3
4. Check Archive.org status page
5. Try with smaller test file

### Feed Not Appearing in Directories

1. Validate feed with validators
2. Check feed is publicly accessible
3. Verify all required iTunes tags present
4. Wait 24-48 hours for indexing
5. Re-submit if necessary

## Future Enhancements

- [ ] CDN integration for faster global delivery
- [ ] Automated transcoding (multiple bitrates)
- [ ] Chapter markers in RSS
- [ ] Transcript XML in feed
- [ ] Multiple audio formats (AAC, Opus)
- [ ] Video podcast support
- [ ] Dynamic ad insertion
- [ ] Geographic restrictions (if needed)
- [ ] Download analytics dashboard

## References

- [Internet Archive S3 API](https://archive.org/services/docs/api/ias3.html)
- [RSS 2.0 Specification](https://www.rssboard.org/rss-specification)
- [Podcast Namespace](https://github.com/Podcastindex-org/podcast-namespace)
- [Apple Podcasts Requirements](https://help.apple.com/itc/podcasts_connect/)
- [Spotify Podcast Specs](https://support.spotify.com/us/podcasters/article/podcast-delivery-specification/)

---

**Last Updated:** 2025-10-27  
**Version:** 1.0
