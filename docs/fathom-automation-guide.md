# Fathom Automation System Guide

## Overview

The Fathom Automation System automatically processes meeting transcripts from Zoom/Fathom AI and converts them into actionable GitHub issues across agent repositories.

## Architecture Flow

```
┌─────────────────┐
│  Zoom Meeting   │
└────────┬────────┘
         │ (recorded)
         ▼
┌─────────────────┐
│   Fathom AI     │ Transcribes & analyzes
└────────┬────────┘
         │ (webhook: fathom_meeting_ended)
         ▼
┌──────────────────────────────────────┐
│  fathom-ingest.yml Workflow          │
│  • Saves raw transcript              │
│  • Calls extract_tasks.py            │
│  • Generates tasks.json              │
└────────┬─────────────────────────────┘
         │ (repository_dispatch: create_agent_tasks)
         ▼
┌──────────────────────────────────────┐
│  create-agent-issues.yml Workflow    │
│  • Reads tasks.json                  │
│  • Calls create_issues.py            │
│  • Creates issues in agent repos     │
└────────┬─────────────────────────────┘
         │ (issues with label: automation/codex)
         ▼
┌──────────────────────────────────────┐
│  Agent Repos: codex-autopatch.yml    │
│  • Detects labeled issue             │
│  • Runs Codex AI container           │
│  • Makes automated code changes      │
│  • Creates pull request              │
└────────┬─────────────────────────────┘
         │ (on PR merge to main)
         ▼
┌──────────────────────────────────────┐
│  knowledge-sync.yml Workflow         │
│  • Creates GitHub Discussion         │
│  • Creates public Gist               │
│  • Syncs to Notion database          │
└──────────────────────────────────────┘
```

## Components

### 1. Fathom Webhook Ingestion

**File:** `.github/workflows/fathom-ingest.yml`

**Trigger:**
- `repository_dispatch` with event type `fathom_meeting_ended`
- Manual trigger via `workflow_dispatch`

**Payload Example:**
```json
{
  "event_type": "fathom_meeting_ended",
  "client_payload": {
    "meeting_id": "zoom-2025-01-15-123456",
    "transcript": "Full meeting transcript text...",
    "timestamp": "2025-01-15T10:00:00Z",
    "participants": ["alice@example.com", "bob@example.com"],
    "duration": "45:30"
  }
}
```

**Actions:**
1. Saves `raw.json` to `data/meetings/<meeting_id>/`
2. Runs `scripts/extract_tasks.py` to process transcript
3. Generates `tasks.json` with extracted tasks
4. Commits files to repository
5. Dispatches `create_agent_tasks` event

### 2. Task Extraction

**File:** `scripts/extract_tasks.py`

**Purpose:** Extract actionable tasks from meeting transcripts using AI/LLM

**Usage:**
```bash
python scripts/extract_tasks.py \
  --input data/meetings/meeting-001/raw.json \
  --output data/meetings/meeting-001/tasks.json \
  --verbose
```

**Environment Variables:**
- `OPENAI_API_KEY` (optional): If not set, uses stub extraction

**Output Schema:**
```json
{
  "meeting_id": "meeting-001",
  "summary": "Meeting summary text",
  "tasks": [
    {
      "task_id": "meeting-001_TASK_001",
      "agent": "A-01",
      "repo": "PR-CYBR-AGENT-01",
      "title": "Task title",
      "description": "Detailed description",
      "priority": "high|medium|low",
      "type": "bug|enhancement|documentation",
      "labels": ["automation/codex", "meeting/meeting-001"],
      "explicit": true
    }
  ],
  "extracted_at": "2025-01-15T10:30:00Z",
  "version": "1.0"
}
```

### 3. Issue Creation

**File:** `scripts/create_issues.py`

**Purpose:** Create or update GitHub issues in agent repositories

**Usage:**
```bash
export GITHUB_TOKEN="ghp_..."

# Create issues
python scripts/create_issues.py \
  --input data/meetings/meeting-001/tasks.json \
  --config config/agents.yaml \
  --verbose

# Dry run (no changes)
python scripts/create_issues.py \
  --input data/meetings/meeting-001/tasks.json \
  --dry-run
```

**Features:**
- **Idempotency**: Searches for existing issues by task_id before creating
- **Agent Mapping**: Uses `config/agents.yaml` to route tasks to correct repos
- **Label Management**: Automatically applies agent, priority, and meeting labels
- **Error Handling**: Continues processing if individual tasks fail

