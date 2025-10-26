#!/usr/bin/env python3
"""
Release Schedule Population Script

Generates release schedule for podcast episodes across all seasons (1-17).
Calculates release dates based on Monday/Wednesday/Friday pattern at 06:00 UTC.
Saves the schedule to episodes/release-schedule.txt.
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Tuple


# Configuration
EPISODES_DIR = Path("episodes")
SCHEDULE_FILE = EPISODES_DIR / "release-schedule.txt"
RELEASE_DAYS = [0, 2, 4]  # Monday=0, Wednesday=2, Friday=4
RELEASE_TIME = "06:00"  # 24-hour UTC format
START_DATE = datetime(2024, 1, 1, 6, 0)  # Default start date
EPISODES_PER_SEASON = 52  # Default episodes per season
TOTAL_SEASONS = 17


def get_next_release_day(current_date: datetime) -> datetime:
    """
    Calculate the next release day (Monday, Wednesday, or Friday).
    
    Args:
        current_date: Current date to calculate from
        
    Returns:
        Next release date at 06:00 UTC
    """
    current_weekday = current_date.weekday()
    
    # Find the next release day
    for day in RELEASE_DAYS:
        if day > current_weekday:
            days_ahead = day - current_weekday
            next_date = current_date + timedelta(days=days_ahead)
            return next_date.replace(hour=6, minute=0, second=0, microsecond=0)
    
    # If no release day found this week, get Monday of next week
    days_ahead = (7 - current_weekday) + RELEASE_DAYS[0]
    next_date = current_date + timedelta(days=days_ahead)
    return next_date.replace(hour=6, minute=0, second=0, microsecond=0)


def generate_season_schedule(
    season: int,
    episodes: int,
    start_date: datetime
) -> List[Tuple[int, int, datetime]]:
    """
    Generate release schedule for a single season.
    
    Args:
        season: Season number
        episodes: Number of episodes in the season
        start_date: Start date for the season
        
    Returns:
        List of tuples (season, episode, release_date)
    """
    schedule = []
    current_date = start_date
    
    for episode in range(1, episodes + 1):
        schedule.append((season, episode, current_date))
        # Move to next release day
        current_date = get_next_release_day(current_date + timedelta(days=1))
    
    return schedule


def generate_full_schedule(
    start_date: datetime = START_DATE,
    seasons: int = TOTAL_SEASONS,
    episodes_per_season: int = EPISODES_PER_SEASON
) -> List[Tuple[int, int, datetime]]:
    """
    Generate complete release schedule for all seasons.
    
    Args:
        start_date: Starting date for season 1, episode 1
        seasons: Total number of seasons to generate
        episodes_per_season: Number of episodes per season
        
    Returns:
        List of tuples (season, episode, release_date)
    """
    full_schedule = []
    current_date = start_date
    
    for season in range(1, seasons + 1):
        season_schedule = generate_season_schedule(
            season,
            episodes_per_season,
            current_date
        )
        full_schedule.extend(season_schedule)
        
        # Start next season after last episode of current season
        if season_schedule:
            current_date = get_next_release_day(season_schedule[-1][2] + timedelta(days=1))
    
    return full_schedule


def format_schedule_entry(season: int, episode: int, release_date: datetime) -> str:
    """
    Format a schedule entry for output.
    
    Args:
        season: Season number
        episode: Episode number
        release_date: Release date and time
        
    Returns:
        Formatted schedule string
    """
    date_str = release_date.strftime("%Y-%m-%d")
    time_str = release_date.strftime("%H:%M")
    day_name = release_date.strftime("%A")
    
    return f"S{season:02d}E{episode:03d} | {date_str} {time_str} UTC | {day_name}"


def save_schedule(
    schedule: List[Tuple[int, int, datetime]],
    output_file: Path
) -> None:
    """
    Save the schedule to a text file.
    
    Args:
        schedule: List of schedule entries
        output_file: Path to output file
    """
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("PR-CYBR-P0D Release Schedule\n")
        f.write("=" * 60 + "\n")
        f.write("Generated: " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") + "\n")
        f.write("Pattern: Monday/Wednesday/Friday at 06:00 UTC\n")
        f.write("=" * 60 + "\n\n")
        
        current_season = None
        for season, episode, release_date in schedule:
            # Add season header when season changes
            if season != current_season:
                if current_season is not None:
                    f.write("\n")
                f.write(f"Season {season}\n")
                f.write("-" * 60 + "\n")
                current_season = season
            
            f.write(format_schedule_entry(season, episode, release_date) + "\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Total Episodes: {len(schedule)}\n")
        f.write(f"Total Seasons: {TOTAL_SEASONS}\n")
        f.write("=" * 60 + "\n")


def main():
    """Main entry point for the schedule generation script."""
    print("=" * 60)
    print("PR-CYBR-P0D Release Schedule Generator")
    print("=" * 60)
    
    print(f"\n📅 Generating schedule for {TOTAL_SEASONS} seasons...")
    print(f"   Episodes per season: {EPISODES_PER_SEASON}")
    print(f"   Release pattern: Monday/Wednesday/Friday at {RELEASE_TIME} UTC")
    print(f"   Starting from: {START_DATE.strftime('%Y-%m-%d')}")
    
    # Generate schedule
    schedule = generate_full_schedule()
    
    print(f"\n✅ Generated {len(schedule)} episode release dates")
    
    # Save to file
    save_schedule(schedule, SCHEDULE_FILE)
    print(f"💾 Schedule saved to: {SCHEDULE_FILE}")
    
    # Display first and last few entries
    print("\n📊 Preview (first 5 entries):")
    for season, episode, release_date in schedule[:5]:
        print(f"   {format_schedule_entry(season, episode, release_date)}")
    
    print("\n📊 Preview (last 5 entries):")
    for season, episode, release_date in schedule[-5:]:
        print(f"   {format_schedule_entry(season, episode, release_date)}")
    
    print("\n" + "=" * 60)
    print("✅ Schedule generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
