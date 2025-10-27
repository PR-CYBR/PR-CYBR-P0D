# Retrofit Plan: Autonomous Podcast Architecture

**Repository:** PR-CYBR/PR-CYBR-P0D  
**Date:** 2025-10-27  
**Status:** Phase 0 - Audit Complete

## Executive Summary

This plan outlines the retrofit of PR-CYBR-P0D from its current state (basic Notion sync + retrofit automation) to a production-ready autonomous podcast architecture with event-driven workflows, pluggable distribution, and full replication support.

**Current State:** Basic episode sync, some retrofit automation, limited documentation  
**Target State:** Full production architecture with n8n orchestration, self-hosted RSS, Archive.org distribution, NotebookLM integration, and 10-minute replication capability

## Gap Analysis

### ✅ Already Implemented

| Component | Status | Notes |
|-----------|--------|-------|
| Basic Notion sync | ✅ Complete | `scripts/sync_notion.py` working |
| GitHub Actions workflows | ✅ Partial | sync-notion-episodes.yml, retrofit-episodes.yml exist |
| Python environment | ✅ Complete | requirements.txt with dependencies |
| Basic documentation | ✅ Partial | README, SETUP, QUICKSTART exist but need updates |
| Episode metadata | ✅ Partial | JSON metadata exists, needs YAML migration |
| Code names & schedule | ✅ Complete | Scripts exist for generation |
| Google Drive integration | ✅ Partial | google_drive_utils.py exists |

### ❌ Missing / Needs Retrofit

| Component | Gap | Priority |
|-----------|-----|----------|
| Episode directory structure | No season-XX/epXX/ hierarchy | HIGH |
| meta.yaml schema | Using JSON, needs YAML | HIGH |
| .env.example | Missing | HIGH |
| CODEOWNERS, SECURITY.md | Missing | HIGH |
| Issue/PR templates | Missing | MEDIUM |
| docs/ architecture docs | Missing | HIGH |
| verify-env-vars workflow | Missing | HIGH |
| Whisper transcription | Missing | HIGH |
| Show notes generation | Missing | HIGH |
| Archive.org upload | Missing | CRITICAL |
| RSS feed generation | Missing | CRITICAL |
| GitHub Pages RSS hosting | Missing | CRITICAL |
| Pre-release workflow | Missing | HIGH |
| Go-live workflow | Missing | CRITICAL |
| Post-campaign workflow | Missing | MEDIUM |
| Recap generation | Missing | MEDIUM |
| n8n workflow stubs | Missing | HIGH |
| NotebookLM guide | Missing | MEDIUM |
| Replication documentation | Incomplete | HIGH |

## Detailed Changes by Phase

---

## Phase 0: Audit (CURRENT)

**Branch:** `plan/retrofit-arch`  
**PR:** "plan: retrofit to autonomous podcast architecture"

### Deliverables
- [x] PLAN.md (this document)

**Files Created:**
- `PLAN.md`

---

## Phase 1: Scaffolding & Docs

**Branch:** `feat/scaffold-arch`  
**PR:** "feat: add governance, docs, and environment scaffolding"

### Files to Create

| File | Purpose |
|------|---------|
| `.env.example` | Template for all required environment variables |
| `CODEOWNERS` | Define code ownership for automated reviews |
| `SECURITY.md` | Security policy and vulnerability reporting |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Bug report template |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Feature request template |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR template with checklist |
| `docs/notion-schema.md` | Notion database schema documentation |
| `docs/n8n-webhooks.md` | n8n webhook integration guide |
| `docs/storage-distribution.md` | Storage and distribution architecture |
| `docs/notebooklm-guide.md` | NotebookLM setup and usage |
| `hosts/season-01-prompt.txt` | NotebookLM Audio Overview prompt stub |
| `.github/workflows/verify-env-vars.yml` | Environment variable validation workflow |

### Files to Update

| File | Changes |
|------|---------|
| `README.md` | Add architecture overview, badges, link to new docs |
| `QUICKSTART.md` | Update with new setup flow |
| `.gitignore` | Add patterns for local env files, audio binaries |

### Environment Variables (.env.example)

