# Episode Prompts Directory

This directory contains AI prompts for episode content generation.

## Purpose

Episode prompts are 5,000-character AI directives that guide NotebookLM in generating podcast episode scripts and audio content.

## File Naming Convention

Prompts should be named using the format:
```
prompt_S<season>E<episode>.txt
```

Examples:
- `prompt_S01E001.txt` - Season 1, Episode 1
- `prompt_S02E015.txt` - Season 2, Episode 15
- `prompt_S17E052.txt` - Season 17, Episode 52

## Prompt Guidelines

### Length
- **Maximum:** 5,000 characters
- **Recommended:** 3,000-4,500 characters
- Include enough detail for comprehensive content generation
- Leave room for NotebookLM to add context and structure

### Structure

A well-crafted prompt should include:

1. **Topic Overview**
   - Main subject or theme
   - Why this topic is important
   - Target audience level

2. **Key Points to Cover**
   - 3-5 main concepts or sections
   - Technical details to include
   - Examples or case studies

3. **Tone and Style**
   - Professional level (beginner, intermediate, advanced)
   - Conversational vs. formal
   - Technical depth

4. **Special Instructions**
   - Duration target (typically 45 minutes)
   - Required terminology
   - Topics to avoid or emphasize

### Example Prompt Template

```
Create a comprehensive podcast episode about [TOPIC].

Episode Overview:
This episode explores [MAIN THEME] and its impact on [AREA]. 
The target audience includes [AUDIENCE DESCRIPTION].

Key Topics to Cover:
1. Background and History
   - [Historical context]
   - [Evolution of the topic]
   
2. Current State
   - [Present situation]
   - [Key players and technologies]
   
3. Technical Deep Dive
   - [Technical concept 1]
   - [Technical concept 2]
   - [Real-world applications]
   
4. Best Practices
   - [Recommendation 1]
   - [Recommendation 2]
   - [Common pitfalls]
   
5. Future Outlook
   - [Emerging trends]
   - [Predictions]

Tone: Professional but accessible, suitable for cybersecurity professionals
Duration: Target 45 minutes
Focus: Balance theory with practical applications
```

## Integration with Retrofit System

When a prompt file is created or updated:

1. **Detection**: Retrofit workflow scans for new/updated prompts
2. **Processing**: Content is loaded and validated
3. **Document Creation**: Google Doc created with script template
4. **Audio Generation**: NotebookLM generates podcast audio
5. **Metadata Update**: Notion fields updated with links

## Manual Usage

### Create a New Prompt

```bash
# Create prompt file
cat > episodes/prompts/prompt_S01E001.txt << 'EOF'
Create a comprehensive introduction to cybersecurity fundamentals...
[Your prompt content here, up to 5,000 characters]
EOF

# Run retrofit automation
python scripts/sync_notion_enhanced.py
```

### Update Existing Prompt

1. Edit the prompt file
2. Run retrofit workflow manually or wait for scheduled run
3. New documents and audio will be regenerated

## Best Practices

1. **Be Specific**: Clear instructions yield better results
2. **Provide Context**: Include background information
3. **Structure Well**: Use clear sections and bullet points
4. **Test Iteratively**: Start with one episode, refine approach
5. **Version Control**: Commit prompts to track changes
6. **Review Output**: Check generated content for accuracy
7. **Iterate**: Refine prompts based on results

## Prompt Quality Checklist

- [ ] Under 5,000 characters
- [ ] Clear topic definition
- [ ] Structured with sections
- [ ] Tone and style specified
- [ ] Target duration mentioned
- [ ] Key points listed
- [ ] Technical depth appropriate
- [ ] Examples or case studies included
- [ ] Avoid ambiguous language
- [ ] Grammatically correct

## Troubleshooting

**Issue**: Prompt not being processed

**Solutions**:
- Verify file naming convention
- Check file is in correct directory
- Ensure file encoding is UTF-8
- Verify character count under 5,000
- Check Notion Status field is "Not started"

**Issue**: Generated content doesn't match expectations

**Solutions**:
- Refine prompt with more specific instructions
- Add examples of desired output
- Specify technical depth more clearly
- Break complex topics into multiple episodes
- Review and iterate on prompt structure

## Resources

- [NotebookLM Documentation](https://notebooklm.google.com)
- [Retrofit Guide](../retrofitting/docs/RETROFIT_GUIDE.md)
- [Template Documentation](../retrofitting/templates/README.md)

---

**Last Updated**: 2024-01-01
