from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# Balanced Scoring Strategy:
# - Genre match: +2.0 points
# - Mood match: +1.5 points
# - Energy similarity: +1.0 point (based on distance)

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP implementation using balanced scoring: genre (+2.0), mood (+1.5), energy (+1.0)."""
    """For tester.py """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs and return top k recommendations."""
        user_dict = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }

        scored = [
            (song, *score_song(user_dict, song.__dict__))
            for song in self.songs
        ]

        top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
        return [song for song, score, reasons in top_k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return comma-separated reasons why a song was recommended."""
        user_dict = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }

        score, reasons = score_song(user_dict, song.__dict__)
        return ' + '.join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV, converting numeric fields to proper types."""
    songs = []
    numeric_fields = ['id', 'energy', 'tempo_bpm', 'valence', 'danceability',
                      'acousticness', 'instrumentalness', 'speechiness', 'liveness', 'loudness_normalized']

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_fields:
                if field in row:
                    row[field] = float(row[field]) if field != 'id' else int(row[field])
            songs.append(row)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score a song using configurable weights (default: balanced weighting)."""
    if weights is None:
        weights = {'genre': 2.0, 'mood': 1.5, 'energy': 1.0}

    score = 0.0
    reasons = []

    # Genre match
    if song.get('genre', '').lower() == user_prefs.get('favorite_genre', '').lower():
        score += weights['genre']
        reasons.append(f"genre match (+{weights['genre']})")

    # Mood match
    if song.get('mood', '').lower() == user_prefs.get('favorite_mood', '').lower():
        score += weights['mood']
        reasons.append(f"mood match (+{weights['mood']})")

    # Energy similarity: weight × (1 - distance)
    try:
        user_energy = float(user_prefs.get('target_energy', 0.5))
        song_energy = float(song.get('energy', 0.5))
        energy_distance = abs(user_energy - song_energy)
        energy_score = weights['energy'] * (1 - energy_distance)
        score += energy_score
        reasons.append(f"energy close (+{energy_score:.2f})")
    except (ValueError, TypeError):
        pass

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Dict = None) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top k sorted by score with explanations."""
    scored = [(song, *score_song(user_prefs, song, weights)) for song in songs]
    top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    return [(song, score, ' + '.join(reasons)) for song, score, reasons in top_k]