```bash
# Notion Integration
NOTION_TOKEN=secret_xxxxx
NOTION_EPISODES_DB_ID=xxxxx

# Internet Archive
ARCHIVE_ACCESS_KEY=xxxxx
ARCHIVE_SECRET_KEY=xxxxx
ARCHIVE_IDENTIFIER_PREFIX=pr-cybr-pod

# RSS Feed
FEED_TITLE="PR-CYBR Podcast"
FEED_AUTHOR="PR-CYBR Team"
FEED_BASE_URL=https://pr-cybr.github.io/PR-CYBR-P0D
FEED_IMAGE_URL=https://pr-cybr.github.io/PR-CYBR-P0D/assets/podcast-logo.png

# Optional: AI/LLM
OPENAI_API_KEY=sk-xxxxx

# Optional: Social Media
SOCIAL_TWITTER_TOKEN=xxxxx
SOCIAL_LINKEDIN_TOKEN=xxxxx

# n8n Webhooks
N8N_PRE_URL=https://n8n.example.com/webhook/pre-campaign
N8N_LIVE_URL=https://n8n.example.com/webhook/go-live
N8N_POST_URL=https://n8n.example.com/webhook/post-campaign
```

**Definition of Done:**
- All governance files created
- Documentation structure complete
- verify-env-vars.yml passes with placeholder values
- Markdown lints pass
- README updated with architecture overview

---

## Phase 2: Data & Episode Schema

**Branch:** `feat/episode-schema`  
**PR:** "feat: implement season/episode directory structure and meta.yaml schema"

### Directory Structure Changes

**Current:**
```
episodes/
  episode-001-title.mp3
  episode-001-metadata.json
  prompts/
  release-schedule.txt
  episode-code-names.json
```

**Target:**
```
episodes/
  season-01/
    ep01/
      meta.yaml
      transcript.txt
      shownotes.md
      assets/
  season-02/
    ep01/
      meta.yaml
      ...
  prompts/           # Keep for backwards compat
  release-schedule.txt
  episode-code-names.json
```

### meta.yaml Schema

```yaml
# Episode Metadata
title: "Episode Title"
codename: "P0D-S01-E001-AXIS-CIPHER"
season: 1
episode: 1

# Release
release_date: "2024-01-15T06:00:00Z"
status: "live"  # draft, pre-release, live, archived

# Media
audio_url: "https://archive.org/download/pr-cybr-s01e01/audio.mp3"
duration: "45:30"
file_size: 65432100
file_type: "audio/mpeg"

# Content
description: "Episode description for RSS feed"
keywords: ["cybersecurity", "podcast"]

# Links
notion_url: "https://notion.so/page/..."
script_doc_url: "https://docs.google.com/document/..."
show_notes_url: "https://docs.google.com/document/..."

# Production
transcribed: true
show_notes_generated: true
published_to_rss: true
archived: false
```

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/new_episode.py` | Scaffold new episode directories and meta.yaml |
| `scripts/migrate_episodes.py` | One-time migration of JSON → YAML |
| `episodes/season-01/ep01/meta.yaml` | Sample episode for testing |

### Files to Update

| File | Changes |
|------|---------|
| `scripts/notion_sync.py` | Read/write meta.yaml instead of JSON, support season/episode structure |
| `.github/workflows/sync-notion.yml` | Rename from sync-notion-episodes.yml, update paths |

### Migration Strategy

1. Keep existing JSON files for backwards compatibility
2. New episodes use YAML + season/episode structure
3. Provide migration script for existing episodes (optional, run manually)
4. Update sync script to handle both formats during transition

**Definition of Done:**
- Season/episode directory structure implemented
- meta.yaml schema documented and validated
- new_episode.py creates proper structure
- notion_sync.py reads/writes YAML
- Sample episode exists in season-01/ep01/
- sync-notion.yml workflow updated and passing

---

## Phase 3: Pre-Campaign Automation

**Branch:** `feat/pre-campaign`  
**PR:** "feat: add pre-campaign automation with transcription and show notes"

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/transcribe_whisper.py` | OpenAI Whisper transcription |
| `scripts/generate_shownotes.py` | Template-based show notes with optional LLM |
| `.github/workflows/pre-release.yml` | Pre-campaign automation workflow |

