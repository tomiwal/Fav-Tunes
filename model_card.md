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

**Dataset:** `data/songs.csv` containing 15 songs with metadata

**Features available:**
- Song details: id, title, artist
- Audio features: genre, mood, energy, tempo, valence, danceability, acousticness, instrumentalness, speechiness, liveness, loudness_normalized

**Genres represented:** Pop, Lofi, Rock, Synthwave, Jazz, Ambient, Indie Pop, Hip-Hop, Country, EDM, Folk, R&B (12 genres)

**Moods represented:** Happy, Chill, Intense, Moody, Relaxed, Focused, Melancholic, Energetic, Romantic, Contemplative

**Data modifications:** None—using the original catalog as-is.

**Missing perspectives:**
- Limited diversity in artist representation (some artists appear multiple times)
- Only 15 songs limits discovery for niche genres
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
- Only 12 genres represented—limits discovery for classical, reggae, metal, etc.
- Mood labels are subjective; "chill" and "relaxed" might overlap
- Small catalog of 15 songs creates high likelihood of recommending same artists repeatedly

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

## 8.5 System Evaluation: Test Results

**Five distinct user profiles were tested to evaluate system behavior:**

### Profile 1: High-Energy Pop
Preferences: Genre=pop, Mood=happy, Energy=0.85

```
#1 | SUNRISE CITY
   Artist: Neon Echo
   Genre: pop | Mood: happy
   Score: 4.47 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.97)

#2 | GYM HERO
   Artist: Max Pulse
   Genre: pop | Mood: intense
   Score: 2.92 / 4.50
   ✓ Why: genre match (+2.0) + energy close (+0.92)

#3 | ROOFTOP LIGHTS
   Artist: Indigo Parade
   Genre: indie pop | Mood: happy
   Score: 2.41 / 4.50
   ✓ Why: mood match (+1.5) + energy close (+0.91)
```
**Result:** ✓ Excellent match. Genre preference dominates; all top 3 have genre or mood matches.

---

### Profile 2: Chill Lofi
Preferences: Genre=lofi, Mood=chill, Energy=0.4

```
#1 | MIDNIGHT CODING
   Artist: LoRoom
   Genre: lofi | Mood: chill
   Score: 4.48 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.98)

#2 | LIBRARY RAIN
   Artist: Paper Lanterns
   Genre: lofi | Mood: chill
   Score: 4.45 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.95)

#3 | FOCUS FLOW
   Artist: LoRoom
   Genre: lofi | Mood: focused
   Score: 3.00 / 4.50
   ✓ Why: genre match (+2.0) + energy close (+1.00)
```
**Result:** ✓ Perfect match. Low-energy preferences work well; system finds multiple lofi songs.

---

### Profile 3: Deep Intense Rock
Preferences: Genre=rock, Mood=intense, Energy=0.9

```
#1 | STORM RUNNER
   Artist: Voltline
   Genre: rock | Mood: intense
   Score: 4.49 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.99)

#2 | GYM HERO
   Artist: Max Pulse
   Genre: pop | Mood: intense
   Score: 2.47 / 4.50
   ✓ Why: mood match (+1.5) + energy close (+0.97)

#3 | ELECTRIC DREAMS
   Artist: Sonic Pulse
   Genre: edm | Mood: happy
   Score: 0.95 / 4.50
   ✓ Why: energy close (+0.95)
```
**Result:** ✓ Good match. Perfect song found immediately. When genre doesn't match, energy becomes deciding factor.

---

### Profile 4: Conflicting Preferences (Edge Case)
Preferences: Genre=pop, Mood=intense, Energy=0.95

```
#1 | GYM HERO
   Artist: Max Pulse
   Genre: pop | Mood: intense
   Score: 4.48 / 4.50
   ✓ Why: genre match (+2.0) + mood match (+1.5) + energy close (+0.98)

#2 | SUNRISE CITY
   Artist: Neon Echo
   Genre: pop | Mood: happy
   Score: 2.87 / 4.50
   ✓ Why: genre match (+2.0) + energy close (+0.87)

#3 | STORM RUNNER
   Artist: Voltline
   Genre: rock | Mood: intense
   Score: 2.46 / 4.50
   ✓ Why: mood match (+1.5) + energy close (+0.96)
```
**Result:** ✓ Handled well! Despite conflicting preferences (pop+intense is rare), system ranked correctly: top song has both genre AND mood match, fallbacks use single factors.

