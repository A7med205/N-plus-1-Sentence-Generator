# nplus1-language-flashcards

## Overview

This open project aims to provides **3,000 frequency-based vocabulary flashcards** for language learners for multiple languages, built on the **n+1 principle**:

> Each new sentence should introduce only *one* new unknown word compared to the learner’s current vocabulary.

### Features

* Covers **10 languages**:

  * English, French, Mandarin Chinese, Spanish, German, Italian, Japanese, Russian, Portuguese, Korean
* Cards contain words, definitions, example sentences, translations and audio
* Example sentences are sourced, based on the rules, from large corpora or generated via language models, followed by human review [Read More](generator/README.md)
* **3K curated cards per language**
* Repository includes corpora, frequency lists, and flashcard decks
* At a pace of **25 new cards/day**, a beginner can finish the full deck in \~4 months

---

## Roadmap

### Phase One – Sentence Lists

1. **Collect corpora:** Public sentence banks such as Tatoeba and OpenSubtitles are sourced for each language.
2. **Build lemma frequency lists:** Usine Stanza (a context aware NLP model) the most frequent lemmas (base or dictionary forms of each word) are extracted from the dataset and sorted by frequency, and part of speech information / multiple definitions for each word are pulled from Wiktionary.
3. **Human vetting of lists:** Erreneous entries are removed and the best definitions are chosen for each word.
4. **Generate sentences:** For each new word, a sentence that contains only preveuously learned words is either sourced from the sentence bank or machine generated.
5. **Final human review:** The quality/naturalness of each example sentence is reviewed by a native speaker.

| Language         | 1 | 2 | 3 | 4 | 5 |
| ---------------- | - | - | - | - | - |
| English          | ✅ | ✅ | 50% | ❌ | ❌ |
| French           | ✅ | ✅ | 50% | ❌ | ❌ |
| Mandarin Chinese | ✅ | ✅ | 50% | ❌ | ❌ |
| Spanish          | ✅ | ✅ | 50% | ❌ | ❌ |
| German           | ✅ | ✅ | 50% | ❌ | ❌ |
| Italian          | ✅ | ✅ | 50% | ❌ | ❌ |
| Japanese         | ✅ | ✅ | 50% | ❌ | ❌ |
| Russian          | ✅ | ❌ | ❌ | ❌ | ❌ |
| Portuguese       | ✅ | ✅ | 50% | ❌ | ❌ |
| Korean           | ✅ | ✅ | 50% | ❌ | ❌ |


### Phase Two – Deck Building


1. **Generate translations, audio and properly formatted flashcards**.
2. **Human review**.

| Language          | 1 | 2 |
|-------------------| - | - |
| English           | ❌ | ❌ |
| French            | ❌ | ❌ |
| Mandarin Chinese  | ❌ | ❌ |
| Spanish           | ❌ | ❌ |
| German            | ❌ | ❌ |
| Italian           | ❌ | ❌ |
| Japanese          | ❌ | ❌ |
| Russian           | ❌ | ❌ |
| Portuguese        | ❌ | ❌ |
| Korean            | ❌ | ❌ |
---

## Flashcard Format

Each flashcard is **HTML-based** (Anki-compatible).

### Example: **German (Deutsch)**

**Front:**

<p align="center">
  <img src="de_front.svg" alt="das Haus example" />
</p>


**Back:**

<p align="center">
  <img src="de_back.svg" alt="das Haus example" />
</p>

---

### Example: **Japanese (日本語)**

**Front:**

<p align="center">
  <img src="ja_front.svg" alt="das Haus example" />
</p>

**Back:**

<p align="center">
  <img src="ja_back.svg" alt="das Haus example" />
</p>

---

## Repository Contents

* 📂 **generator** – Script used to generate sentences 
* 📂 **corpora** – raw sentence collections for each language
* 📂 **frequency_lists** – lemmatized, frequency-ranked vocabulary
* 📂 **flashcards** – Sentence lists and Anki decks 

---
