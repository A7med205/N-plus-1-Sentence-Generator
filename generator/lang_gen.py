#!/usr/bin/env python3
"""
Language Learning List Generator

Implements a pipeline to:
1) Locate the next unfinished lemma (after skipping the first 500 entries) in a frequency list file.
2) Use an OpenAI model to generate 10 different 5-8 word sentences containing that lemma.
3) Lemmatize those sentences with Stanza, removing punctuation.
4) Select the sentence that introduces the fewest new lemmas relative to those present before the current lemma.
5) Write results to a new list file (copy), appending the sentence to the lemma's line; if new lemmas are needed,
   insert them before the current lemma (and remove moved lemmas from further down the list).

Notes:
- Input list files are named like "1.txt", "2.text", "3.text", etc.
- We do not modify the original file. We always create a new copy with its leading number incremented.
- This script depends on:
    - openai (>=1.0.0): pip install openai
    - stanza: pip install stanza
  Stanza will attempt to download the English models on first run if not present.

CLI:
    python lang_gen.py --steps 3 --file 1.txt --model gpt-5-mini

Public entrypoint:
    generate_language_learning_list(steps: int, filename: str, skip_count: int = 500, language: str = "en", model: str = "gpt-5-mini")

Environment:
    Requires OPENAI_API_KEY set for LLM calls. A fallback generator is provided if the API call fails.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

# --- Optional imports with graceful handling ---
try:
    import stanza  # type: ignore
except Exception:  # pragma: no cover
    stanza = None  # Will handle at runtime


# --------------- Data Structures ---------------

@dataclass
class ListEntry:
    lemma: str
    sentence: Optional[str]  # None if not yet filled


@dataclass
class LemmatizedSentence:
    original: str
    cleaned: str
    tokens: List[str]      # tokens after cleaning
    lemmas: List[str]      # stanza-lemmas corresponding to tokens


# --------------- File Utilities ---------------

def parse_list_file(path: str) -> List[ListEntry]:
    """
    Parse a list file containing one lemma per line. A line may be:
      - "lemma"
      - "lemma\tSentence text..."
    Blank lines are ignored.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"List file not found: {path}")

    entries: List[ListEntry] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n\r")
            if not line.strip():
                continue
            if "\t" in line:
                lemma, sentence = line.split("\t", 1)
                entries.append(ListEntry(lemma=lemma.strip(), sentence=sentence.strip() if sentence.strip() else None))
            else:
                entries.append(ListEntry(lemma=line.strip(), sentence=None))
    return entries


def write_list_file(entries: Sequence[ListEntry], path: str) -> None:
    """
    Write entries to a file. If sentence is present, write 'lemma\tSentence'.
    """
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            if e.sentence:
                f.write(f"{e.lemma}\t{e.sentence}\n")
            else:
                f.write(f"{e.lemma}\n")


def get_next_filename(current_filename: str) -> str:
    """
    Increment the leading integer of the filename, preserving the extension if present.
    Examples:
        1.txt -> 2.txt
        2.text -> 3.text
        99 -> 100.txt (default to .txt if no extension)
    """
    base = os.path.basename(current_filename)
    m = re.match(r"^(\d+)(\.[^.]+)?$", base)
    if not m:
        # Fallback: if the name doesn't match, append or increment a suffix
        name, ext = os.path.splitext(base)
        if name.isdigit():
            nxt = str(int(name) + 1)
            return nxt + (ext if ext else ".txt")
        # No leading digits at all:
        return base + ".next"
    number, ext = m.group(1), m.group(2)
    nxt = str(int(number) + 1)
    return nxt + (ext if ext else ".txt")


# --------------- Step 1: Find next unfinished lemma ---------------

def find_next_undone_lemma(entries: Sequence[ListEntry], skip_count: int = 500) -> Tuple[int, str]:
    """
    Scan entries starting after 'skip_count' lemmas. Return index and lemma of the first entry
    that does not have a sentence yet. Raises ValueError if none found.
    """
    if skip_count < 0:
        skip_count = 0
    start = min(skip_count, len(entries))
    for i in range(start, len(entries)):
        if entries[i].sentence is None:
            return i, entries[i].lemma
    raise ValueError("No unfinished lemma found after the skip region.")


