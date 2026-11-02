# 🎧 Model Card: Music Recommender Simulation

## 1. FavTunes
---

## 2. Intended Use  

**FavTunes** recommends new songs that match a user's favorite genre, mood, and energy level. The system learns what "vibe" a user likes and suggests similar tracks from the catalog.

**What it generates:** Personalized music recommendations (top 5 songs) based on user preferences.

**Assumptions about users:** 
- Users have a preferred genre and mood they enjoy
- Users seek songs with similar energy/intensity to what they like
- Recommendations based on these three factors are sufficient for discovery

**Target audience:** Real users exploring music discovery (not just classroom exploration). A user who knows they like "pop + happy + high-energy" can find new tracks that match.  

---

## 3. How the Model Works  

**The Scoring System (Balanced Approach):**

For each song in the catalog, FavTunes calculates a score based on three factors:

1. **Genre Match** (+2.0 points): Does the song's genre match the user's favorite? If yes, add 2 points.
2. **Mood Match** (+1.5 points): Does the song's mood match what the user likes? If yes, add 1.5 points.
3. **Energy Similarity** (+1.0 points): How close is the song's energy to what the user wants? The closer the match, the more points (up to 1.0).

**Maximum Score:** 4.5 points (perfect match on all three factors)

**The Process:**
1. Load all songs from the catalog
2. Score each song using the formula above
3. Rank songs by score (highest to lowest)
4. Return the top 5 recommendations with explanations

**Why this approach?** It's simple, transparent, and gives users a clear reason for each recommendation ("you got this song because it matches your genre AND mood").

---

## 4. Data  

**Dataset:** `data/songs.csv` containing ~50 songs with metadata

**Features available:**
- Song details: id, title, artist
- Audio features: genre, mood, energy, tempo, valence, danceability, acousticness, etc.

**Genres represented:** Pop, Lofi, Rock, Synthwave, Jazz, Ambient

**Moods represented:** Happy, Chill, Intense, Moody, Relaxed, Focused

**Data modifications:** None—using the original catalog as-is.

**Missing perspectives:**
- Limited diversity in artist representation (some artists appear multiple times)
- Only 50 songs limits discovery for niche genres
- No explicit user feedback or listening history data
- Subjective mood labels may not capture all emotional nuances  

---

## 5. Strengths  

**Works well for:**
- Users with **clear, specific tastes** (e.g., "I like pop + happy songs")
- Finding songs within the **same genre and mood** as preferences
- Users who want **explainable recommendations** (each song shows why it matched)

**What it captures correctly:**
- Genre matching is precise and reliable
- Energy similarity finds songs with similar tempo/intensity
- Balanced weighting prevents one factor from dominating
- Mood preferences are well-represented in the dataset

**Intuitive results:**
- A user who likes "pop + happy + high energy" gets recommendations that align with that exact profile
- Transparent scoring helps users trust the recommendations  

---

## 6. Limitations and Bias 

**Features not considered:**
- Artist preferences (no "I like songs by X artist" option)
- Tempo/danceability beyond energy
- Lyrics, language, or cultural context
- Recency or popularity bias
- User's listening history or mood evolution

**Underrepresented genres/moods:**
- Only 6 genres represented—limits discovery for electronic, classical, hip-hop, etc.
- Mood labels are subjective; "chill" and "relaxed" might overlap

**Overfitting risks:**
- Heavily weighted on genre match (+2.0)—users with niche genres get limited recommendations
- Binary genre matching means songs outside favorite genre score 0, even if musically similar

**Potential unfair outcomes:**
- Users who don't know their favorite genre get no genre bonus (starting at 0 points)
- All users weighted equally—doesn't account for individual preference sensitivity
- Energy range constraints (0-1.0) may not capture all music types fairly  

---

## 7. Evaluation  

**User profiles tested:**
1. Pop lover with happy mood and high energy (0.8)
2. Lofi enthusiast with chill mood and low energy (0.4)
3. Rock fan seeking intense, high-energy tracks (0.9)
4. Genre-neutral user (testing mood + energy only)

**What we looked for:**
- Genre/mood matches appear in top results
- Scores reflect the balanced weighting (not just genre-dominated)
- Energy similarity calculations are accurate
- Explanations are clear and match the scores

**Observations:**
- ✓ Genre matching works as expected—pop preferences get pop songs first
- ✓ Energy proximity matters—0.8 target pulls similar-energy songs
- ✓ Mood matching is reliable across all test cases
- Surprise: Without a preferred genre, recommendations still rank well based on mood + energy alone

**Tests run:**
- Manual spot-checks: "Does 'Sunrise City' score higher than 'Storm Runner' for a pop+happy user?"
- Verification: Recalculated scores by hand to validate the scoring formula
- Edge cases: Tested with missing or extreme energy values

---

## 8. Future Work  

**Additional features to consider:**
- Artist preference weighting (boost or penalize specific artists)
- Acoustic vs. electric preference
- Tempo ranges (not just energy)
- Danceability and valence (happiness) as separate scoring factors
- User listening history (what songs they've already rated)

**Better explanations:**
- Show exact energy difference: "Energy is 0.02 away from your target (0.8)"
- Comparative explanations: "More energetic than your usual picks"
- Learning from user feedback to adjust weights over time

**Improving diversity:**
- Add a "penalize similar songs" filter to avoid recommending duplicates
- Boost different artists even if slightly lower scores
- Diversify across energy ranges, not just top genre/mood

**Handling complex tastes:**
- Support multiple favorite genres (e.g., "pop OR indie")
- Learn personalized weights per user (some users value mood more than genre)
- Seasonal preferences (upbeat in winter, chill in summer)
- Collaborative filtering (if many users like songs X and Y together, recommend Y to someone who liked X)  

---

## 9. Personal Reflection  

Building FavTunes taught me that recommender systems are all about **trade-offs**. The simplicity of scoring (just 3 factors) makes the system understandable and explainable, but it also limits discovery—a pop lover might miss great indie tracks. 

What surprised me most was how **weights matter**: even small changes (genre +2.0 vs. +3.0) dramatically shift which songs rank highest. This made me realize why large recommendation platforms spend so much effort tuning these values based on user feedback.

This project changed how I think about music apps like Spotify or Apple Music. I used to think "the algorithm just knows my taste," but now I see it's a carefully balanced formula considering dozens of factors. The difference between FavTunes (3 factors) and real platforms (50+ features) is like the difference between tic-tac-toe and chess. Both have strategy, but one is vastly more sophisticated. I also learned to appreciate when apps **explain** their reasoning—it builds trust and helps users understand what's working (and what's not).  