### 4. Agent Configuration

**File:** `config/agents.yaml`

**Content:**
```yaml
agents:
  A-01: PR-CYBR-AGENT-01
  A-02: PR-CYBR-AGENT-02
  # ... A-03 through A-12
  
organization: PR-CYBR
```

### 5. Codex Autopatch Template

**File:** `.github/workflows/codex-autopatch-template.yml`

**Purpose:** Reusable workflow for agent repos to automate code fixes

**Usage in Agent Repos:**

Create `.github/workflows/codex-autopatch.yml`:
```yaml
name: Codex Autopatch

on:
  issues:
    types: [opened, labeled]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  check-label:
    runs-on: ubuntu-latest
    outputs:
      should_run: ${{ steps.check.outputs.should_run }}
    steps:
      - name: Check for automation/codex label
        id: check
        run: |
          LABELS='${{ toJson(github.event.issue.labels) }}'
          if echo "$LABELS" | jq -e '.[] | select(.name == "automation/codex")' > /dev/null; then
            echo "should_run=true" >> $GITHUB_OUTPUT
          else
            echo "should_run=false" >> $GITHUB_OUTPUT
          fi

  autopatch:
    needs: check-label
    if: needs.check-label.outputs.should_run == 'true'
    uses: PR-CYBR/PR-CYBR-P0D/.github/workflows/codex-autopatch-template.yml@main
    with:
      issue_number: ${{ github.event.issue.number }}
      issue_title: ${{ github.event.issue.title }}
      issue_body: ${{ github.event.issue.body }}
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**What It Does:**
1. Creates feature branch: `codex/issue-<num>-<task-id>`
2. Runs Codex AI container to make code changes
3. Runs tests (if available)
4. Commits changes and creates PR
5. Comments on original issue with status

### 6. Knowledge Sync

**File:** `.github/workflows/knowledge-sync.yml`

**Trigger:**
- Pull request merged to `main` branch
- Manual trigger via `workflow_dispatch`

**Actions:**
1. Creates GitHub Discussion with work summary
2. Creates public Gist with detailed information
3. Syncs to Notion database using `scripts/notion_sync.py`

**Notion Sync Script:**
```bash
python scripts/notion_sync.py \
  --agent A-01 \
  --repo PR-CYBR-AGENT-01 \
  --issue 123 \
  --pr 456 \
  --meeting-date 2025-01-15 \
  --summary "Implemented feature X"
```

## Testing

### Test Fathom Webhook

**Using curl:**
```bash
GITHUB_TOKEN="your_github_token"

curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -d '{
    "event_type": "fathom_meeting_ended",
    "client_payload": {
      "meeting_id": "test-meeting-001",
      "transcript": "TODO: Update documentation\nACTION ITEM: Fix bug\nNEED TO implement feature",
      "timestamp": "2025-01-15T10:00:00Z"
    }
  }'
```

**Using GitHub CLI:**
```bash
gh api repos/PR-CYBR/PR-CYBR-P0D/dispatches \
  -f event_type=fathom_meeting_ended \
  -f client_payload[meeting_id]=test-meeting-001 \
  -f client_payload[transcript]="TODO: Test task\nACTION: Another task"
```

### Test Issue Creation

```bash
# 1. Create test tasks file
cat > /tmp/test-tasks.json << 'EOF'
{
  "meeting_id": "test-001",
  "summary": "Test meeting",
  "tasks": [
    {
      "task_id": "test-001_TASK_001",
      "agent": "A-01",
      "repo": "PR-CYBR-AGENT-01",
      "title": "Test task",
      "description": "This is a test task",
      "priority": "medium",
      "type": "enhancement",
      "labels": ["automation/codex", "meeting/test-001"],
      "explicit": false
    }
  ]
}
EOF

# 2. Test in dry-run mode
python scripts/create_issues.py \
  --input /tmp/test-tasks.json \
  --dry-run

# 3. Create actual issues (requires GITHUB_TOKEN)
export GITHUB_TOKEN="your_token"
python scripts/create_issues.py \
  --input /tmp/test-tasks.json
```

### Manual Workflow Triggers

**Via GitHub UI:**
1. Go to Actions tab
2. Select workflow (e.g., "Fathom Meeting Ingest")
3. Click "Run workflow"
4. Fill in inputs
5. Click "Run workflow"

**Via GitHub CLI:**
```bash
# Trigger fathom-ingest
gh workflow run fathom-ingest.yml \
  -f meeting_id=test-001 \
  -f transcript="TODO: Test"

