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
| French            | ✅✅❌❌❌ |
| Mandarin Chinese  | ✅✅❌❌❌ |
| Spanish           | ✅✅❌❌❌ |
| German            | ✅✅❌❌❌ |
| Italian           | ✅✅❌❌❌ |
| Japanese          | ✅✅❌❌❌ |
| Russian           | ✅✅❌❌❌ |
| Portuguese        | ✅✅❌❌❌ |
| Korean            | ✅✅❌❌❌ |


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

<div style="text-align:center;">
  <p><b>das Haus</b> (Häuser)</p>
  <p>
    <span style="color:#008080;">Er</span> 
    <span style="color:#B22222;">kauft</span> 
    <span style="color:#696969;">ein</span> 
    <u><span style="color:#2E8B57;">Haus</span></u> 
    <span style="color:#696969;">für</span> 
    <span style="color:#696969;">seine</span> 
    <span style="color:#2E8B57;">Familie</span>.
  </p>
</div>

**Back:**

<div style="text-align:center;">
  <p><b>Haus</b> – house (building for living in)</p>
  <p>He buys a house for his family.</p>
  <p>[Sentence Audio]</p>
</div>

---

### Example: **Japanese (日本語)**

**Front:**

<div style="text-align:center;">
  <p><b>食べる</b></p>
  <p>
    <span style="color:#FF8C00;">毎日</span> 
    <u><span style="color:#B22222;">食べる</span></u> 
    <span style="color:#2E8B57;">野菜</span> 
    <span style="color:#696969;">を</span> 
    <span style="color:#B22222;">食べる</span> 
    <span style="color:#696969;">こと</span> 
    <span style="color:#696969;">が</span> 
    <span style="color:#1E90FF;">大切</span> 
    <span style="color:#696969;">です</span>。
  </p>
</div>

**Back:**

<div style="text-align:center;">
  <p><b>たべる (taberu)</b> – to eat</p>
  <p>食 (eat) + べる</p>
  <p>It is important to eat vegetables every day.</p>
  <p>[Sentence Audio]</p>
</div>

---

## Repository Contents

* 📂 **generator** – Script used to generate sentences 
* 📂 **corpora** – raw sentence collections for each language
* 📂 **frequency_lists** – lemmatized, frequency-ranked vocabulary
* 📂 **flashcards** – Sentence lists and Anki decks 

---
