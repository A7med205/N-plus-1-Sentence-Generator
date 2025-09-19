# nplus1-language-flashcards

## Overview

This open project aims to provides **3,000 frequency-based vocabulary flashcards** for multiple languages, built on the **n+1 principle**:

> Each new sentence should contain only *one* additional unknown word compared to the learner’s current vocabulary.

### Features

* Covers **10 languages**:

  * English, French, Mandarin Chinese, Spanish, German, Italian, Japanese, Russian, Portuguese, Korean
* Sentences and vocabulary are sourced from large corpora or generated via language models, followed by human review
* **3K curated cards per language**
* Repository includes corpora, frequency lists, and flashcard decks
* At a pace of **25 new cards/day**, a beginner can finish the full deck in \~4 months

---

## Roadmap

### Phase One – Sentence Lists

1. Collect corpora
2. Build lemma frequency lists
3. Human vetting of lists
4. Generate sentences (via corpus or LLM)
5. Final human review

| Language          | Status |
|-------------------|--------|
| English           | ✅✅❌❌❌ |
| French            | ✅❌❌❌❌ |
| Mandarin Chinese  | ✅❌❌❌❌ |
| Spanish           | ✅✅❌❌❌ |
| German            | ✅✅❌❌❌ |
| Italian           | ✅✅❌❌❌ |
| Japanese          | ✅✅❌❌❌ |
| Russian           | ✅❌❌❌❌ |
| Portuguese        | ✅✅❌❌❌ |
| Korean            | ✅❌❌❌❌ |


### Phase Two – Deck Building


1. Generate translations & audio
2. Human review

| Language          | Status |
|-------------------|--------|
| English           | ❌❌ |
| French            | ❌❌ |
| Mandarin Chinese  | ❌❌ |
| Spanish           | ❌❌ |
| German            | ❌❌ |
| Italian           | ❌❌ |
| Japanese          | ❌❌ |
| Russian           | ❌❌ |
| Portuguese        | ❌❌ |
| Korean            | ❌❌ |
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
