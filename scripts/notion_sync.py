#!/usr/bin/env python3
"""
Notion Database Sync for Meeting Results

This script syncs completed agent work back to a Notion database.
It provides idempotency through deterministic UUID generation based on task identifiers.

Usage:
    python notion_sync.py --agent A-01 --repo PR-CYBR-AGENT-01 --issue 123 --pr 456 --meeting-date 2025-01-15 --summary "Task summary"

Environment Variables:
    NOTION_TOKEN: Notion integration token (required)
    NOTION_DATABASE_ID: Target Notion database ID (required)
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from notion_client import Client
except ImportError:
    print("Error: notion-client library not found. Install with: pip install notion-client", file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotionSync:
    """Handles synchronization of meeting results to Notion."""
    
    def __init__(self, token: str, database_id: str):
        """
        Initialize Notion sync handler.
        
        Args:
            token: Notion integration token
            database_id: Target database ID
        """
        self.client = Client(auth=token)
        self.database_id = database_id
        logger.info(f"Initialized Notion sync for database {database_id}")
    
    def generate_deterministic_id(self, agent: str, repo: str, issue: int, meeting_date: str) -> str:
        """
        Generate a deterministic UUID based on task identifiers.
        
        This ensures idempotency - the same task will always generate the same ID,
        allowing us to update existing entries instead of creating duplicates.
        
        Args:
            agent: Agent identifier (e.g., 'A-01')
            repo: Repository name
            issue: Issue number
            meeting_date: Meeting date (YYYY-MM-DD format)
            
        Returns:
            Deterministic UUID string
        """
        # Create a stable string representation
        identifier = f"{agent}:{repo}:{issue}:{meeting_date}"
        
        # Generate UUID from hash
        hash_obj = hashlib.sha256(identifier.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        
        # Convert to UUID (using first 32 hex characters)
        deterministic_uuid = str(uuid.UUID(hash_hex[:32]))
        
        logger.debug(f"Generated deterministic ID: {deterministic_uuid} for {identifier}")
        return deterministic_uuid
    
    def search_existing_page(self, deterministic_id: str) -> Optional[str]:
        """
        Search for an existing page by deterministic ID.
        
        Args:
            deterministic_id: Deterministic UUID to search for
            
        Returns:
            Page ID if found, None otherwise
        """
        logger.info(f"Searching for existing page with ID: {deterministic_id}")
        
        try:
            # Search for pages with matching deterministic ID in a custom property
            results = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Task ID",
                    "rich_text": {
                        "equals": deterministic_id
                    }
                }
            )
            
            if results.get('results'):
                page_id = results['results'][0]['id']
                logger.info(f"Found existing page: {page_id}")
                return page_id
            
            logger.info("No existing page found")
            return None
            
        except Exception as e:
            logger.warning(f"Error searching for existing page: {e}")
            return None
    
    def format_properties(
        self,
        deterministic_id: str,
        agent: str,
        repo: str,
        issue: int,
        pr: Optional[int],
        meeting_date: str,
        summary: str
    ) -> Dict[str, Any]:
        """
        Format properties for Notion page.
        
        Args:
            deterministic_id: Deterministic UUID
            agent: Agent identifier
            repo: Repository name
            issue: Issue number
            pr: Pull request number (optional)
            meeting_date: Meeting date
            summary: Task summary
            
        Returns:
            Dictionary of Notion properties
        """
        # Parse meeting date
        try:
            meeting_datetime = datetime.strptime(meeting_date, '%Y-%m-%d')
        except ValueError:
            meeting_datetime = datetime.utcnow()
            logger.warning(f"Invalid date format: {meeting_date}, using current date")
        
        # Format GitHub URLs
        issue_url = f"https://github.com/PR-CYBR/{repo}/issues/{issue}"
        pr_url = f"https://github.com/PR-CYBR/{repo}/pull/{pr}" if pr else None
        
        properties = {
            "Task ID": {
                "rich_text": [{"text": {"content": deterministic_id}}]
            },
            "Title": {
                "title": [{"text": {"content": summary[:100]}}]  # Notion title limit
            },
            "Agent": {
                "select": {"name": agent}
            },
            "Repository": {
                "rich_text": [{"text": {"content": repo}}]
            },
            "Issue": {
                "number": issue
            },
            "Meeting Date": {
                "date": {"start": meeting_datetime.isoformat()}
            },
            "Summary": {
                "rich_text": [{"text": {"content": summary[:2000]}}]  # Notion rich_text limit
            },
            "Issue URL": {
                "url": issue_url
            },
            "Status": {
                "select": {"name": "Complete"}
            }
        }
        
        # Add PR URL if provided
        if pr_url:
            properties["PR"] = {"number": pr}
            properties["PR URL"] = {"url": pr_url}
        
        return properties
    
    def create_page(
        self,
        deterministic_id: str,
        agent: str,
        repo: str,
        issue: int,
        pr: Optional[int],
        meeting_date: str,
        summary: str
    ) -> str:
        """
        Create a new page in the Notion database.
        
        Args:
            deterministic_id: Deterministic UUID
            agent: Agent identifier
            repo: Repository name
            issue: Issue number
            pr: Pull request number (optional)
            meeting_date: Meeting date
            summary: Task summary
            
        Returns:
            Created page ID
        """
        logger.info(f"Creating new page for {agent}/{repo}#{issue}")
        
        properties = self.format_properties(
            deterministic_id, agent, repo, issue, pr, meeting_date, summary
        )
        
        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
        
        page_id = response['id']
        logger.info(f"✅ Created page: {page_id}")
        return page_id
    
    def update_page(
        self,
        page_id: str,
        deterministic_id: str,
        agent: str,
        repo: str,
        issue: int,
        pr: Optional[int],
        meeting_date: str,
        summary: str
    ) -> None:
        """
        Update an existing page in the Notion database.
        
        Args:
            page_id: Notion page ID to update
            deterministic_id: Deterministic UUID
            agent: Agent identifier
            repo: Repository name
            issue: Issue number
            pr: Pull request number (optional)
            meeting_date: Meeting date
            summary: Task summary
        """
        logger.info(f"Updating existing page: {page_id}")
        
        properties = self.format_properties(
            deterministic_id, agent, repo, issue, pr, meeting_date, summary
        )
        
        self.client.pages.update(
            page_id=page_id,
            properties=properties
        )
        
        logger.info(f"✅ Updated page: {page_id}")
    
    def upsert(
        self,
        agent: str,
        repo: str,
        issue: int,
        pr: Optional[int],
        meeting_date: str,
        summary: str
    ) -> Dict[str, Any]:
        """
        Upsert (create or update) a page in the Notion database.
        
        Args:
            agent: Agent identifier
            repo: Repository name
            issue: Issue number
            pr: Pull request number (optional)
            meeting_date: Meeting date
            summary: Task summary
            
        Returns:
            Result dictionary with status and page ID
        """
        # Generate deterministic ID
        deterministic_id = self.generate_deterministic_id(agent, repo, issue, meeting_date)
        
        # Check for existing page
        existing_page = self.search_existing_page(deterministic_id)
        
        if existing_page:
            # Update existing page
            self.update_page(
                existing_page, deterministic_id, agent, repo, issue, pr, meeting_date, summary
            )
            return {
                'status': 'updated',
                'page_id': existing_page,
                'deterministic_id': deterministic_id
            }
        else:
            # Create new page
            page_id = self.create_page(
                deterministic_id, agent, repo, issue, pr, meeting_date, summary
            )
            return {
                'status': 'created',
                'page_id': page_id,
                'deterministic_id': deterministic_id
            }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Sync meeting results to Notion database'
    )
    parser.add_argument(
        '--agent',
        required=True,
        help='Agent identifier (e.g., A-01)'
    )
    parser.add_argument(
        '--repo',
        required=True,
        help='Repository name (e.g., PR-CYBR-AGENT-01)'
    )
    parser.add_argument(
        '--issue',
        type=int,
        required=True,
        help='GitHub issue number'
    )
    parser.add_argument(
        '--pr',
        type=int,
        help='GitHub pull request number (optional)'
    )
    parser.add_argument(
        '--meeting-date',
        required=True,
        help='Meeting date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--summary',
        required=True,
        help='Task summary'
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
    notion_token = os.environ.get('NOTION_TOKEN')
    notion_database_id = os.environ.get('NOTION_DATABASE_ID')
    
    if not notion_token:
        logger.error("NOTION_TOKEN environment variable not set")
        print("❌ Error: NOTION_TOKEN environment variable is required", file=sys.stderr)
        return 1
    
    if not notion_database_id:
        logger.error("NOTION_DATABASE_ID environment variable not set")
        print("❌ Error: NOTION_DATABASE_ID environment variable is required", file=sys.stderr)
        return 1
    
    try:
        # Initialize Notion sync
        notion = NotionSync(notion_token, notion_database_id)
        
        # Perform upsert
        result = notion.upsert(
            agent=args.agent,
            repo=args.repo,
            issue=args.issue,
            pr=args.pr,
            meeting_date=args.meeting_date,
            summary=args.summary
        )
        
        # Print result
        status = result['status']
        page_id = result['page_id']
        
        if status == 'created':
            print(f"✅ Created new Notion page: {page_id}")
        else:
            print(f"✅ Updated existing Notion page: {page_id}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error syncing to Notion: {e}", exc_info=True)
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
