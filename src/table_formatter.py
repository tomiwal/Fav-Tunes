"""
Table formatter for music recommendations using ASCII tables.
Provides visual output with columns for ranking, song details, score, and explanations.
"""

from typing import List, Tuple, Dict

def format_recommendations_table(recommendations: List[Tuple[Dict, float, str]]) -> str:
    """Format recommendations as a clean ASCII table using tabulate-style formatting."""
    if not recommendations:
        return "No recommendations found."

    # Build table rows
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        max_score = 4.50
        score_pct = int((score / max_score) * 100)
        rows.append([
            rank,
            song['title'],
            song.get('artist', 'Unknown'),
            song.get('genre', 'Unknown'),
            song.get('mood', 'Unknown'),
            f"{score:.2f} / {max_score}",
            explanation
        ])

    return _build_ascii_table([
        ['Rank', 'Title', 'Artist', 'Genre', 'Mood', 'Score', 'Why Recommended'],
        *rows
    ])


def _build_ascii_table(data: List[List]) -> str:
    """Build an ASCII table from raw data."""
    if not data or len(data) == 1:
        return ""

    # Calculate column widths
    col_widths = []
    for col_idx in range(len(data[0])):
        width = max(len(str(row[col_idx])) for row in data)
        col_widths.append(width)

    # Build table
    lines = []

    # Header separator
    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    lines.append(sep)

    # Header
    header = data[0]
    header_row = "|"
    for col_idx, cell in enumerate(header):
        header_row += f" {str(cell).ljust(col_widths[col_idx])} |"
    lines.append(header_row)
    lines.append(sep)

    # Data rows
    for row in data[1:]:
        data_row = "|"
        for col_idx, cell in enumerate(row):
            cell_str = str(cell)
            if col_idx == len(row) - 1 and len(cell_str) > col_widths[col_idx]:
                # Allow explanation column to wrap
                data_row += f" {cell_str[:col_widths[col_idx]]}... |"
            else:
                data_row += f" {cell_str.ljust(col_widths[col_idx])} |"
        lines.append(data_row)

    # Footer separator
    lines.append(sep)

    return "\n".join(lines)


def format_comparison_table(profiles_results: Dict[str, List[Tuple[Dict, float, str]]]) -> str:
    """Compare recommendations across multiple user profiles."""
    lines = ["=" * 100]
    lines.append("RECOMMENDATION COMPARISON ACROSS USER PROFILES")
    lines.append("=" * 100)

    for profile_name, recommendations in profiles_results.items():
        lines.append(f"\n📊 {profile_name}")
        lines.append(format_recommendations_table(recommendations))

    return "\n".join(lines)
