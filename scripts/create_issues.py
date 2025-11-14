#!/usr/bin/env python3
"""
Create GitHub Issues from Task Definitions

This script reads task definitions from JSON and creates or updates GitHub issues
in the appropriate agent repositories. It provides idempotency by checking for
existing issues with the same task_id before creating new ones.

Usage:
    python create_issues.py --input <tasks_json>

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token with repo scope (required)
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GitHubIssueCreator:
    """Handles creation and updating of GitHub issues."""
    
    def __init__(self, token: str, organization: str, agent_mapping: Dict[str, str]):
        """
        Initialize the GitHub issue creator.
        
        Args:
            token: GitHub personal access token
            organization: GitHub organization name
            agent_mapping: Dictionary mapping agent IDs to repository names
        """
        self.token = token
        self.organization = organization
        self.agent_mapping = agent_mapping
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'PR-CYBR-P0D-IssueCreator/1.0'
        })
    
    def get_repository_name(self, agent_id: str, fallback_repo: Optional[str] = None) -> str:
        """
        Get repository name for an agent ID.
        
        Args:
            agent_id: Agent identifier (e.g., 'A-01')
            fallback_repo: Optional fallback repository name
            
        Returns:
            Repository name
            
        Raises:
            ValueError: If agent_id is not found and no fallback provided
        """
        repo = self.agent_mapping.get(agent_id, fallback_repo)
        if not repo:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        return repo
    
    def search_issue_by_task_id(self, repo: str, task_id: str) -> Optional[int]:
        """
        Search for an existing issue by task_id label.
        
        Args:
            repo: Repository name
            task_id: Task identifier
            
        Returns:
            Issue number if found, None otherwise
        """
        logger.debug(f"Searching for existing issue with task_id: {task_id}")
        
        # Search for issues with the task_id in the title or labels
        query = f"repo:{self.organization}/{repo} {task_id} in:title"
        url = f"{self.base_url}/search/issues"
        
        params = {
            'q': query,
            'per_page': 10
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            if items:
                issue_number = items[0]['number']
                logger.info(f"Found existing issue #{issue_number} for task {task_id}")
                return issue_number
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error searching for issue: {e}")
            return None
    
    def create_issue(self, repo: str, task: Dict[str, Any]) -> int:
        """
        Create a new GitHub issue.
        
        Args:
            repo: Repository name
            task: Task dictionary containing issue details
            
        Returns:
            Issue number of created issue
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        url = f"{self.base_url}/repos/{self.organization}/{repo}/issues"
        
        # Format issue title to include task_id
        title = f"[{task['task_id']}] {task['title']}"
        
        # Format issue body
        body_parts = [
            task['description'],
            "",
            "---",
            f"**Task ID:** `{task['task_id']}`",
            f"**Priority:** {task['priority']}",
            f"**Type:** {task['type']}",
            f"**Explicit:** {'Yes' if task.get('explicit', False) else 'No (Inferred)'}",
        ]
        
        # Add meeting reference if available
        meeting_labels = [label for label in task.get('labels', []) if label.startswith('meeting/')]
        if meeting_labels:
            meeting_id = meeting_labels[0].split('/')[-1]
            body_parts.append(f"**Meeting:** {meeting_id}")
        
        body = "\n".join(body_parts)
        
        # Prepare payload
        payload = {
            'title': title,
            'body': body,
            'labels': task.get('labels', [])
        }
        
        logger.info(f"Creating issue in {self.organization}/{repo}: {title}")
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        issue_data = response.json()
        issue_number = issue_data['number']
        
        logger.info(f"✅ Created issue #{issue_number}: {title}")
        return issue_number
    
    def update_issue(self, repo: str, issue_number: int, task: Dict[str, Any]) -> None:
        """
        Update an existing GitHub issue.
        
        Args:
            repo: Repository name
            issue_number: Issue number to update
            task: Task dictionary containing updated details
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        url = f"{self.base_url}/repos/{self.organization}/{repo}/issues/{issue_number}"
        
        # Format issue body
        body_parts = [
            task['description'],
            "",
            "---",
            f"**Task ID:** `{task['task_id']}`",
            f"**Priority:** {task['priority']}",
            f"**Type:** {task['type']}",
            f"**Explicit:** {'Yes' if task.get('explicit', False) else 'No (Inferred)'}",
            "",
            f"*Last updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}*"
        ]
        
        body = "\n".join(body_parts)
        
        # Prepare payload
        payload = {
            'body': body,
            'labels': task.get('labels', [])
        }
        
        logger.info(f"Updating issue #{issue_number} in {self.organization}/{repo}")
        
        response = self.session.patch(url, json=payload)
        response.raise_for_status()
        
        logger.info(f"✅ Updated issue #{issue_number}")
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task by creating or updating an issue.
        
        Args:
            task: Task dictionary
            
        Returns:
            Result dictionary with status and details
        """
        task_id = task.get('task_id', 'unknown')
        agent_id = task.get('agent', 'unknown')
        
        try:
            # Get repository name
            repo = self.get_repository_name(agent_id, task.get('repo'))
            
            # Check if issue already exists
            existing_issue = self.search_issue_by_task_id(repo, task_id)
            
            if existing_issue:
                # Update existing issue
                self.update_issue(repo, existing_issue, task)
                return {
                    'task_id': task_id,
                    'status': 'updated',
                    'issue_number': existing_issue,
                    'repo': repo
                }
            else:
                # Create new issue
                issue_number = self.create_issue(repo, task)
                return {
                    'task_id': task_id,
                    'status': 'created',
                    'issue_number': issue_number,
                    'repo': repo
                }
                
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            return {
                'task_id': task_id,
                'status': 'error',
                'error': str(e)
            }