# --------------- Step 2: LLM sentence generation ---------------

def call_openai_generate_sentences(lemma: str, model: str = "gpt-5-mini") -> List[str]:
    """
    Call OpenAI Responses API to generate 10 different sentences containing 'lemma'.
    Each sentence must be between 5 and 8 words (inclusive).
    Returns a list of 10 strings.

    If the API call fails for any reason, a deterministic fallback generator is used.
    """
    word_count = random.randint(5, 8)

    # Build prompt and schema based on user's suggested structure
    developer_text = (
        "You're an expert AI language assistant, analyse the user provided prompt and answer accordingly."
    )
    user_text = (
        f"Produce 10 simple {word_count}-word sentences that must all include the word {lemma}. "
        "Return only the sentences in the JSON fields as specified."
    )

    # Try OpenAI
    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI()
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "input_text",
                            "text": developer_text,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": user_text,
                        }
                    ],
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ten_sentences",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            **{
                                f"sentence{i}": {
                                    "type": "string",
                                    "description": f"The sentence #{i}."
                                }
                                for i in range(1, 11)
                            }
                        },
                        "required": [f"sentence{i}" for i in range(1, 11)],
                        "additionalProperties": False,
                    },
                },
                "verbosity": "medium",
            },
            reasoning={
                "effort": "medium",
                "summary": "auto",
            },
            tools=[],
            store=True,
            include=[
                "reasoning.encrypted_content",
                "web_search_call.action.sources",
            ],
        )

        # Extract JSON text from response
        # The python SDK v1 Responses API returns output in response.output_text or response.output[0]?.content?
        # We handle robustly by checking common locations.
        json_str: Optional[str] = None

        # Try new SDK shape
        # response.output_text may contain already the JSON text
        if hasattr(response, "output_text") and isinstance(response.output_text, str):
            json_str = response.output_text.strip()

        # Some SDK builds place content in response.output or response.data; check generically
        if not json_str:
            candidate = getattr(response, "output", None)
            if candidate and isinstance(candidate, str):
                json_str = candidate.strip()

        # Last resort: convert whole object to string (may fail)
        if not json_str:
            json_str = str(response).strip()

        # Attempt to find JSON object in the string
        json_match = re.search(r"\{.*\}", json_str, flags=re.S)
        if not json_match:
            raise ValueError("Failed to locate JSON object in LLM response.")
        data = json.loads(json_match.group(0))

        sentences = [data[f"sentence{i}"] for i in range(1, 11)]
        # Basic normalization and deduplication while preserving order
        normed = []
        seen = set()
        for s in sentences:
            s_clean = " ".join(str(s).strip().split())
            if s_clean and s_clean.lower() not in seen:
                normed.append(s_clean)
                seen.add(s_clean.lower())

        # Ensure 10 items: if fewer due to deduping, pad with simple variants
        while len(normed) < 10:
            normed.append(_fallback_sentence(lemma, word_count, idx=len(normed) + 1))

        return normed[:10]

    except Exception as e:
        # Fallback deterministic generator (no external calls)
        sys.stderr.write(f"[WARN] OpenAI call failed or unavailable: {e}\n")
        wc = word_count
        return [_fallback_sentence(lemma, wc, idx=i) for i in range(1, 11)]


def _fallback_sentence(lemma: str, word_count: int, idx: int) -> str:
    """
    Generate a simple deterministic sentence with the target lemma to serve as a fallback.
    """
    base_words = [
        "today", "people", "often", "quickly", "learn", "new", "ideas", "through", "simple", "practice",
        "we", "can", "easily", "build", "useful", "skills", "together", "by", "trying", "examples",
    ]
    rng = random.Random(idx * 7919)
    words = []
    # Guarantee the lemma appears exactly once
    insert_pos = rng.randint(0, max(0, word_count - 1))
    for i in range(word_count):
        if i == insert_pos:
            words.append(lemma)
        else:
            words.append(rng.choice(base_words))
    # Capitalize first and add period for readability
    sent = " ".join(words)
    return sent[0].upper() + sent[1:] + "."


