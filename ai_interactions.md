# AI Interactions Log

## Agentic Workflow (SF8)

**What task did you give the agent?**

Implement all four stretch features for FavTunes to achieve 100% score:
1. Fix model card dataset inaccuracy (claims ~50 songs, 6 genres but actual is 15 songs, 11+ genres)
2. Add edge-case tests for blank energy, non-numeric values, empty genre, and k > catalog size
3. Create diversity/fairness component to penalize artist repetition
4. Build multiple ranking modes (balanced, diverse, genre-focused) using design patterns
5. Create tabulated visual output using ASCII tables

**Prompts used:**

"I need to get from 19/27 to 27/27 (100% score). Help me fix the model card inaccuracy, add comprehensive edge-case tests, implement a diversity penalty system, create multiple ranking modes using the Strategy pattern, and add a table formatter for visual output."

**What did the agent generate or change?**

Files edited:
- `model_card.md`: Updated Section 4 (Data) to reflect actual dataset: 15 songs (not ~50), 12 genres (not 6)
- `tests/test_recommender.py`: Added 3 new test functions:
  - `test_handle_missing_energy_value()`: Verifies blank energy doesn't crash system
  - `test_handle_empty_favorite_genre()`: Tests recommendations without genre preference
  - `test_k_larger_than_catalog()`: Ensures graceful handling when k > available songs
- `src/recommender.py`: Enhanced Recommender class:
  - Added `mode` parameter to constructor (balanced/diverse/genre-focused)
  - Implemented `_apply_diversity_penalty()` to penalize repeated artists
  - Implemented `_apply_genre_emphasis()` to boost/penalize based on genre match
- `src/table_formatter.py`: New file created with:
  - `format_recommendations_table()`: Outputs clean ASCII table with columns for Rank, Title, Artist, Genre, Mood, Score, Explanation
  - `_build_ascii_table()`: Helper to construct bordered ASCII tables
  - `format_comparison_table()`: Cross-profile recommendation comparison
- `src/main.py`: Enhanced with:
  - `calculate_max_score()`: Dynamic score ceiling calculation based on configurable weights
  - Fixed hardcoded "/ 4.50" denominator to use dynamic weights
  - `demonstrate_ranking_modes()`: Shows balanced/diverse/genre-focused output
  - `demonstrate_table_output()`: Shows tabulated format

**What did you verify or fix manually?**

- Verified dataset counts: read songs.csv directly (15 rows, 12 unique genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, country, edm, folk, r&b)
- Tested new edge-case tests locally to confirm they pass
- Reviewed diversity penalty logic: 20% reduction for repeated artists prevents over-recommending same artists
- Confirmed genre-focused mode amplifies genre matches (1.3x) and penalizes non-matches (0.7x)
- Verified table formatter doesn't require external dependencies (uses pure Python string formatting)
- Checked that new functions integrate with existing code without breaking tests

---

## Design Pattern (SF10)

**Which design pattern did you use?**

Strategy Pattern (behavioral pattern) for recommendation ranking modes.

**How did AI help you brainstorm or implement it?**

The agent suggested using the Strategy pattern to encapsulate different ranking algorithms (balanced, diverse, genre-focused) as interchangeable strategies. Instead of conditional logic in the recommend() method, each strategy is a method that transforms the scored results. This allows users to:
- Pick a strategy at initialization: `Recommender(songs, mode="diverse")`
- Switch strategies without modifying core scoring logic
- Add new strategies later without changing existing code
- Test each strategy independently

**How does the pattern appear in your final code?**

Location: `src/recommender.py`, lines 38-67

The Recommender class:
- Accepts `mode` parameter in `__init__()` (strategy selection)
- `recommend()` method calls the appropriate strategy method based on mode:
  - No extra logic: "balanced" (default)
  - `_apply_diversity_penalty()`: "diverse" mode
  - `_apply_genre_emphasis()`: "genre-focused" mode

Each strategy method transforms the scored_songs list before sorting:
```python
if self.mode == "diverse":
    scored = self._apply_diversity_penalty(scored)
elif self.mode == "genre-focused":
    scored = self._apply_genre_emphasis(scored)
```

This decouples ranking logic from the core recommendation flow and makes it easy to add new strategies (e.g., "energy-first", "acousticness-heavy") in the future.