# Trigger create-agent-issues
gh workflow run create-agent-issues.yml \
  -f meeting_id=test-001

# Trigger knowledge-sync
gh workflow run knowledge-sync.yml \
  -f pr_number=123 \
  -f agent=A-01 \
  -f repo=PR-CYBR-AGENT-01 \
  -f issue_number=456 \
  -f meeting_date=2025-01-15 \
  -f summary="Completed task"
```

## Environment Setup

### Required Secrets

Configure these in GitHub Settings → Secrets and Variables → Actions:

**For PR-CYBR-P0D:**
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `OPENAI_API_KEY` - OpenAI API key for task extraction (optional)
- `NOTION_TOKEN` - Notion integration token (optional)
- `NOTION_DATABASE_ID` - Notion database ID (optional)

**For Agent Repositories:**
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Notion Database Schema

Create a Notion database with these properties:

| Property | Type | Description |
|----------|------|-------------|
| Task ID | Text | Deterministic UUID for idempotency |
| Title | Title | Task title |
| Agent | Select | Agent ID (A-01 to A-12) |
| Repository | Text | Repository name |
| Issue | Number | GitHub issue number |
| PR | Number | GitHub PR number |
| Meeting Date | Date | Meeting date |
| Summary | Text | Task summary |
| Issue URL | URL | Link to GitHub issue |
| PR URL | URL | Link to GitHub PR |
| Status | Select | Options: Complete, In Progress, etc. |

## Troubleshooting

### Workflow Not Triggering

**Problem:** Fathom webhook not triggering workflow

**Solutions:**
1. Check webhook is configured in Fathom settings
2. Verify webhook URL: `https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches`
3. Ensure webhook includes `event_type: fathom_meeting_ended`
4. Test with manual curl command

### Tasks Not Extracted

**Problem:** No tasks in tasks.json

**Solutions:**
1. Check transcript contains action keywords (TODO, ACTION ITEM, etc.)
2. Verify `OPENAI_API_KEY` is set if using LLM mode
3. Check logs for extraction errors
4. Test locally with sample transcript

### Issues Not Created

**Problem:** Issues not appearing in agent repos

**Solutions:**
1. Verify `GITHUB_TOKEN` has `repo` scope
2. Check agent mapping in `config/agents.yaml`
3. Verify repository exists: `PR-CYBR/PR-CYBR-AGENT-XX`
4. Check workflow logs for API errors
5. Test with `--dry-run` first

### Notion Sync Failing

**Problem:** Cannot sync to Notion

**Solutions:**
1. Verify `NOTION_TOKEN` is valid integration token
2. Check `NOTION_DATABASE_ID` is correct
3. Ensure Notion integration has access to database
4. Verify database schema matches expected properties
5. Check for API rate limiting

## Best Practices

1. **Testing**: Always test with manual triggers before setting up webhooks
2. **Dry Run**: Use `--dry-run` to preview changes before creating issues
3. **Monitoring**: Check workflow logs regularly for errors
4. **Idempotency**: Task IDs ensure re-running workflows won't create duplicates
5. **Labels**: Use consistent labeling for easy filtering and automation
6. **Documentation**: Keep agent mapping up to date as repos change

## Integration with Fathom

### Webhook Configuration

In Fathom settings:
1. Go to Integrations → Webhooks
2. Add webhook URL: `https://api.github.com/repos/PR-CYBR/PR-CYBR-P0D/dispatches`
3. Event type: Meeting Ended
4. Headers:
   - `Accept: application/vnd.github.v3+json`
   - `Authorization: token YOUR_GITHUB_TOKEN`
5. Payload template:
   ```json
   {
     "event_type": "fathom_meeting_ended",
     "client_payload": {
       "meeting_id": "{{meeting_id}}",
       "transcript": "{{transcript}}",
       "timestamp": "{{timestamp}}",
       "participants": {{participants}},
       "duration": "{{duration}}"
     }
   }
   ```

## Future Enhancements

- [ ] Add support for task prioritization based on urgency keywords
- [ ] Implement sentiment analysis for better task categorization
- [ ] Add automatic assignment of tasks based on expertise
- [ ] Create dashboard for tracking automation metrics
- [ ] Add support for multiple LLM providers (Claude, Gemini)
- [ ] Implement automatic PR review and merge for low-risk changes
- [ ] Add Slack/Discord notifications for task assignments
- [ ] Create weekly summary reports of automation activity