# --------------- Step 3: Stanza Lemmatization ---------------

_STANZA_PIPELINE_CACHE: Dict[str, "stanza.Pipeline"] = {}  # type: ignore


def _ensure_stanza_pipeline(language: str = "en") -> "stanza.Pipeline":  # type: ignore
    """
    Initialize and cache a stanza pipeline for the given language.
    Downloads models if not present.
    """
    if stanza is None:
        raise RuntimeError(
            "stanza is not installed. Please run: pip install stanza"
        )
    if language in _STANZA_PIPELINE_CACHE:
        return _STANZA_PIPELINE_CACHE[language]
    try:
        # Try to build directly
        nlp = stanza.Pipeline(lang=language, processors="tokenize,mwt,pos,lemma", tokenize_pretokenized=False, verbose=False)
    except Exception:
        # Attempt download then build
        stanza.download(language, processors="tokenize,mwt,pos,lemma", verbose=False)
        nlp = stanza.Pipeline(lang=language, processors="tokenize,mwt,pos,lemma", tokenize_pretokenized=False, verbose=False)
    _STANZA_PIPELINE_CACHE[language] = nlp
    return nlp


_PUNCT_REGEX = re.compile(r"[^\w\s]")


def _remove_punctuation(text: str) -> str:
    """
    Remove punctuation from the text. Keep whitespace and word characters (letters, digits, underscore).
    """
    # Remove punctuation and normalize whitespace
    no_punct = _PUNCT_REGEX.sub(" ", text)
    return " ".join(no_punct.split())


def lemmatize_sentences_stanza(sentences: Sequence[str], language: str = "en") -> List[LemmatizedSentence]:
    """
    Remove punctuation, run stanza lemmatizer, and return tokens and lemmas for each sentence.
    """
    nlp = _ensure_stanza_pipeline(language)
    results: List[LemmatizedSentence] = []
    for s in sentences:
        cleaned = _remove_punctuation(s)
        if not cleaned.strip():
            results.append(LemmatizedSentence(original=s, cleaned="", tokens=[], lemmas=[]))
            continue
        doc = nlp(cleaned)
        toks: List[str] = []
        lems: List[str] = []
        for sent in doc.sentences:
            for w in sent.words:
                # Keep only tokens that are non-empty
                token_text = (w.text or "").strip()
                lemma_text = (w.lemma or "").strip()
                if token_text:
                    toks.append(token_text)
                    lems.append(lemma_text)
        results.append(LemmatizedSentence(original=s, cleaned=cleaned, tokens=toks, lemmas=lems))
    return results


# --------------- Step 4: Sentence selection and list update ---------------

def choose_best_sentence(
    target_lemma: str,
    lemmatized: Sequence[LemmatizedSentence],
    prev_lemmas: Sequence[str],
) -> Tuple[Optional[LemmatizedSentence], Dict[str, any]]:
    """
    From the provided lemmatized sentences:
     - Filter those whose lemmas contain the target lemma (case-insensitive)
     - Score each by the count of lemmas not present in prev_lemmas
     - Choose one with fewest new lemmas; tie-breaker: fewer tokens; then original order.

    Returns (chosen_sentence_or_None, debug_info)
    """
    prev_set = {l.lower() for l in prev_lemmas}
    target = target_lemma.lower()

    candidates: List[Tuple[LemmatizedSentence, int, int, List[str]]] = []
    for idx, ls in enumerate(lemmatized):
        lemmas_lower = [l.lower() for l in ls.lemmas if l]
        if target not in lemmas_lower:
            continue
        unknown = sorted({l for l in lemmas_lower if l not in prev_set})
        unknown_count = len(unknown)
        candidates.append((ls, unknown_count, len(ls.tokens), unknown))

    if not candidates:
        return None, {"reason": "no_sentence_contains_target_lemma"}

    # Choose by: fewest unknowns, then fewest tokens, then earliest
    candidates.sort(key=lambda t: (t[1], t[2]))
    best, unk_count, tok_count, unknown_list = candidates[0]
    debug = {
        "unknown_count": unk_count,
        "token_count": tok_count,
        "unknown_list": unknown_list,
        "candidate_count": len(candidates),
    }
    return best, debug


