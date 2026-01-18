#!/usr/bin/env python3
"""
Skill Registrar - Helper script for parsing SKILL.md and updating marketplace.json
"""

import json
import re
import sys
from pathlib import Path


def parse_skill_frontmatter(skill_path: Path) -> dict:
    """
    Parse YAML frontmatter from SKILL.md file

    Args:
        skill_path: Path to the skill directory

    Returns:
        dict with 'name' and 'description' keys

    Raises:
        FileNotFoundError: If SKILL.md doesn't exist
        ValueError: If frontmatter is invalid or missing required fields
    """
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    content = skill_md.read_text(encoding="utf-8")

    # Extract YAML frontmatter between --- markers
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid SKILL.md format: missing YAML frontmatter in {skill_md}")

    frontmatter = match.group(1)

    # Parse YAML-like key-value pairs
    metadata = {}
    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    # Validate required fields
    if "name" not in metadata:
        raise ValueError(f"SKILL.md missing required field 'name' in {skill_md}")
    if "description" not in metadata:
        raise ValueError(f"SKILL.md missing required field 'description' in {skill_md}")

    return {
        "name": metadata["name"],
        "description": metadata["description"],
        "raw_metadata": metadata
    }


def extract_keywords(description: str, count: int = 6) -> list:
    """
    Extract relevant keywords from description

    Args:
        description: Skill description text
        count: Number of keywords to extract (default: 6)

    Returns:
        List of keywords
    """
    # Simple keyword extraction based on common technical terms
    # Remove common words and extract meaningful terms

    # Common tech/dev terms to look for
    tech_terms = [
        "api", "ui", "ux", "design", "code", "test", "debug", "git",
        "documentation", "tracking", "recording", "notes", "productivity",
        "automation", "workflow", "development", "web", "frontend", "backend",
        "database", "ai", "ml", "parsing", "formatting", "conversion",
        "cli", "tool", "helper", "utility", "generator", "analyzer",
        "monitor", "deploy", "build", "refactor", "review"
    ]

    # Convert description to lowercase
    desc_lower = description.lower()

    # Find matching tech terms
    found_keywords = [term for term in tech_terms if term in desc_lower]

    # If not enough keywords, extract meaningful words from description
    if len(found_keywords) < count:
        # Extract words that are longer than 4 characters
        words = re.findall(r'\b[a-z]{4,}\b', desc_lower)
        # Remove common stop words
        stop_words = {"this", "that", "with", "from", "user", "when", "need", "help", "provide"}
        words = [w for w in words if w not in stop_words and w not in found_keywords]
        found_keywords.extend(words[:count - len(found_keywords)])

    return found_keywords[:count]


def infer_category(description: str) -> str:
    """
    Infer skill category from description

    Args:
        description: Skill description text

    Returns:
        Category string (productivity|design|development|utilities)
    """
    desc_lower = description.lower()

    # Define category keywords
    category_rules = {
        "productivity": ["note", "track", "organize", "workflow", "record", "task", "manage"],
        "design": ["ui", "ux", "style", "visual", "design", "graphic", "layout"],
        "development": ["code", "test", "debug", "api", "develop", "build", "refactor", "review"],
        "utilities": ["tool", "helper", "utility", "converter", "formatter", "generator"]
    }

    # Score each category
    scores = {category: 0 for category in category_rules}

    for category, keywords in category_rules.items():
        for keyword in keywords:
            if keyword in desc_lower:
                scores[category] += 1

    # Return category with highest score
    return max(scores, key=scores.get)


def update_marketplace_json(
    marketplace_path: Path,
    skill_name: str,
    skill_metadata: dict,
    owner_name: str
) -> bool:
    """
    Update marketplace.json with new skill plugin configuration

    Args:
        marketplace_path: Path to marketplace.json file
        skill_name: Name of the skill
        skill_metadata: Metadata extracted from SKILL.md
        owner_name: Owner name from marketplace.json root

    Returns:
        True if updated, False if already exists (not modified)
    """
    # Read marketplace.json
    with open(marketplace_path, "r", encoding="utf-8") as f:
        marketplace = json.load(f)

    # Generate plugin configuration
    keywords = extract_keywords(skill_metadata["description"])
    category = infer_category(skill_metadata["description"])

    plugin_config = {
        "name": skill_name,
        "source": f"./.claude/skills/{skill_name}",
        "description": skill_metadata["description"],
        "version": "1.0.0",
        "author": {
            "name": owner_name
        },
        "keywords": keywords,
        "category": category,
        "strict": False
    }

    # Check if skill already exists
    plugins = marketplace.get("plugins", [])
    existing_index = None

    for i, plugin in enumerate(plugins):
        if plugin.get("name") == skill_name:
            existing_index = i
            break

    # Update or append
    if existing_index is not None:
        plugins[existing_index] = plugin_config
        action = "updated"
    else:
        plugins.append(plugin_config)
        action = "added"

    marketplace["plugins"] = plugins

    # Write back to file
    with open(marketplace_path, "w", encoding="utf-8") as f:
        json.dump(marketplace, f, indent=2, ensure_ascii=False)

    return action


def main():
    """CLI entry point for testing"""
    if len(sys.argv) < 2:
        print("Usage: python register_skill.py <skill-name>")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Paths
    # From script location: .claude/skills/skill-registrar/scripts/register_skill.py
    # To project root: go up 5 levels
    project_root = Path(__file__).parent.parent.parent.parent.parent
    skills_dir = project_root / ".claude" / "skills"
    marketplace_path = project_root / ".claude-plugin" / "marketplace.json"

    skill_path = skills_dir / skill_name

    try:
        # Parse SKILL.md
        print(f"Parsing {skill_path}/SKILL.md...")
        metadata = parse_skill_frontmatter(skill_path)
        print(f"  Name: {metadata['name']}")
        print(f"  Description: {metadata['description'][:80]}...")

        # Read marketplace.json for owner name
        with open(marketplace_path, "r", encoding="utf-8") as f:
            marketplace = json.load(f)
        owner_name = marketplace.get("owner", {}).get("name", "unknown")

        # Update marketplace.json
        print(f"\nUpdating {marketplace_path}...")
        action = update_marketplace_json(marketplace_path, skill_name, metadata, owner_name)
        print(f"  Skill {action} successfully!")

        # Show extracted info
        keywords = extract_keywords(metadata["description"])
        category = infer_category(metadata["description"])
        print(f"\nExtracted metadata:")
        print(f"  Keywords: {', '.join(keywords)}")
        print(f"  Category: {category}")

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