def load_agent_mapping(config_path: Path) -> Dict[str, str]:
    """
    Load agent to repository mapping from YAML config.
    
    Args:
        config_path: Path to agents.yaml config file
        
    Returns:
        Dictionary mapping agent IDs to repository names
    """
    logger.info(f"Loading agent mapping from {config_path}")
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    agents = config.get('agents', {})
    logger.info(f"Loaded mapping for {len(agents)} agents")
    
    return agents


def load_tasks(tasks_path: Path) -> Dict[str, Any]:
    """
    Load tasks from JSON file.
    
    Args:
        tasks_path: Path to tasks JSON file
        
    Returns:
        Dictionary containing tasks data
    """
    logger.info(f"Loading tasks from {tasks_path}")
    
    if not tasks_path.exists():
        raise FileNotFoundError(f"Tasks file not found: {tasks_path}")
    
    with open(tasks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tasks = data.get('tasks', [])
    logger.info(f"Loaded {len(tasks)} tasks")
    
    return data


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Create GitHub issues from task definitions'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to tasks JSON file'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/agents.yaml'),
        help='Path to agents mapping config (default: config/agents.yaml)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate issue creation without making changes'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Check for required environment variables
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token and not args.dry_run:
        logger.error("GITHUB_TOKEN environment variable not set")
        print("❌ Error: GITHUB_TOKEN environment variable is required", file=sys.stderr)
        return 1
    
    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - No issues will be created or updated")
    
    try:
        # Load agent mapping
        agent_mapping = load_agent_mapping(args.config)
        
        # Load tasks
        tasks_data = load_tasks(args.input)
        tasks = tasks_data.get('tasks', [])
        meeting_id = tasks_data.get('meeting_id', 'unknown')
        
        if not tasks:
            logger.warning("No tasks found in input file")
            print("⚠️  No tasks to process")
            return 0
        
        # Get organization from config or use default
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        organization = config.get('organization', 'PR-CYBR')
        
        if args.dry_run:
            # In dry run mode, just log what would be done
            print(f"\n📋 Would process {len(tasks)} tasks for meeting {meeting_id}:")
            for task in tasks:
                agent_id = task.get('agent', 'unknown')
                repo = agent_mapping.get(agent_id, task.get('repo', 'unknown'))
                print(f"  - [{task['task_id']}] {task['title'][:60]}... → {organization}/{repo}")
            return 0
        
        # Create issue creator
        creator = GitHubIssueCreator(github_token, organization, agent_mapping)
        
        # Process all tasks
        results = []
        for task in tasks:
            result = creator.process_task(task)
            results.append(result)
            
            # Be nice to GitHub API (rate limiting)
            time.sleep(0.5)
        
        # Print summary
        created = sum(1 for r in results if r.get('status') == 'created')
        updated = sum(1 for r in results if r.get('status') == 'updated')
        errors = sum(1 for r in results if r.get('status') == 'error')
        
        print(f"\n✅ Processed {len(results)} tasks:")
        print(f"   📝 Created: {created}")
        print(f"   🔄 Updated: {updated}")
        if errors > 0:
            print(f"   ❌ Errors: {errors}")
        
        return 0 if errors == 0 else 1
        
    except Exception as e:
        logger.error(f"Error creating issues: {e}", exc_info=True)
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