def apply_sentence_and_reorder(
    entries: List[ListEntry],
    current_index: int,
    chosen: LemmatizedSentence,
    unknown_lemmas: Sequence[str],
) -> Tuple[List[ListEntry], Dict[str, any]]:
    """
    Update the entries:
      - Attach chosen sentence to the current lemma at current_index.
      - If unknown_lemmas is non-empty:
           * Partition them into reorders (present later) and out_of_bound (not present in file).
           * Insert both groups (in the order they appear in 'unknown_lemmas') right before current_index.
           * Remove the original instances of the reorders from further down the list.

    Returns (new_entries, info_dict)
    """
    # Normalize sets/maps
    lemma_to_first_index: Dict[str, int] = {}
    for i, e in enumerate(entries):
        key = e.lemma.lower()
        if key not in lemma_to_first_index:  # first occurrence (case-insensitive)
            lemma_to_first_index[key] = i

    # Update current lemma with chosen sentence
    updated_entries = entries.copy()
    updated_entries[current_index] = ListEntry(lemma=entries[current_index].lemma, sentence=chosen.original)

    # If no unknowns: simple update
    if not unknown_lemmas:
        return updated_entries, {
            "out_of_bound": [],
            "reorders": [],
            "out_of_bound_count": 0,
            "reorders_count": 0,
        }

    current_lemma = entries[current_index].lemma
    all_head_lemmas_set = set(e.lemma.lower() for e in entries)

    # Partition unknowns
    reorders: List[str] = []
    out_of_bound: List[str] = []
    for l in unknown_lemmas:
        if l == current_lemma.lower():
            # It is the current lemma itself; it's already present here -> not an unknown in practice,
            # but keep logic defensive by skipping insertion.
            continue
        if l in all_head_lemmas_set:
            # Present in file; check if it's after current_index to qualify as reorder
            orig_idx = lemma_to_first_index.get(l, -1)
            if orig_idx > current_index:
                reorders.append(l)
            else:
                # If it's before, it wouldn't be part of unknown_lemmas by construction,
                # but handle gracefully by ignoring.
                pass
        else:
            out_of_bound.append(l)

    # Build items to insert (in the original unknown order)
    to_insert: List[ListEntry] = []
    for l in unknown_lemmas:
        if l in reorders:
            orig_idx = lemma_to_first_index[l]
            # Use the existing entry (lemma with its sentence if any)
            to_insert.append(ListEntry(lemma=entries[orig_idx].lemma, sentence=entries[orig_idx].sentence))
        elif l in out_of_bound:
            to_insert.append(ListEntry(lemma=l, sentence=None))
        else:
            # Either skipped because it's current or unexpected
            pass

    # Construct final list: before + inserted + after(without duplicates of reorders)
    before = updated_entries[:current_index]
    after = updated_entries[current_index:]  # includes the current lemma at position 0 of this slice

    # Remove any reorders from 'after' slice except the current lemma row
    reorder_set = set(reorders)
    filtered_after: List[ListEntry] = []
    seen_current = False
    for i, e in enumerate(after):
        # Keep the first row (the current lemma we just updated)
        if not seen_current:
            filtered_after.append(e)
            seen_current = True
            continue
        # Skip entries whose lemma is in reorder_set
        if e.lemma.lower() in reorder_set:
            continue
        filtered_after.append(e)

    new_entries = before + to_insert + filtered_after

    info = {
        "out_of_bound": out_of_bound,
        "reorders": reorders,
        "out_of_bound_count": len(out_of_bound),
        "reorders_count": len(reorders),
    }
    return new_entries, info


