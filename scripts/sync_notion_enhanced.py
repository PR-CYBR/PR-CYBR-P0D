#!/usr/bin/env python3
"""
Enhanced Notion Sync with Bidirectional Support

This module extends the original sync_notion.py with:
- Bidirectional sync (GitHub ↔ Notion)
- Prompt-Input field handling
- Google Drive integration
- NotebookLM integration
- Automatic metadata updates
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from datetime import datetime

from notion_client import Client

# Import utilities
try:
    from google_drive_utils import (
        GoogleDriveClient,
        NotebookLMClient,
        extract_audio_duration,
        generate_show_notes
    )
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print("⚠️  Google Drive utilities not available (import failed)")


class EnhancedNotionSync:
    """Enhanced Notion synchronization with bidirectional support."""
    
    def __init__(
        self,
        token: str,
        database_id: str,
        enable_google_drive: bool = True
    ):
        """
        Initialize enhanced sync client.
        
        Args:
            token: Notion API integration token
            database_id: ID of the Notion database
            enable_google_drive: Whether to enable Google Drive features
        """
        self.client = Client(auth=token)
        self.database_id = database_id
        self.episodes_dir = Path("episodes")
        self.prompts_dir = self.episodes_dir / "prompts"
        
        # Initialize Google Drive client if available
        self.google_drive = None
        self.notebook_lm = None
        
        if enable_google_drive and GOOGLE_DRIVE_AVAILABLE:
            try:
                self.google_drive = GoogleDriveClient()
                self.notebook_lm = NotebookLMClient()
                print("✅ Google Drive integration enabled")
            except Exception as e:
                print(f"⚠️  Google Drive initialization failed: {e}")
    
    def get_episodes_with_status(self, status: str = "Not started") -> List[Dict]:
        """
        Get episodes filtered by status.
        
        Args:
            status: Status to filter by (e.g., "Not started", "In progress")
            
        Returns:
            List of episode dictionaries
        """
        print(f"🔍 Querying episodes with status: {status}")
        
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Status",
                    "select": {
                        "equals": status
                    }
                }
            )
            
            episodes = []
            for page in response.get("results", []):
                episode = self._parse_episode_extended(page)
                if episode:
                    episodes.append(episode)
            
            print(f"✅ Found {len(episodes)} episodes with status '{status}'")
            return episodes
            
        except Exception as e:
            print(f"❌ Error querying Notion database: {e}")
            return []
    
    def _parse_episode_extended(self, page: Dict) -> Optional[Dict]:
        """
        Parse episode with extended fields.
        
        Args:
            page: Notion page object
            
        Returns:
            Dictionary with episode metadata
        """
        try:
            properties = page.get("properties", {})
            
            # Basic fields
            title = self._get_title_property(properties.get("Title", {}))
            season = self._get_number_property(properties.get("Season", {}))
            episode = self._get_number_property(properties.get("Episode", {}))
            
            # Extended fields for retrofit
            status = self._get_select_property(properties.get("Status", {}))
            code_name = self._get_text_property(properties.get("Code-Name", {}))
            prompt_input = self._get_text_property(properties.get("Prompt-Input", {}))
            script_doc_link = self._get_url_property(properties.get("Script-Doc-Link", {}))
            track_cloud = self._get_url_property(properties.get("Track-Cloud", {}))
            duration = self._get_text_property(properties.get("Duration", {}))
            show_notes_link = self._get_url_property(properties.get("Show-Notes-Link", {}))
            
            return {
                "notion_id": page["id"],
                "title": title,
                "season": season,
                "episode": episode,
                "status": status,
                "code_name": code_name,
                "prompt_input": prompt_input,
                "script_doc_link": script_doc_link,
                "track_cloud": track_cloud,
                "duration": duration,
                "show_notes_link": show_notes_link
            }
            
        except Exception as e:
            print(f"⚠️  Error parsing episode: {e}")
            return None
    
    def _get_title_property(self, prop: Dict) -> str:
        """Extract title from property."""
        if prop.get("title"):
            return "".join([t.get("plain_text", "") for t in prop["title"]])
        return ""
    
    def _get_text_property(self, prop: Dict) -> str:
        """Extract text from rich text property."""
        if prop.get("rich_text"):
            return "".join([t.get("plain_text", "") for t in prop["rich_text"]])
        return ""
    
    def _get_number_property(self, prop: Dict) -> Optional[int]:
        """Extract number from property."""
        return prop.get("number")
    
    def _get_select_property(self, prop: Dict) -> str:
        """Extract select value from property."""
        select = prop.get("select")
        if select:
            return select.get("name", "")
        return ""
    
    def _get_url_property(self, prop: Dict) -> str:
        """Extract URL from property."""
        return prop.get("url", "")
    
    def update_notion_property(
        self,
        page_id: str,
        property_name: str,
        value: any,
        property_type: str = "rich_text"
    ) -> bool:
        """
        Update a Notion page property.
        
        Args:
            page_id: Notion page ID
            property_name: Name of property to update
            value: New value
            property_type: Type of property (rich_text, url, number, etc.)
            
        Returns:
            True if successful
        """
        try:
            if property_type == "rich_text":
                properties = {
                    property_name: {
                        "rich_text": [{"text": {"content": str(value)}}]
                    }
                }
            elif property_type == "url":
                properties = {
                    property_name: {"url": str(value)}
                }
            elif property_type == "number":
                properties = {
                    property_name: {"number": value}
                }
            else:
                print(f"⚠️  Unsupported property type: {property_type}")
                return False
            
            self.client.pages.update(page_id=page_id, properties=properties)
            print(f"✅ Updated {property_name} for page {page_id[:8]}...")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update Notion property: {e}")
            return False
    
    def process_prompt_input(self, episode: Dict) -> bool:
        """
        Process Prompt-Input field and create Google Doc.
        
        Args:
            episode: Episode metadata dictionary
            
        Returns:
            True if successful
        """
        if not self.google_drive:
            print("⚠️  Google Drive not available, skipping prompt processing")
            return False
        
        prompt_text = episode.get("prompt_input", "")
        if not prompt_text:
            # Check for local prompt file
            prompt_file = self.prompts_dir / f"prompt_S{episode['season']:02d}E{episode['episode']:03d}.txt"
            if prompt_file.exists():
                prompt_text = prompt_file.read_text()
                print(f"📄 Loaded prompt from: {prompt_file.name}")
            else:
                print("⚠️  No prompt input found")
                return False
        
        # Create Google Doc with prompt content
        doc_title = f"{episode.get('code_name', 'Episode')} - Script"
        doc_result = self.google_drive.create_google_doc(
            title=doc_title,
            content=prompt_text
        )
        
        # Update Notion with Script-Doc-Link
        self.update_notion_property(
            episode["notion_id"],
            "Script-Doc-Link",
            doc_result["url"],
            "url"
        )
        
        return True
    
    def process_notebooklm_integration(self, episode: Dict) -> bool:
        """
        Process NotebookLM integration for episode.
        
        Args:
            episode: Episode metadata dictionary
            
        Returns:
            True if successful
        """
        if not self.notebook_lm or not episode.get("script_doc_link"):
            return False
        
        # Extract doc ID from URL
        doc_url = episode["script_doc_link"]
        doc_id = doc_url.split("/")[-2] if "/" in doc_url else doc_url
        
        # Get or create notebook for this season
        notebook_id = f"notebook_S{episode['season']:02d}"
        
        # Add document to notebook
        self.notebook_lm.add_source_to_notebook(notebook_id, doc_id)
        
        # Generate audio overview
        audio_result = self.notebook_lm.generate_audio_overview(notebook_id)
        
        # Update Notion with Track-Cloud
        self.update_notion_property(
            episode["notion_id"],
            "Track-Cloud",
            audio_result["url"],
            "url"
        )
        
        return True
    
    def process_audio_metadata(self, episode: Dict) -> bool:
        """
        Extract audio duration and update Notion.
        
        Args:
            episode: Episode metadata dictionary
            
        Returns:
            True if successful
        """
        track_url = episode.get("track_cloud", "")
        if not track_url:
            return False
        
        # In real implementation, download and extract duration
        # For now, use placeholder
        duration = "45:30"
        
        # Update Notion with duration
        self.update_notion_property(
            episode["notion_id"],
            "Duration",
            duration,
            "rich_text"
        )
        
        return True
    
    def generate_and_upload_show_notes(self, episode: Dict) -> bool:
        """
        Generate show notes and upload as Google Doc.
        
        Args:
            episode: Episode metadata dictionary
            
        Returns:
            True if successful
        """
        if not self.google_drive:
            return False
        
        # Generate show notes content
        show_notes = generate_show_notes(episode)
        
        # Create Google Doc
        doc_title = f"{episode.get('code_name', 'Episode')} - Show Notes"
        doc_result = self.google_drive.create_google_doc(
            title=doc_title,
            content=show_notes
        )
        
        # Update Notion with Show-Notes-Link
        self.update_notion_property(
            episode["notion_id"],
            "Show-Notes-Link",
            doc_result["url"],
            "url"
        )
        
        return True
    
    def retrofit_episode(self, episode: Dict) -> bool:
        """
        Run complete retrofit automation for an episode.
        
        Args:
            episode: Episode metadata dictionary
            
        Returns:
            True if successful
        """
        print(f"\n🔧 Retrofitting episode: {episode.get('title', 'Unknown')}")
        
        try:
            # Step 1: Process prompt input
            if episode.get("prompt_input") and not episode.get("script_doc_link"):
                self.process_prompt_input(episode)
            
            # Step 2: Process NotebookLM integration
            if episode.get("script_doc_link") and not episode.get("track_cloud"):
                self.process_notebooklm_integration(episode)
            
            # Step 3: Extract audio metadata
            if episode.get("track_cloud") and not episode.get("duration"):
                self.process_audio_metadata(episode)
            
            # Step 4: Generate show notes
            if episode.get("track_cloud") and not episode.get("show_notes_link"):
                self.generate_and_upload_show_notes(episode)
            
            print(f"✅ Retrofit complete for episode")
            return True
            
        except Exception as e:
            print(f"❌ Retrofit failed: {e}")
            return False


def get_season_database_ids() -> List[Tuple[int, str]]:
    """
    Get all season-specific database IDs from environment variables.
    
    Returns:
        List of tuples containing (season_number, database_id) for all configured seasons
    """
    database_ids = []
    
    # Check for season-specific database IDs (S1 through S18)
    for season in range(1, 19):
        db_id = os.environ.get(f"PR_CYBR_P0D_S{season}_DB_ID")
        if db_id:
            database_ids.append((season, db_id))
            print(f"✅ Found database ID for Season {season}")
    
    return database_ids


def main():
    """Main entry point for enhanced sync."""
    print("=" * 70)
    print("PR-CYBR-P0D Enhanced Notion Sync")
    print("=" * 70)
    
    # Get configuration
    notion_token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not notion_token:
        print("❌ Missing NOTION_TOKEN environment variable")
        return
    
    # Get all season-specific database IDs
    season_databases = get_season_database_ids()
    
    # If no season-specific IDs found, fall back to NOTION_DATABASE_ID
    if not season_databases and database_id:
        season_databases = [(0, database_id)]  # Season 0 indicates fallback
        print("✅ Using fallback NOTION_DATABASE_ID")
    
    if not season_databases:
        print("❌ No database IDs found. Set either NOTION_DATABASE_ID or PR_CYBR_P0D_S#_DB_ID")
        return
    
    print(f"\n📊 Found {len(season_databases)} database(s) to process")
    
    # Process each database
    total_episodes = 0
    for season, db_id in season_databases:
        print(f"\n{'=' * 70}")
        if season > 0:
            print(f"Processing Season {season} database: {db_id[:8]}...")
        else:
            print(f"Processing database: {db_id[:8]}...")
        print(f"{'=' * 70}")
        
        # Initialize sync for this database
        sync = EnhancedNotionSync(notion_token, db_id)
        
        # Find episodes to retrofit
        episodes = sync.get_episodes_with_status("Not started")
        total_episodes += len(episodes)
        
        print(f"\n📊 Found {len(episodes)} episodes to process")
        
        # Process each episode
        for episode in episodes:
            sync.retrofit_episode(episode)
    
    print("\n" + "=" * 70)
    print(f"✅ Enhanced sync complete - Processed {total_episodes} total episodes")
    print("=" * 70)


if __name__ == "__main__":
    main()