### transcribe_whisper.py

**Features:**
- Accept audio file path from meta.yaml
- Use OpenAI Whisper API or local model
- Output to `transcript.txt`
- Update meta.yaml with `transcribed: true`
- CLI: `python scripts/transcribe_whisper.py --season 1 --episode 1`

**Dependencies:**
- `openai` (for API)
- `ffmpeg` (for audio processing)

### generate_shownotes.py

**Features:**
- Template-first approach (use template from retrofitting/templates/)
- Optional LLM enhancement if `OPENAI_API_KEY` set
- Read transcript.txt, output shownotes.md
- Include timestamps, key points, links
- Update meta.yaml with `show_notes_generated: true`

**Template Variables:**
- `{title}`, `{release_date}`, `{description}`, `{transcript}`

### pre-release.yml Workflow

**Triggers:**
- `repository_dispatch` (from n8n): `event_type: "pre-campaign"`
- `workflow_dispatch` (manual)

**Steps:**
1. Checkout repo
2. Setup Python + ffmpeg
3. Check if transcript exists (skip if present unless `--force`)
4. Run transcribe_whisper.py if raw audio available
5. Run generate_shownotes.py
6. Commit changes to episode folder
7. Post status comment/update Notion

**Payload Example:**
```json
{
  "event_type": "pre-campaign",
  "client_payload": {
    "season": 1,
    "episode": 1,
    "force": false
  }
}
```

**Definition of Done:**
- transcribe_whisper.py works with sample audio
- generate_shownotes.py creates valid shownotes.md
- pre-release.yml workflow passes in CI
- Workflow can be triggered via repository_dispatch
- Generated files committed to episode directory

---

## Phase 4: Live (Publish) Automation

**Branch:** `feat/live-publish`  
**PR:** "feat: add live publishing with Archive.org and RSS generation"

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/upload_archive.py` | Upload to Internet Archive S3 |
| `scripts/generate_rss.py` | Generate podcast RSS feed |
| `.github/workflows/go-live.yml` | Publishing workflow |
| `docs/podcast.xml` | RSS feed output (generated) |

### upload_archive.py

**Features:**
- Internet Archive S3 API integration
- Upload MP3 from local path or URL
- Set metadata (title, creator, description, date)
- Return canonical media URL, file length, MIME type
- Support for pluggable adapter pattern (future: Spotify, custom)
- CLI: `python scripts/upload_archive.py --season 1 --episode 1`

**Configuration:**
```python
STORAGE_ADAPTER = os.getenv("STORAGE_ADAPTER", "archive")  # archive | spotify | custom

if STORAGE_ADAPTER == "archive":
    # Use Internet Archive
elif STORAGE_ADAPTER == "spotify":
    # Use Spotify for Podcasters
elif STORAGE_ADAPTER == "custom":
    # Use custom endpoint
```

**Dependencies:**
- `internetarchive` or `boto3` (for S3 API)
- Archive.org account and S3 keys

### generate_rss.py

**Features:**
- Read all meta.yaml files from episodes/season-XX/epXX/
- Generate valid RSS 2.0 + Podcast namespace XML
- Proper `<enclosure>` with length, type, URL
- Stable `<guid>` (use episode codename)
- RFC-822 formatted dates
- `<itunes:duration>` tag
- Categories and keywords
- Output to `docs/podcast.xml`

**RSS Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>PR-CYBR Podcast</title>
    <link>https://pr-cybr.github.io/PR-CYBR-P0D</link>
    <description>...</description>
    <itunes:image href="..." />
    <item>
      <title>Episode 1: Title</title>
      <description>...</description>
      <enclosure url="https://archive.org/..." length="65432100" type="audio/mpeg"/>
      <guid isPermaLink="false">P0D-S01-E001-AXIS-CIPHER</guid>
      <pubDate>Mon, 15 Jan 2024 06:00:00 GMT</pubDate>
      <itunes:duration>45:30</itunes:duration>
    </item>
  </channel>
</rss>
```

