#!/usr/bin/env python3
"""
Extract Tasks from Meeting Transcripts

This script processes meeting transcripts and uses an LLM to extract actionable tasks.
It outputs a structured JSON file containing tasks that need to be routed to agent repositories.

Usage:
    python extract_tasks.py --input <input_json> --output <output_json>

Environment Variables:
    OPENAI_API_KEY: API key for OpenAI (required for LLM processing)
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_transcript(input_path: Path) -> Dict[str, Any]:
    """
    Load transcript data from JSON file.
    
    Args:
        input_path: Path to input JSON file containing transcript data
        
    Returns:
        Dictionary containing transcript data
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        json.JSONDecodeError: If input file is not valid JSON
    """
    logger.info(f"Loading transcript from {input_path}")
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Successfully loaded transcript with {len(data.get('transcript', ''))} characters")
    return data


def extract_tasks_with_llm(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract tasks from transcript using LLM (OpenAI API).
    
    This is a stub implementation. In production, this would:
    1. Format the transcript for the LLM
    2. Send request to OpenAI API
    3. Parse the LLM response
    4. Structure tasks according to schema
    
    Args:
        transcript_data: Dictionary containing transcript and metadata
        
    Returns:
        List of task dictionaries
    """
    # Check for API key (but don't fail if missing - this is a stub)
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.warning("OPENAI_API_KEY not set. Using stub task extraction.")
        return extract_tasks_stub(transcript_data)
    
    # TODO: Implement actual OpenAI API integration
    # For now, return stub implementation
    logger.info("Using stub task extraction (OpenAI integration not yet implemented)")
    return extract_tasks_stub(transcript_data)


def extract_tasks_stub(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Stub implementation for task extraction.
    
    This demonstrates the expected output format. In production, this would
    be replaced by actual LLM-based extraction.
    
    Args:
        transcript_data: Dictionary containing transcript and metadata
        
    Returns:
        List of task dictionaries in the expected schema
    """
    meeting_id = transcript_data.get('meeting_id', 'unknown')
    transcript_text = transcript_data.get('transcript', '')
    
    # Parse transcript for action items (simple keyword-based stub)
    tasks = []
    
    # Look for common action indicators
    action_keywords = [
        'TODO', 'ACTION ITEM', 'TASK', 'NEED TO', 'SHOULD', 
        'UPDATE', 'FIX', 'IMPLEMENT', 'CREATE', 'ADD'
    ]
    
    # Simple line-by-line parsing (stub logic)
    lines = transcript_text.split('\n')
    task_id_counter = 1
    
    for line in lines:
        line_upper = line.upper()
        if any(keyword in line_upper for keyword in action_keywords):
            # Extract a simple task (this is just demonstration logic)
            task = {
                "task_id": f"{meeting_id}_TASK_{task_id_counter:03d}",
                "agent": "A-01",  # Default agent (would be determined by LLM)
                "repo": "PR-CYBR-AGENT-01",  # Default repo
                "title": line.strip()[:100],  # First 100 chars
                "description": line.strip(),
                "priority": "medium",  # Default priority
                "type": "enhancement",  # Default type
                "labels": ["automation/codex", f"meeting/{meeting_id}"],
                "explicit": False  # False = inferred, True = explicitly stated
            }
            tasks.append(task)
            task_id_counter += 1
            
            # Limit to 10 tasks in stub mode
            if task_id_counter > 10:
                break
    
    logger.info(f"Extracted {len(tasks)} tasks (stub mode)")
    return tasks


def generate_summary(transcript_data: Dict[str, Any], tasks: List[Dict[str, Any]]) -> str:
    """
    Generate a summary of the meeting.
    
    Args:
        transcript_data: Dictionary containing transcript and metadata
        tasks: List of extracted tasks
        
    Returns:
        String summary of the meeting
    """
    meeting_id = transcript_data.get('meeting_id', 'unknown')
    timestamp = transcript_data.get('timestamp', datetime.now(timezone.utc).isoformat())
    
    summary = f"Meeting {meeting_id} held on {timestamp}. "
    summary += f"Extracted {len(tasks)} actionable tasks. "
    
    if tasks:
        agents = set(task['agent'] for task in tasks)
        summary += f"Tasks assigned to agents: {', '.join(sorted(agents))}."
    
    return summary


def save_tasks(output_path: Path, meeting_id: str, summary: str, tasks: List[Dict[str, Any]]) -> None:
    """
    Save extracted tasks to JSON file.
    
    Args:
        output_path: Path to output JSON file
        meeting_id: Meeting identifier
        summary: Meeting summary
        tasks: List of task dictionaries
    """
    logger.info(f"Saving {len(tasks)} tasks to {output_path}")
    
    output_data = {
        "meeting_id": meeting_id,
        "summary": summary,
        "tasks": tasks,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0"
    }
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Successfully saved tasks to {output_path}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Extract actionable tasks from meeting transcripts'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to input JSON file containing transcript data'
    )
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Path to output JSON file for extracted tasks'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Load transcript
        transcript_data = load_transcript(args.input)
        
        # Extract tasks using LLM
        tasks = extract_tasks_with_llm(transcript_data)
        
        # Generate summary
        meeting_id = transcript_data.get('meeting_id', 'unknown')
        summary = generate_summary(transcript_data, tasks)
        
        # Save tasks to output file
        save_tasks(args.output, meeting_id, summary, tasks)
        
        # Print summary to stdout
        print(f"✅ Successfully extracted {len(tasks)} tasks from meeting {meeting_id}")
        print(f"📄 Tasks saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error processing transcript: {e}", exc_info=True)
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
