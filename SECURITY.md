# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |

## Reporting a Vulnerability

The PR-CYBR team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to the [Security tab](https://github.com/PR-CYBR/PR-CYBR-P0D/security/advisories)
   - Click "Report a vulnerability"
   - Provide details in the form

2. **Email**
   - Send details to: security@pr-cybr.com
   - Use subject: `[SECURITY] PR-CYBR-P0D: [Brief Description]`

### What to Include

Please include as much of the following information as possible:

- **Type of vulnerability** (e.g., authentication bypass, injection, etc.)
- **Full paths of source file(s)** related to the vulnerability
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability** and what an attacker might be able to do
- **Potential mitigations** you've identified (if any)

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt of your vulnerability report within 48 hours
- **Updates**: We'll send you regular updates on our progress (at least every 5 business days)
- **Validation**: We'll work to validate the issue and determine its severity
- **Fix Timeline**: 
  - Critical vulnerabilities: 7 days
  - High severity: 30 days
  - Medium/Low severity: 90 days
- **Disclosure**: Once fixed, we'll coordinate disclosure timing with you
- **Credit**: We'll publicly thank you for responsible disclosure (unless you prefer to remain anonymous)

### Safe Harbor

We support safe harbor for security researchers who:

- Make a good faith effort to avoid privacy violations, data destruction, and service interruption
- Only interact with accounts you own or with explicit permission of the account holder
- Do not exploit a security issue beyond what's necessary to demonstrate it
- Allow us reasonable time to fix issues before public disclosure
- Follow this security policy

We will not pursue legal action against researchers who follow this policy.

## Security Best Practices

### For Contributors

When contributing to this project, please:

1. **Never commit secrets**
   - Don't commit API keys, tokens, passwords, or credentials
   - Use `.env` files (which are gitignored) for local secrets
   - Use GitHub Secrets for CI/CD credentials
   - Always use `.env.example` with placeholder values

2. **Validate all inputs**
   - Sanitize user inputs in scripts
   - Validate file paths to prevent directory traversal
   - Validate URLs before downloading content

3. **Use secure dependencies**
   - Keep dependencies up to date
   - Review dependency security advisories
   - Use `pip install --upgrade` for security patches

4. **Follow least privilege principle**
   - GitHub Actions workflows should use minimal necessary permissions
   - Notion integrations should have read-only access when possible
   - Service accounts should have minimal scopes

5. **Protect sensitive data**
   - Episode metadata may contain private information
   - Don't log credentials or tokens
   - Sanitize error messages that might expose system details

### For Maintainers

1. **Review all PRs for security implications**
   - Check for accidentally committed secrets
   - Review new dependencies
   - Validate input handling in scripts

2. **Enable GitHub security features**
   - Dependabot alerts
   - Code scanning
   - Secret scanning
   - Branch protection rules

3. **Regular security audits**
   - Review access permissions quarterly
   - Rotate secrets regularly
   - Audit workflow permissions
   - Check for unused integrations

4. **Incident response**
   - Have a plan for security incidents
   - Know how to rotate all credentials quickly
   - Document incident response procedures

## Security-Related Configuration

### GitHub Actions Permissions

Our workflows follow the principle of least privilege:

```yaml
permissions:
  contents: write  # Only for workflows that commit changes
  # Other permissions are explicitly denied by default
```

### Secret Management

Required secrets (stored in GitHub Secrets):

- `NOTION_TOKEN` - Notion API integration token
- `NOTION_EPISODES_DB_ID` - Database ID
- `ARCHIVE_ACCESS_KEY` - Internet Archive S3 access key
- `ARCHIVE_SECRET_KEY` - Internet Archive S3 secret key
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Network Security

- All API communications use HTTPS
- Webhook endpoints should validate signatures
- Rate limiting should be implemented for public endpoints

## Known Security Considerations

### Episode Files

- Episode MP3 files are public by design (for podcast distribution)
- Metadata in `meta.yaml` may contain public information
- Transcripts are public once published

### API Keys

- Notion tokens have database-level access (not workspace-wide)
- Archive.org keys can upload to your account (use dedicated account if possible)
- OpenAI keys are rate-limited (consider setting usage limits)

### Webhook Security

- n8n webhooks should use authentication tokens
- GitHub dispatch events require a valid GitHub token
- Validate all webhook payloads before processing

## Vulnerability Disclosure Policy

When a security vulnerability is confirmed:

1. We'll develop and test a fix
2. We'll prepare a security advisory
3. We'll coordinate disclosure with the reporter
4. We'll release the fix and publish the advisory
5. We'll credit the reporter (unless they prefer anonymity)

Typical disclosure timeline:
- Day 0: Vulnerability reported
- Day 1-2: Acknowledgment sent
- Day 3-7: Validation and severity assessment
- Day 7-30: Fix developed and tested
- Day 30-45: Fix released
- Day 45: Public disclosure

## Security Updates

Subscribe to security updates:

- Watch this repository for security advisories
- Check the [Security Advisories page](https://github.com/PR-CYBR/PR-CYBR-P0D/security/advisories)
- Follow our security updates via [GitHub Discussions](https://github.com/PR-CYBR/PR-CYBR-P0D/discussions)

## Compliance

This project follows:

- OWASP Top 10 guidelines
- GitHub security best practices
- Principle of least privilege
- Defense in depth

## Questions?

If you have questions about this security policy, please open a [GitHub Discussion](https://github.com/PR-CYBR/PR-CYBR-P0D/discussions) or email security@pr-cybr.com.

---

**Last Updated:** 2025-10-27  
**Policy Version:** 1.0