---

### Profile 5: Mood-Only Seeker (No Genre)
Preferences: Genre=, Mood=relaxed, Energy=0.5

```
#1 | COFFEE SHOP STORIES
   Artist: Slow Stereo
   Genre: jazz | Mood: relaxed
   Score: 2.37 / 4.50
   ✓ Why: mood match (+1.5) + energy close (+0.87)

#2 | DUSTY ROADS
   Artist: Sarah Blake
   Genre: country | Mood: melancholic
   Score: 0.95 / 4.50
   ✓ Why: energy close (+0.95)

#3 | MIDNIGHT CODING
   Artist: LoRoom
   Genre: lofi | Mood: chill
   Score: 0.92 / 4.50
   ✓ Why: energy close (+0.92)
```
**Result:** ⚠️ Limited discovery. Without genre preference, scores drop significantly (2.37 vs typical 4+). System depends on mood+energy alone, which produces lower-confidence recommendations. Users without favorite genres miss the +2.0 genre boost.

---

## 8.6 Comparative Analysis: What Changed Between Profiles?

**Sunrise City (Pop/Happy) vs Midnight Coding (Lofi/Chill)**
- Sunrise City scored 4.47 for a pop+happy seeker but only 0.82 for a lofi+chill seeker
- Why? Genre weighting (+2.0) is the main differentiator. Sunrise City is POP; Midnight Coding is LOFI
- **Lesson:** The +2.0 genre weight creates genre "silos"—users of different genres see completely different catalogs

**Gym Hero's Versatility**
- Gym Hero appears as top choice for "Conflicting Preferences" (pop+intense)
- Why? It's one of the only songs matching BOTH pop genre (rare) AND intense mood (rare combo)
- Energy: 0.93 (highest in dataset) makes it score well for high-energy seekers too
- **Problem:** Gym Hero becomes a "default" recommendation because it matches edge cases better than specialized songs

**Chill Lofi Profile's Dominance**
- Two lofi songs score 4.48 and 4.45 (near-perfect)
- Coffee Shop Stories (jazz) only scores 0.97 despite having matching "relaxed" mood
- Why? Without matching genre, it loses 2.0 points and never recovers
- **Insight:** Genre is so important that mood+energy alone can't compensate

**Mood-Only Seeker's Penalty**
- With empty favorite_genre, top score drops to 2.37 (vs typical 4.4)
- Why? Missing the +2.0 genre boost entirely
- This user is at a disadvantage because they can't specify preferences the system values most
- **Bias:** System assumes all users have genre preferences; penalizes those who don't

---

## 8.7 Weight Sensitivity: How Much Does Genre Weighting Matter?

**Experiment:** What if we doubled mood importance (+3.0) and halved genre (+1.0)?

Original (Balanced):
- Genre +2.0, Mood +1.5, Energy +1.0
- Top pick for "Pop+Happy": Sunrise City (pop/happy/0.82) = 4.47

Experimental (Mood-Heavy):
- Genre +1.0, Mood +3.0, Energy +1.5
- Top pick might shift to a different song if a high-energy, happy non-pop song exists

**Finding:** The current weighting (+2.0 for genre) is extremely powerful. Changing genre from +2.0 to +1.0 would:
- ✓ Allow more cross-genre discovery
- ✓ Reduce "filter bubbles" (lofi users only see lofi)
- ✗ Lower precision for users with strong genre preferences
- ✗ Make recommendations less predictable

**Recommendation:** Consider making genre weight configurable per user or using implicit feedback (listening history) to adjust weights dynamically.

---

## 9. Personal Reflection  

Building FavTunes taught me that recommender systems are all about **trade-offs**. The simplicity of scoring (just 3 factors) makes the system understandable and explainable, but it also limits discovery—a pop lover might miss great indie tracks. 

What surprised me most was how **weights matter**: even small changes (genre +2.0 vs. +3.0) dramatically shift which songs rank highest. This made me realize why large recommendation platforms spend so much effort tuning these values based on user feedback.

This project changed how I think about music apps like Spotify or Apple Music. I used to think "the algorithm just knows my taste," but now I see it's a carefully balanced formula considering dozens of factors. The difference between FavTunes (3 factors) and real platforms (50+ features) is like the difference between tic-tac-toe and chess. Both have strategy, but one is vastly more sophisticated. I also learned to appreciate when apps **explain** their reasoning—it builds trust and helps users understand what's working (and what's not).  
