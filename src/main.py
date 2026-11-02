"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List, Tuple
from src.recommender import load_songs, recommend_songs, Song, UserProfile, Recommender
from src.table_formatter import format_recommendations_table


def calculate_max_score(weights: Dict = None) -> float:
    """Calculate maximum possible score based on weights."""
    if weights is None:
        weights = {'genre': 2.0, 'mood': 1.5, 'energy': 1.0}
    return weights['genre'] + weights['mood'] + weights['energy']


def format_recommendations(recommendations: list, weights: Dict = None) -> str:
    """Format recommendations into a clean, readable terminal display."""
    max_score = calculate_max_score(weights)
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
        output.append(f"   Score: {score:.2f} / {max_score:.2f}")
        output.append(f"   ✓ Why: {' + '.join(reasons)}")
        output.append("   " + "-"*66)

    output.append("="*70 + "\n")
    return "\n".join(output)


def main() -> None:
    songs = load_songs("./data/songs.csv")

    # Define multiple user profiles for testing
    user_profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
        },
        "Conflicting Preferences (Edge Case)": {
            "favorite_genre": "pop",
            "favorite_mood": "intense",
            "target_energy": 0.95,
        },
        "Mood-Only Seeker (No Genre)": {
            "favorite_genre": "",
            "favorite_mood": "relaxed",
            "target_energy": 0.5,
        },
    }

    # Test each profile
    for profile_name, user_prefs in user_profiles.items():
        print(f"\n\n{'='*70}")
        print(f"TESTING: {profile_name}")
        print(f"Preferences: Genre={user_prefs['favorite_genre']}, Mood={user_prefs['favorite_mood']}, Energy={user_prefs['target_energy']}")
        print(f"{'='*70}")

        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(format_recommendations(recommendations))


def run_weight_experiment(songs: list) -> None:
    """Test system sensitivity to weight changes."""
    print("\n\n" + "="*70)
    print("WEIGHT SENSITIVITY EXPERIMENT")
    print("="*70)

    # Original weights
    original_weights = {'genre': 2.0, 'mood': 1.5, 'energy': 1.0}

    # Experimental weights (mood doubled, genre halved)
    experimental_weights = {'genre': 1.0, 'mood': 3.0, 'energy': 1.5}

    test_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    print(f"\nProfile: Pop + Happy + 0.8 Energy")
    print(f"\nOriginal weights: {original_weights}")
    print("Top 3 recommendations:")
    recs_original = recommend_songs(test_profile, songs, k=3, weights=original_weights)
    for i, (song, score, explanation) in enumerate(recs_original, 1):
        print(f"  {i}. {song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")

    print(f"\nExperimental weights (doubled mood, halved genre): {experimental_weights}")
    print("Top 3 recommendations:")
    recs_experimental = recommend_songs(test_profile, songs, k=3, weights=experimental_weights)
    for i, (song, score, explanation) in enumerate(recs_experimental, 1):
        print(f"  {i}. {song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")

    print("\n📊 Analysis:")
    print("- Original: Genre-weighted system prioritizes 'pop' heavily")
    print("- Experimental: Mood-weighted system allows non-pop songs if they match mood/energy")
    print("- This shows how much the scoring is dominated by genre preference!")


def demonstrate_ranking_modes(songs: List[Song]) -> None:
    """Demonstrate different ranking modes: balanced, diverse, genre-focused."""
    print("\n\n" + "="*70)
    print("RANKING MODES COMPARISON")
    print("="*70)

    test_profile = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False
    )

    # Convert dict songs to Song objects
    song_objects = [
        Song(
            id=int(s['id']),
            title=s['title'],
            artist=s['artist'],
            genre=s['genre'],
            mood=s['mood'],
            energy=float(s['energy']),
            tempo_bpm=float(s['tempo_bpm']),
            valence=float(s.get('valence', 0.5)),
            danceability=float(s.get('danceability', 0.5)),
            acousticness=float(s.get('acousticness', 0.5))
        )
        for s in songs
    ]

    modes = ["balanced", "diverse", "genre-focused"]

    for mode in modes:
        print(f"\n\n📊 Mode: {mode.upper()}")
        print(f"{'='*70}")

        recommender = Recommender(song_objects, mode=mode)
        results = recommender.recommend(test_profile, k=5)

        print(f"\nProfile: Pop + Happy + 0.8 Energy")
        print(f"Top 5 recommendations ({mode}):\n")

        for rank, song in enumerate(results, 1):
            explanation = recommender.explain_recommendation(test_profile, song)
            print(f"  {rank}. {song.title} ({song.artist})")
            print(f"     Genre: {song.genre} | Mood: {song.mood}")
            print(f"     ✓ {explanation}\n")


def demonstrate_table_output(songs: List[Dict]) -> None:
    """Demonstrate tabulated output format."""
    print("\n\n" + "="*70)
    print("TABLE FORMAT OUTPUT")
    print("="*70)

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n")
    print(format_recommendations_table(recommendations))
    print("\n")


if __name__ == "__main__":
    main()

    # Uncomment to run weight experiment:
    # songs = load_songs("./data/songs.csv")
    # run_weight_experiment(songs)

    # Uncomment to demonstrate ranking modes:
    # songs = load_songs("./data/songs.csv")
    # demonstrate_ranking_modes(songs)

    # Uncomment to see table format output:
    # songs = load_songs("./data/songs.csv")
    # demonstrate_table_output(songs)