### go-live.yml Workflow

**Triggers:**
- Scheduled cron at release times
- `repository_dispatch` from n8n: `event_type: "go-live"`
- `workflow_dispatch` (manual)

**Steps:**
1. Checkout repo
2. Setup Python
3. Check for episodes with `release_date <= now` AND `status = "pre-release"`
4. For each episode:
   - Upload to Archive.org (or configured adapter)
   - Update meta.yaml with audio_url, file_size, file_type
   - Mark `published_to_rss: true`, `status: "live"`
5. Run generate_rss.py
6. Commit changes
7. Verify GitHub Pages is enabled (instruction in PR if not)

**Definition of Done:**
- upload_archive.py successfully uploads to Archive.org
- generate_rss.py creates valid RSS 2.0 feed
- Feed validates with feedparser
- go-live.yml workflow passes
- docs/podcast.xml published via GitHub Pages
- Absolute URLs in feed

---

## Phase 5: Post-Campaign

**Branch:** `feat/post-campaign`  
**PR:** "feat: add post-campaign automation with recap generation"

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/generate_recap.py` | Generate episode recap and Q&A |
| `.github/workflows/post-campaign.yml` | Post-campaign workflow |

### generate_recap.py

**Features:**
- Read transcript.txt
- Generate recap article (summary, key takeaways)
- Create 5 Q&A flashcards with quotes from transcript
- Output to `episodes/season-XX/epXX/recap.md`
- Use LLM if available, otherwise template with TODO markers
- Update meta.yaml with archival status

**Recap Structure:**
```markdown
# Episode Recap: {title}

## Summary
[3-5 paragraph summary]

## Key Takeaways
- Point 1
- Point 2
- Point 3

## Discussion Questions

### Q1: [Question]
**A:** [Answer with quote from transcript]

[... 5 questions total]

## Resources & Links
- [Link to show notes]
- [Link to audio]
```

### post-campaign.yml Workflow

**Triggers:**
- Scheduled (X days after release)
- `repository_dispatch` from n8n: `event_type: "post-campaign"`
- `workflow_dispatch` (manual)

**Steps:**
1. Checkout repo
2. Setup Python
3. Find episodes where `status = "live"` AND `days_since_release > threshold`
4. For each episode:
   - Run generate_recap.py
   - Update indices (if any)
   - Mark `archived: true`
5. Commit changes

**Definition of Done:**
- generate_recap.py creates recap.md
- Recap includes citations from transcript
- post-campaign.yml workflow passes
- Clear TODO markers when LLM key absent

---

## Phase 6: n8n Integration Stubs

**Branch:** `feat/n8n-stubs`  
**PR:** "feat: add n8n workflow stubs and webhook documentation"

### Files to Create

| File | Purpose |
|------|---------|
| `workflows/n8n/pre-campaign.json` | n8n workflow export for pre-campaign |
| `workflows/n8n/live.json` | n8n workflow export for go-live |
| `workflows/n8n/post.json` | n8n workflow export for post-campaign |
| `workflows/n8n/README.md` | Import instructions |

### n8n Workflow Structure (All Workflows)

**Nodes:**
1. **Notion Trigger** - Watch for button press or status change
2. **Notion Lookup** - Get episode details
3. **Function** - Build GitHub dispatch payload
4. **HTTP Request** - POST to GitHub API
5. **Notion Update** - Update status fields

**GitHub Dispatch Payload:**
```json
{
  "event_type": "pre-campaign",  // or "go-live", "post-campaign"
  "client_payload": {
    "season": 1,
    "episode": 1,
    "notion_page_id": "xxxxx",
    "force": false
  }
}
```

### Files to Update

| File | Changes |
|------|---------|
| `docs/n8n-webhooks.md` | Add curl examples, payload specs, setup instructions |

### Webhook Documentation

**curl Example:**
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{"event_type":"pre-campaign","client_payload":{"season":1,"episode":1}}'
```

**Definition of Done:**
- 3 n8n workflow JSON exports created
- Each has placeholder values
- README explains import process
- docs/n8n-webhooks.md updated with curl examples
- Manual test: curl triggers workflow

---

## Implementation Order

