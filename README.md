# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:
The core features that each song will use in my system and the The information my UserProfile will store are Energy, Valence, Genre, Mood. My recommender computes a score for each song with the formula [100 (1 -|reccomended song value| - |fav song value|)]. It calculates how close the different features of the songs are to the users fav song then adds up the points from each features together to give a total closeness match. I'll choose which song to recommend based how high of a point a certain song gets with the calculation. 100 being a perfect match and 0 being a Terrible match


- The system takes in the users fav genre, fav mood, target energy
- It then loads the songs in the csv database
- it loops through the available the songs
- checks if it's a genre is a match +2.0 if yes 0 if no to keep the options broad
- checks if the mood is a match +1.5 if yes 0 if no
- checks the energy distance of the current song to the song the user likes 1.0 * 1 - |user_energy - song_energy| (the higher the better)
- Calculates the total score Genre+Mood+Energy
- Stores the result Song + score + reasons
- checks if there are any more songs left to see to score
- Sorts all songs rank by highest score
- Then returns the top recommendations about top 3 with explantion.

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



