# 🎵 FavTunes: Music Recommender System

A CLI-first music recommendation engine that suggests songs based on user preferences for **genre**, **mood**, and **energy level**. Built to explore how scoring algorithms work and where bias can hide in real recommender systems.

---

## How It Works

**Balanced Scoring Algorithm:**
- **Genre Match:** +2.0 points (binary match)
- **Mood Match:** +1.5 points (binary match)
- **Energy Similarity:** +1.0 × (1 - distance) (scaled by closeness)

**Maximum Score:** 4.5 points (perfect match on all factors)

**Process:**
1. Load songs from CSV catalog
2. Score each song using the above formula
3. Rank songs by total score (highest first)
4. Return top 5 recommendations with explanations

Each recommendation shows exactly why it matched: `"genre match (+2.0) + mood match (+1.5) + energy close (+0.98)"`

---

## Quick Start

### Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the Recommender

```bash
python -m src.main
```

Output shows top 5 recommendations for 5 different user profiles:
- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Conflicting Preferences (edge case)
- Mood-Only Seeker (no genre preference)

### Run Tests

```bash
pytest
```

---

## Sample Output

```
#1 | SUNRISE CITY
   Artist: Neon Echo
   Genre: pop | Mood: happy
   Score: 4.47 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.97)
```

---

## What I Learned: Key Findings

### ✅ What Works Well
- Clear, transparent scoring explains every recommendation
- Genre matching is precise and reliable
- Energy similarity captures user taste accurately
- Balanced weighting prevents any one factor from dominating

### ⚠️ Limitations Discovered

1. **Genre Weight Dominance:** +2.0 for genre is so powerful it creates "filter bubbles"
   - Pop lovers only see pop songs, even when similar mood/energy songs exist in other genres
   - Lofi listeners are locked into lofi catalog

2. **Genre Preference Required:** Users without a favorite genre lose 2.0 points
   - Mood-only seekers score max 2.37/4.50 vs typical 4.4+
   - System assumes all users have genre preferences (it's not optional)

3. **Dataset Bias:** "Gym Hero" over-represents edge cases
   - One of few pop+intense songs → appears in multiple top recommendations
   - Small 15-song catalog means rare combos become dominant

4. **No Cross-Genre Discovery:** Hard genre matching prevents finding similar songs outside preferred genre
   - A jazz fan might love an indie pop song with relaxed mood, but it never scores high

---

## Experiments

### Weight Sensitivity Test
Changed weights from balanced (genre +2.0) to mood-heavy (genre +1.0, mood +3.0):
- **Result:** Genre weight is extremely influential. Halving it would increase cross-genre discovery but reduce precision for genre-specific users
- **Implication:** Real recommendation systems likely need personalized weights

### Five User Profiles Tested
1. **High-Energy Pop** (0.85 energy) → Top score: 4.47
2. **Chill Lofi** (0.4 energy) → Top score: 4.48
3. **Deep Intense Rock** (0.9 energy) → Top score: 4.49
4. **Conflicting Preferences** (pop+intense, 0.95 energy) → Top score: 4.48
5. **Mood-Only Seeker** (no genre) → Top score: 2.37 ⚠️

---

## Project Structure

```
src/
  ├── recommender.py    # Scoring logic + OOP/functional implementations
  ├── main.py           # CLI with formatted output for multiple profiles
data/
  └── songs.csv         # 15-song catalog
model_card.md           # Detailed evaluation, biases, limitations
```

---

## Deep Dive

For detailed evaluation of system behavior, accuracy, biases, and recommendations for improvement, see **[Model Card](model_card.md)**.

The model card includes:
- Test results for 5 user profiles with full terminal output
- Comparative analysis showing why certain songs rank high
- Weight sensitivity analysis
- Identification of filter bubbles and unfair outcomes

---

## Key Takeaway

Building even a simple recommender reveals how **weights encode preferences** into systems. The +2.0 for genre isn't just a number—it's a design choice that shapes what millions of users discover. Real-world systems like Spotify optimize these weights endlessly, and understanding that tradeoff is critical to recognizing bias in AI.