### Draft PRs (Sequential Creation)

1. **Phase 0** - Create PLAN.md ✅
2. **Phase 1** - Scaffolding & Docs
3. **Phase 2** - Episode Schema
4. **Phase 3** - Pre-Campaign
5. **Phase 4** - Live Publishing (CRITICAL PATH)
6. **Phase 5** - Post-Campaign
7. **Phase 6** - n8n Stubs

### Dependencies

```
Phase 1 (scaffolding)
  ↓
Phase 2 (schema) ← Required for all automation
  ↓
Phase 3 (pre) ────┐
Phase 4 (live) ←──┼─ Can develop in parallel
Phase 5 (post) ←──┘
  ↓
Phase 6 (n8n) ← Requires all workflows complete
```

---

## Quality Gates (All PRs)

### CI Checks
- [ ] `verify-env-vars.yml` - Prints missing vars, doesn't fail
- [ ] `markdownlint` - All docs pass
- [ ] `yamllint` - All YAML valid
- [ ] `pytest` - Unit tests for Python scripts (where applicable)
- [ ] RSS validation - Feed parses correctly

### PR Checklist Template
```markdown
- [ ] Docs updated
- [ ] CI green
- [ ] Backwards compatible
- [ ] No secrets committed
- [ ] Tests added/updated
```

---

## Migration Notes

### Backwards Compatibility

**Episode Files:**
- Keep existing JSON metadata for old episodes
- New episodes use YAML + season structure
- Sync script handles both formats

**Audio Storage:**
- Existing MP3s can remain in flat structure
- Move to season folders gradually
- RSS includes all episodes regardless of location

**Workflows:**
- Existing workflows continue to work
- New workflows are additive
- No breaking changes to API contracts

### Rollout Strategy

1. **Phase 1-2:** Non-breaking (new files only)
2. **Phase 3:** Optional (doesn't affect existing episodes)
3. **Phase 4:** Critical - affects RSS (test thoroughly)
4. **Phase 5-6:** Optional enhancements

---

## Testing Strategy

### Unit Tests
- `test_generate_rss.py` - RSS XML validation
- `test_meta_yaml.py` - YAML schema validation
- `test_upload_archive.py` - Mock Archive.org API

### Integration Tests
- End-to-end episode creation flow
- Notion → GitHub sync roundtrip
- RSS feed with real episode data

### Manual Testing
- Trigger each workflow via workflow_dispatch
- Validate RSS in podcast player
- Test Archive.org upload with real credentials
- Import n8n workflows

---

## Success Criteria

### Milestone: v0.1 – Autonomous Retrofit

**Essential:**
- [x] PLAN.md created
- [ ] All 6 phases complete (draft PRs)
- [ ] RSS feed live on GitHub Pages
- [ ] At least 1 episode published via automation
- [ ] QUICKSTART enables replication in ≤10 minutes
- [ ] No secrets in repository

**Desirable:**
- [ ] NotebookLM guide complete
- [ ] All workflows tested with n8n
- [ ] Migration script for existing episodes
- [ ] Comprehensive test coverage

---

## Future Enhancements (Post v0.1)

- Multiple distribution adapters (Spotify, Apple Podcasts, etc.)
- Social media auto-posting
- Analytics integration
- Multi-language support
- Advanced AI show notes (chapter markers, summaries)
- Video podcast support
- Automated episode artwork generation

---

## Support & References

**Documentation:**
- [Notion API](https://developers.notion.com/)
- [Internet Archive S3](https://archive.org/services/docs/api/ias3.html)
- [RSS 2.0 Spec](https://www.rssboard.org/rss-specification)
- [Podcast Namespace](https://github.com/Podcastindex-org/podcast-namespace)
- [GitHub Actions](https://docs.github.com/en/actions)
- [n8n Documentation](https://docs.n8n.io/)

**Contact:**
- GitHub Issues: https://github.com/PR-CYBR/PR-CYBR-P0D/issues
- Discussions: https://github.com/PR-CYBR/PR-CYBR-P0D/discussions

---

**Last Updated:** 2025-10-27  
**Next Review:** After Phase 1 completion
