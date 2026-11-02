"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def format_recommendations(recommendations: list) -> str:
    """Format recommendations into a clean, readable terminal display."""
    output = []
    output.append("\n" + "="*70)
    output.append(" 🎵 TOP RECOMMENDATIONS")
    output.append("="*70)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        # Extract reasons from explanation string
        reasons = explanation.split(' + ')

        output.append(f"\n#{rank} | {song['title'].upper()}")
        output.append(f"   Artist: {song.get('artist', 'Unknown')}")
        output.append(f"   Genre: {song.get('genre', 'Unknown')} | Mood: {song.get('mood', 'Unknown')}")
        output.append(f"   Score: {score:.2f} / 4.50")
        output.append(f"   ✓ Why: {' + '.join(reasons)}")
        output.append("   " + "-"*66)

    output.append("="*70 + "\n")
    return "\n".join(output)


def main() -> None:
    songs = load_songs("./data/songs.csv") 

    # Example user profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Display formatted recommendations
    print(format_recommendations(recommendations))


if __name__ == "__main__":
    main()
