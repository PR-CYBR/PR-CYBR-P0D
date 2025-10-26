#!/usr/bin/env python3
"""
Notion Episode Sync Script

This script synchronizes podcast episodes from a Notion database to the repository.
It queries the "pr-cyberpod" Notion database, identifies episodes marked as live,
downloads their MP3 files, and commits them to the episodes directory.
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import requests
from notion_client import Client
from slugify import slugify


# Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
EPISODES_DIR = Path("episodes")
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class NotionEpisodeSync:
    """Handles synchronization of podcast episodes from Notion database."""

    def __init__(self, token: str, database_id: str):
        """
        Initialize the sync client.

        Args:
            token: Notion API integration token
            database_id: ID of the pr-cyberpod Notion database
        """
        self.client = Client(auth=token)
        self.database_id = database_id
        self.episodes_dir = EPISODES_DIR
        self.episodes_dir.mkdir(exist_ok=True)

    def get_live_episodes(self) -> List[Dict]:
        """
        Query Notion database for episodes marked as live.

        Returns:
            List of episode dictionaries with metadata
        """
        print("🔍 Querying Notion database for live episodes...")
        
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Episode Live",
                    "checkbox": {
                        "equals": True
                    }
                }
            )
            
            episodes = []
            for page in response.get("results", []):
                episode = self._parse_episode(page)
                if episode:
                    episodes.append(episode)
            
            print(f"✅ Found {len(episodes)} live episodes")
            return episodes
            
        except Exception as e:
            print(f"❌ Error querying Notion database: {e}")
            raise

    def _parse_episode(self, page: Dict) -> Optional[Dict]:
        """
        Parse episode metadata from Notion page.

        Args:
            page: Notion page object

        Returns:
            Dictionary with episode metadata or None if invalid
        """
        try:
            properties = page.get("properties", {})
            
            # Extract title
            title_prop = properties.get("Title", {})
            title = ""
            if title_prop.get("title"):
                title = "".join([t.get("plain_text", "") for t in title_prop["title"]])
            
            # Extract file URL
            file_url_prop = properties.get("File URL", {})
            file_url = file_url_prop.get("url", "")
            
            # Extract release date
            release_date_prop = properties.get("Release Date", {})
            release_date = release_date_prop.get("date", {}).get("start", "")
            
            # Extract episode number (optional)
            episode_num_prop = properties.get("Episode Number", {})
            episode_number = episode_num_prop.get("number")
            
            # Extract description (optional)
            description_prop = properties.get("Description", {})
            description = ""
            if description_prop.get("rich_text"):
                description = "".join([t.get("plain_text", "") for t in description_prop["rich_text"]])
            
            # Validate required fields
            if not title or not file_url:
                print(f"⚠️  Skipping episode with missing title or file URL")
                return None
            
            return {
                "notion_id": page["id"],
                "title": title,
                "file_url": file_url,
                "release_date": release_date,
                "episode_number": episode_number,
                "description": description,
            }
            
        except Exception as e:
            print(f"⚠️  Error parsing episode: {e}")
            return None

    def _get_episode_filename(self, episode: Dict) -> str:
        """
        Generate consistent filename for episode.

        Args:
            episode: Episode metadata dictionary

        Returns:
            Filename for the episode
        """
        slug = slugify(episode["title"])
        
        if episode["episode_number"]:
            return f"episode-{episode['episode_number']:03d}-{slug}"
        else:
            # Use hash of title if no episode number
            title_hash = hashlib.md5(episode["title"].encode()).hexdigest()[:8]
            return f"episode-{title_hash}-{slug}"

    def _file_exists(self, filename_base: str) -> bool:
        """
        Check if episode file already exists.

        Args:
            filename_base: Base filename without extension

        Returns:
            True if file exists, False otherwise
        """
        mp3_file = self.episodes_dir / f"{filename_base}.mp3"
        return mp3_file.exists()

    def download_episode(self, episode: Dict) -> bool:
        """
        Download episode MP3 file from URL.

        Args:
            episode: Episode metadata dictionary

        Returns:
            True if download successful, False otherwise
        """
        filename_base = self._get_episode_filename(episode)
        
        # Check if already downloaded
        if self._file_exists(filename_base):
            print(f"⏭️  Episode already exists: {filename_base}")
            return False
        
        mp3_file = self.episodes_dir / f"{filename_base}.mp3"
        metadata_file = self.episodes_dir / f"{filename_base}-metadata.json"
        
        print(f"⬇️  Downloading: {episode['title']}")
        
        # Download with retries
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(episode["file_url"], timeout=300)
                response.raise_for_status()
                
                # Validate content type
                content_type = response.headers.get("content-type", "")
                if "audio" not in content_type and "octet-stream" not in content_type:
                    print(f"⚠️  Warning: Unexpected content type: {content_type}")
                
                # Save MP3 file
                mp3_file.write_bytes(response.content)
                print(f"✅ Downloaded: {mp3_file.name} ({len(response.content)} bytes)")
                
                # Save metadata
                metadata = {
                    "title": episode["title"],
                    "release_date": episode["release_date"],
                    "episode_number": episode["episode_number"],
                    "description": episode["description"],
                    "notion_id": episode["notion_id"],
                    "file_url": episode["file_url"],
                    "downloaded_at": datetime.utcnow().isoformat(),
                    "file_size": len(response.content),
                }
                metadata_file.write_text(json.dumps(metadata, indent=2))
                
                return True
                
            except requests.RequestException as e:
                print(f"⚠️  Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"❌ Failed to download after {MAX_RETRIES} attempts")
                    return False
        
        return False

    def sync(self) -> int:
        """
        Perform full sync of live episodes.

        Returns:
            Number of newly downloaded episodes
        """
        print("🚀 Starting Notion episode sync...")
        
        episodes = self.get_live_episodes()
        downloaded_count = 0
        
        for episode in episodes:
            if self.download_episode(episode):
                downloaded_count += 1
        
        print(f"\n📊 Sync complete: {downloaded_count} new episodes downloaded")
        return downloaded_count


def main():
    """Main entry point for the sync script."""
    print("=" * 60)
    print("PR-CYBR-P0D Notion Episode Sync")
    print("=" * 60)
    
    # Validate environment variables
    if not NOTION_TOKEN:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        sys.exit(1)
    
    if not NOTION_DATABASE_ID:
        print("❌ Error: NOTION_DATABASE_ID environment variable not set")
        sys.exit(1)
    
    # Perform sync
    try:
        syncer = NotionEpisodeSync(NOTION_TOKEN, NOTION_DATABASE_ID)
        downloaded_count = syncer.sync()
        
        # Exit with status code indicating number of downloads
        # 0 = no new episodes, >0 = new episodes downloaded
        sys.exit(0 if downloaded_count == 0 else 0)
        
    except Exception as e:
        print(f"\n❌ Sync failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