# --------------- Orchestration (Step loop) ---------------

def generate_language_learning_list(
    steps: int,
    filename: str,
    skip_count: int = 500,
    language: str = "en",
    model: str = "gpt-5-mini",
) -> None:
    """
    The main loop:
      - For each step:
          1) Read the current list file.
          2) Find the next unfinished lemma after skip_count.
          3) Generate 10 sentences with LLM.
          4) Lemmatize with stanza.
          5) Choose sentence with fewest unknown lemmas vs prev list.
          6) Write updated list to the next filename (increment leading number).
          7) Print details and continue to next step using the newly written file.
    """
    if steps <= 0:
        print("Nothing to do: steps must be > 0.")
        return

    current_file = filename
    for step_idx in range(1, steps + 1):
        # 1) Read current list
        entries = parse_list_file(current_file)

        # 2) Find target lemma
        idx, lemma = find_next_undone_lemma(entries, skip_count=skip_count)

        # Prepare prev lemmas set (only heads, ignore sentences)
        prev_lemmas = [e.lemma for e in entries[:idx]]

        # 3) Generate sentences
        sentences = call_openai_generate_sentences(lemma, model=model)

        # 4) Lemmatize
        lemmas_per_sentence = lemmatize_sentences_stanza(sentences, language=language)

        # 5) Choose best sentence
        chosen, dbg = choose_best_sentence(lemma, lemmas_per_sentence, prev_lemmas)

        if chosen is None:
            # No sentence included the lemma; skip creating a new file to avoid infinite loop
            print(f"[Step {step_idx}] No generated sentence contained the lemma '{lemma}'. Skipping this step.")
            break

        # Build unknowns specifically for the chosen sentence
        prev_set = {l.lower() for l in prev_lemmas}
        unknowns = [l.lower() for l in chosen.lemmas if l and l.lower() not in prev_set]

        # 6) Apply update and write new file
        new_entries, info = apply_sentence_and_reorder(entries, idx, chosen, unknowns)
        next_file = get_next_filename(current_file)
        write_list_file(new_entries, next_file)

        # 7) Print details
        if len(info.get("out_of_bound", [])) == 0 and len(info.get("reorders", [])) == 0:
            print(f"[Step {step_idx}] File: {next_file}")
            print(f"  Lemma: {lemma}")
            print(f"  Sentence: {chosen.original}")
            print(f"  Unknown lemmas introduced: 0")
        else:
            print(f"[Step {step_idx}] File: {next_file}")
            print(f"  Lemma: {lemma}")
            print(f"  Sentence: {chosen.original}")
            print(f"  Out-of-bound lemmas ({info['out_of_bound_count']}): {', '.join(info['out_of_bound']) if info['out_of_bound'] else '(none)'}")
            print(f"  Re-orders ({info['reorders_count']}): {', '.join(info['reorders']) if info['reorders'] else '(none)'}")

        # Continue with the new file next
        current_file = next_file


# --------------- CLI ---------------

def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a language learning list with LLM + Stanza.")
    p.add_argument("--steps", type=int, required=True, help="Number of steps to run.")
    p.add_argument("--file", type=str, required=True, help="Input list filename (e.g., 1.txt).")
    p.add_argument("--skip", type=int, default=500, help="Number of initial lemmas to skip (default: 500).")
    p.add_argument("--lang", type=str, default="en", help="Language code for Stanza (default: en).")
    p.add_argument("--model", type=str, default="gpt-5-mini", help="OpenAI model name (default: gpt-5-mini).")
    return p


def main() -> None:
    args = _build_arg_parser().parse_args()
    generate_language_learning_list(
        steps=args.steps,
        filename=args.file,
        skip_count=args.skip,
        language=args.lang,
        model=args.model,
    )


if __name__ == "__main__":
    main()
