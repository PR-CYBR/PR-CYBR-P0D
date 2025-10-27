#!/usr/bin/env python3
"""
Episode Code Name Generator

Generates systematic, thematic code names for podcast episodes.
Format: P0D-S<season>-E<episode>-AXIS-<symbol>

This script can be re-run to regenerate or reassign code names programmatically.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple


# Configuration
EPISODES_PER_SEASON = 52
TOTAL_SEASONS = 17
CODE_PREFIX = "P0D"
CODE_THEME = "AXIS"

# Symbol sets for code names (thematic cybersecurity/tech terms)
SYMBOL_SETS = {
    "encryption": [
        "CIPHER", "ENCRYPT", "HASH", "TOKEN", "KEY", "SALT",
        "AES", "RSA", "TLS", "SSL", "PKI", "CERT"
    ],
    "security": [
        "FIREWALL", "SHIELD", "GUARD", "SENTINEL", "BASTION", "FORTRESS",
        "AEGIS", "BARRIER", "DEFENSE", "PATROL", "WATCH", "VAULT"
    ],
    "attack": [
        "BREACH", "EXPLOIT", "PAYLOAD", "VECTOR", "MALWARE", "PHISH",
        "TROJAN", "WORM", "ROOTKIT", "BACKDOOR", "INJECT", "OVERFLOW"
    ],
    "network": [
        "PACKET", "ROUTER", "GATEWAY", "PROXY", "TUNNEL", "BRIDGE",
        "NODE", "MESH", "FABRIC", "LINK", "HUB", "SWITCH"
    ],
    "data": [
        "STREAM", "BUFFER", "CACHE", "QUEUE", "STACK", "HEAP",
        "BLOCK", "CHUNK", "SHARD", "FRAME", "SEGMENT", "BYTE"
    ],
    "protocol": [
        "HTTP", "TCP", "UDP", "DNS", "DHCP", "FTP",
        "SMTP", "SSH", "SNMP", "ICMP", "BGP", "OSPF"
    ],
    "operation": [
        "SCAN", "PROBE", "TRACE", "QUERY", "FETCH", "PUSH",
        "PULL", "MERGE", "FORK", "CLONE", "PATCH", "BUILD"
    ],
    "status": [
        "ACTIVE", "IDLE", "READY", "ARMED", "ALERT", "LOCKED",
        "SECURE", "OPEN", "CLOSED", "PENDING", "LIVE", "STANDBY"
    ]
}


def generate_symbol_pool(seasons: int, episodes_per_season: int) -> List[str]:
    """
    Generate a pool of unique symbols for all episodes.
    
    Args:
        seasons: Number of seasons
        episodes_per_season: Episodes per season
        
    Returns:
        List of symbol names
    """
    total_episodes = seasons * episodes_per_season
    symbol_pool = []
    
    # Flatten all symbols into a single list
    all_symbols = []
    for category_symbols in SYMBOL_SETS.values():
        all_symbols.extend(category_symbols)
    
    # Remove duplicates and sort
    all_symbols = sorted(set(all_symbols))
    
    # If we need more symbols than available, reuse with numeric suffixes
    if total_episodes > len(all_symbols):
        for i in range(total_episodes):
            base_symbol = all_symbols[i % len(all_symbols)]
            suffix_num = i // len(all_symbols)
            if suffix_num > 0:
                symbol_pool.append(f"{base_symbol}{suffix_num}")
            else:
                symbol_pool.append(base_symbol)
    else:
        symbol_pool = all_symbols[:total_episodes]
    
    return symbol_pool


def generate_code_name(season: int, episode: int, symbol: str) -> str:
    """
    Generate a code name for an episode.
    
    Args:
        season: Season number
        episode: Episode number
        symbol: Symbol/theme word
        
    Returns:
        Formatted code name
    """
    return f"{CODE_PREFIX}-S{season:02d}-E{episode:03d}-{CODE_THEME}-{symbol}"


def generate_all_code_names(
    seasons: int = TOTAL_SEASONS,
    episodes_per_season: int = EPISODES_PER_SEASON,
    randomize: bool = False
) -> List[Tuple[int, int, str, str]]:
    """
    Generate code names for all episodes.
    
    Args:
        seasons: Number of seasons
        episodes_per_season: Episodes per season
        randomize: Whether to randomize symbol assignment
        
    Returns:
        List of tuples (season, episode, code_name, symbol)
    """
    symbols = generate_symbol_pool(seasons, episodes_per_season)
    
    if randomize:
        random.shuffle(symbols)
    
    code_names = []
    symbol_index = 0
    
    for season in range(1, seasons + 1):
        for episode in range(1, episodes_per_season + 1):
            symbol = symbols[symbol_index]
            code_name = generate_code_name(season, episode, symbol)
            code_names.append((season, episode, code_name, symbol))
            symbol_index += 1
    
    return code_names


def save_code_names(
    code_names: List[Tuple[int, int, str, str]],
    output_dir: Path
) -> None:
    """
    Save code names to files.
    
    Args:
        code_names: List of code name tuples
        output_dir: Directory to save files
    """
    output_dir.mkdir(exist_ok=True)
    
    # Save as JSON
    json_file = output_dir / "episode-code-names.json"
    data = {
        "generated_at": "2024-01-01T00:00:00Z",
        "prefix": CODE_PREFIX,
        "theme": CODE_THEME,
        "total_episodes": len(code_names),
        "episodes": [
            {
                "season": season,
                "episode": episode,
                "code_name": code_name,
                "symbol": symbol
            }
            for season, episode, code_name, symbol in code_names
        ]
    }
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Save as text
    txt_file = output_dir / "episode-code-names.txt"
    with open(txt_file, 'w') as f:
        f.write("PR-CYBR-P0D Episode Code Names\n")
        f.write("=" * 70 + "\n")
        f.write("Format: P0D-S<season>-E<episode>-AXIS-<symbol>\n")
        f.write("=" * 70 + "\n\n")
        
        current_season = None
        for season, episode, code_name, symbol in code_names:
            if season != current_season:
                if current_season is not None:
                    f.write("\n")
                f.write(f"Season {season}\n")
                f.write("-" * 70 + "\n")
                current_season = season
            
            f.write(f"E{episode:03d}: {code_name}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Total Episodes: {len(code_names)}\n")
        f.write("=" * 70 + "\n")


def display_sample_codes(code_names: List[Tuple[int, int, str, str]], count: int = 10):
    """
    Display sample code names.
    
    Args:
        code_names: List of code name tuples
        count: Number of samples to display
    """
    print("\n📋 Sample Code Names:")
    for season, episode, code_name, symbol in code_names[:count]:
        print(f"   S{season:02d}E{episode:03d}: {code_name}")


def display_symbol_distribution(code_names: List[Tuple[int, int, str, str]]):
    """
    Display symbol category distribution.
    
    Args:
        code_names: List of code name tuples
    """
    # Count symbols by category
    category_counts = {category: 0 for category in SYMBOL_SETS.keys()}
    
    for _, _, _, symbol in code_names:
        # Find which category this symbol belongs to
        for category, symbols in SYMBOL_SETS.items():
            if any(s in symbol for s in symbols):
                category_counts[category] += 1
                break
    
    print("\n📊 Symbol Distribution by Category:")
    for category, count in sorted(category_counts.items()):
        print(f"   {category.capitalize()}: {count} episodes")


def main():
    """Main entry point for code name generation."""
    print("=" * 70)
    print("PR-CYBR-P0D Episode Code Name Generator")
    print("=" * 70)
    
    print(f"\n🏷️  Generating code names for {TOTAL_SEASONS} seasons...")
    print(f"   Episodes per season: {EPISODES_PER_SEASON}")
    print(f"   Format: {CODE_PREFIX}-S##-E###-{CODE_THEME}-<SYMBOL>")
    
    # Generate code names
    code_names = generate_all_code_names()
    
    print(f"\n✅ Generated {len(code_names)} unique code names")
    
    # Save to files
    output_dir = Path("episodes")
    save_code_names(code_names, output_dir)
    
    print(f"💾 Saved to:")
    print(f"   - episodes/episode-code-names.json")
    print(f"   - episodes/episode-code-names.txt")
    
    # Display samples
    display_sample_codes(code_names, 10)
    display_symbol_distribution(code_names)
    
    print("\n" + "=" * 70)
    print("✅ Code name generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
