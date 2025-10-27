# NotebookLM Integration Guide

This document explains how to use Google's NotebookLM for AI-powered podcast content generation in PR-CYBR-P0D.

## Overview

NotebookLM is Google's AI-powered research and note-taking tool that can generate Audio Overview podcasts from source documents. We integrate it into our production pipeline for AI-assisted episode creation.

## What is NotebookLM?

**NotebookLM** is a Google Labs product that:
- Analyzes uploaded documents (PDFs, Google Docs, websites)
- Answers questions about your content
- Generates summaries and insights
- **Creates Audio Overviews** - AI-generated podcast-style conversations (2-10 minutes)

**Audio Overview Feature:**
- Two AI hosts discuss your content
- Natural conversation format
- Engaging explanations of complex topics
- Customizable via prompt engineering

## Integration Architecture

```
Episode Planning (Notion)
  ↓
Prompt Input (5,000 chars max)
  ↓
Google Doc Creation (via API)
  ↓
NotebookLM Notebook (manual/API)
  ↓
Upload Doc to Notebook
  ↓
Generate Audio Overview
  ↓
Download Audio to Drive
  ↓
Sync to GitHub (Track-Cloud field)
  ↓
Continue Production Pipeline
```

## Setup

### Prerequisites

1. **Google Account** with NotebookLM access
2. **Google Drive** for document storage
3. **Google Docs** for scripts
4. **NotebookLM API key** (if using API automation)

### Per-Season Setup

Each season has its own NotebookLM notebook for consistency.

**Steps:**

1. **Create Notebook**
   - Go to [notebooklm.google.com](https://notebooklm.google.com)
   - Click "New Notebook"
   - Name: "PR-CYBR Podcast - Season 01"

2. **Add Season Context Document**
   - Upload `hosts/season-01-prompt.txt` as a source
   - This provides consistent persona/style across all episodes

3. **Configure Audio Overview Settings**
   - Voice style: Professional/Conversational
   - Length: Full (or customize per episode)
   - Emphasis: Technical accuracy + accessibility

4. **Save Notebook ID**
   - Note the Notebook ID from URL
   - Store in `NOTEBOOK_LM_SEASON_01_ID` (GitHub Secret)

## Workflow

### Method 1: Manual (Recommended for v0.1)

**Per Episode:**

1. **Create Script Doc**
   ```
   Title: S01E01 - Introduction to Cybersecurity
   Codename: P0D-S01-E001-AXIS-CIPHER
   
   [Episode content - 5,000 characters max]
   ```

2. **Upload to NotebookLM**
   - Open season notebook
   - Click "Add sources"
   - Select Google Doc
   - Choose your script doc

3. **Generate Audio Overview**
   - Click "Generate Audio Overview"
   - Wait 2-5 minutes for processing
   - Review generated audio

4. **Download & Upload**
   - Download MP3 from NotebookLM
   - Upload to Google Drive episode folder
   - Copy link to Notion "Track-Cloud" field

5. **Update Metadata**
   - Duration extracted from audio
   - Notion fields auto-updated via sync

### Method 2: API (Future Enhancement)

**Using NotebookLM API** (when available):

```python
# scripts/generate_notebooklm_audio.py
import notebooklm

client = notebooklm.Client(api_key=os.getenv("NOTEBOOK_LM_API_KEY"))

# Get or create notebook
notebook = client.get_notebook(notebook_id=SEASON_NOTEBOOK_ID)

# Upload document
source = notebook.add_source(
    type="google_doc",
    url=script_doc_url
)

# Generate audio
audio = notebook.generate_audio_overview(
    sources=[source],
    length="full",
    style="conversational"
)

# Download result
audio.download(output_path=f"episodes/season-01/ep01/audio-overview.mp3")
```

## Prompt Engineering

### Season Context Prompt

Located at: `hosts/season-01-prompt.txt`

**Purpose:** Define the AI hosts' personas and style for the entire season.

**Structure:**
```
# PR-CYBR Podcast Season 1: Cybersecurity Foundations

## Show Concept
[Brief description of season theme]

## Host Personas

### Host 1: [Name]
- Role: [Expert/Novice/etc.]
- Personality: [Traits]
- Background: [Context]

### Host 2: [Name]
- Role: [Different perspective]
- Personality: [Complementary traits]
- Background: [Context]

## Conversation Style
- Tone: [Professional but accessible]
- Pacing: [Conversational, not rushed]
- Technical Level: [Appropriate for audience]
- Use analogies and examples
- Ask clarifying questions
- Build on each other's points

## Topics to Cover (Season 1)
1. [Theme 1]
2. [Theme 2]
...

## Avoid
- Jargon without explanation
- Overly formal language
- Rapid-fire information dumps
- Condescending tone
```

**Character Limit:** 5,000 characters (NotebookLM limit)

### Episode Prompt

**Location:** Notion "Prompt-Input" field or `episodes/prompts/prompt_S01E001.txt`

**Template:**

```
Episode: [Title]
Code Name: [P0D-S##-E###-AXIS-SYMBOL]
Duration Target: 45 minutes

## Episode Goal
[What should listeners learn?]

## Key Concepts
1. [Concept 1]
2. [Concept 2]
3. [Concept 3]

## Discussion Points
- [Point 1 with context]
- [Point 2 with real-world example]
- [Point 3 with analogy]

## Story/Scenario (Optional)
[Narrative hook or case study]

## Practical Takeaways
- [Action item 1]
- [Action item 2]

## Additional Notes
[Any special instructions for this episode]
```

**Best Practices:**
- Be specific about learning objectives
- Include real-world examples
- Suggest analogies for complex topics
- Specify key terms to define
- Indicate target technical level
- Mention any prerequisite knowledge

## Audio Overview Output

### What You Get

**Generated Audio:**
- Format: MP3
- Length: 2-10 minutes (depends on input)
- Quality: High-quality synthesized voices
- Style: Two-host conversation

**Characteristics:**
- Natural conversational flow
- Turn-taking between hosts
- Clarifying questions
- Examples and analogies
- Summary and key takeaways

### Post-Processing (Optional)

After generating Audio Overview:

1. **Extend with Intro/Outro**
   ```bash
   ffmpeg -i intro.mp3 -i notebooklm-audio.mp3 -i outro.mp3 \
     -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1" \
     episode-final.mp3
   ```

2. **Add Music/Effects**
   - Background music (low volume)
   - Sound effects for transitions
   - Chapter markers

3. **Normalize Audio**
   ```bash
   ffmpeg -i episode.mp3 -af loudnorm final.mp3
   ```

## Integration with Retrofit Pipeline

### Automated Workflow

```
1. Episode Status → "In progress" (Notion)
   ↓
2. Retrofit workflow triggered
   ↓
3. Check for Prompt-Input field
   ↓
4. Create Google Doc with prompt
   ↓ (Manual step for now)
5. Upload to NotebookLM
   ↓
6. Generate Audio Overview
   ↓
7. Download and upload to Drive
   ↓
8. Update Track-Cloud field (Notion)
   ↓
9. Continue with transcription/show notes
```

### Semi-Automated (Current)

**What's Automated:**
- Google Doc creation
- Notion field updates
- Metadata extraction

**What's Manual:**
- Uploading doc to NotebookLM
- Generating audio
- Downloading result

**Future:** Full API automation when NotebookLM API is available.

## Google Drive Setup

### Folder Structure

```
PR-CYBR Podcast/
├── Season 01/
│   ├── Scripts/
│   │   ├── S01E01-script.gdoc
│   │   ├── S01E02-script.gdoc
│   │   └── ...
│   ├── Audio/
│   │   ├── S01E01-notebooklm.mp3
│   │   ├── S01E02-notebooklm.mp3
│   │   └── ...
│   └── Show Notes/
│       ├── S01E01-notes.gdoc
│       └── ...
├── Season 02/
└── ...
```

### Service Account Access

1. **Create Service Account**
   - Google Cloud Console → IAM → Service Accounts
   - Create new account
   - Generate JSON key

2. **Share Drive Folders**
   - Share each season folder with service account email
   - Permission: Editor

3. **Store Credentials**
   ```bash
   GOOGLE_DRIVE_SERVICE_ACCOUNT={"type":"service_account",...}
   PR_CYBR_P0D_DRIVE_FOLDER_ID=xxxxxxxxxxxxx
   ```

## Alternative: Manual Google Docs Export

If not using API automation:

1. **Write script** in Google Docs manually
2. **File → Download → Plain Text**
3. Copy to `episodes/prompts/prompt_S01E001.txt`
4. Continue with NotebookLM manual workflow

## Tips for Great Audio Overviews

### Content Preparation

1. **Clear Structure**
   - Introduction
   - 3-5 main points
   - Conclusion with takeaways

2. **Appropriate Length**
   - 1,500-3,000 words → ~5-10 min audio
   - Don't overload with information

3. **Examples & Analogies**
   - Include concrete examples
   - Use relatable analogies
   - Tell brief stories

4. **Discussion Prompts**
   - Add "Note to hosts:" callouts
   - Suggest questions to ask
   - Indicate tone shifts

### Style Guidelines

1. **Conversational**
   - Write as you speak
   - Short sentences
   - Active voice

2. **Technical Accuracy**
   - Define acronyms
   - Explain concepts clearly
   - Cite sources when needed

3. **Engagement**
   - Start with a hook
   - Use rhetorical questions
   - Build narrative tension

## Limitations & Workarounds

### Current Limitations

| Limitation | Workaround |
|------------|------------|
| 5,000 character prompt limit | Split content, focus on key points |
| 2-10 minute audio limit | Use as intro/summary, expand manually |
| No custom voice selection | Accept AI voices, add human intro/outro |
| No API (yet) | Manual upload to NotebookLM |
| Can't edit generated audio | Regenerate or post-process |

### Future Enhancements

- [ ] API integration for automation
- [ ] Custom voice training
- [ ] Longer episode generation
- [ ] Chapter marker support
- [ ] Multi-language support
- [ ] Voice cloning for consistent hosts

## Examples

### Example Season Prompt

See: `hosts/season-01-prompt.txt`

### Example Episode Prompt

```
Episode: The CIA Triad Explained
Code: P0D-S01-E003-AXIS-SHIELD

Target: 8 minutes
Audience: IT professionals new to security

## Goal
Explain Confidentiality, Integrity, and Availability with memorable examples.

## Structure
1. Why security matters (30 seconds)
2. Confidentiality - secrets stay secret (2 min)
   - Example: Medical records, banking info
   - Analogy: Locked safe
3. Integrity - data stays accurate (2 min)
   - Example: Financial transactions
   - Analogy: Tamper-evident seals
4. Availability - systems stay accessible (2 min)
   - Example: DDoS attacks
   - Analogy: Store hours
5. Balancing the three (1 min)
6. Takeaways (30 seconds)

## Discussion Points
- Why CIA triad? Why not just "security"?
- Real-world breaches for each pillar
- Trade-offs between pillars

## Tone
- Professional but friendly
- Use analogies for clarity
- Encourage questions
```

## Troubleshooting

### Audio Quality Issues

**Problem:** Audio sounds robotic or unnatural

**Solutions:**
- Rewrite prompt to be more conversational
- Add more examples and context
- Use shorter sentences
- Include "Host A:" and "Host B:" dialogue

### Content Not Covered

**Problem:** Audio skips important points

**Solutions:**
- Make key points more prominent
- Reduce total content (focus on 3-5 points)
- Add explicit structure cues
- Use numbered lists

### Generation Fails

**Problem:** NotebookLM doesn't generate audio

**Solutions:**
- Check document is properly uploaded
- Ensure content is appropriate
- Try regenerating
- Verify notebook has sufficient sources

## Resources

- [NotebookLM Official Site](https://notebooklm.google.com)
- [Google Drive API Docs](https://developers.google.com/drive)
- [Audio Overview Guide](https://support.google.com/notebooklm)

---

**Last Updated:** 2025-10-27  
**Version:** 1.0
