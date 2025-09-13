
#Example: python lemmatizer.py --lang de --input deu_sentences_only.txt --output deu_sentences_with_lemmas.txt --continue_mode
#Example: python lemmatizer.py --lang es --input /home/salmon/anki/N-plus-1-Sentence-Generator/corpora/es/sentences_only.txt --output /home/salmon/anki/N-plus-1-Sentence-Generator/corpora/es/sentences_with_lemmas.txt --continue_mode

import stanza
import argparse
import os
import string
from tqdm import tqdm


def process_file(input_file, output_file, lang, continue_mode):
    # Initialize Stanza pipeline
    print(f"Loading Stanza pipeline for language: {lang}...")
    stanza.download(lang, processors='tokenize,pos,lemma', verbose=False)
    nlp = stanza.Pipeline(lang=lang, processors='tokenize,pos,lemma', use_gpu=False)

    # If continuation mode, count existing lines in output file
    start_line = 0
    if continue_mode and os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as out:
            start_line = sum(1 for _ in out)
        print(f"Continuation enabled. Skipping first {start_line} lines.")
    else:
        # Create new file or overwrite existing
        open(output_file, "w", encoding="utf-8").close()

    with open(input_file, "r", encoding="utf-8") as f:
        total_inlines = sum(1 for _ in f)

    with open(output_file, "r", encoding="utf-8") as f:
        total_outlines = sum(1 for _ in f)

    total_lines= total_inlines-total_outlines

    # Process input
    count = 0
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "a", encoding="utf-8") as outfile:
        for idx, line in tqdm(enumerate(infile), total=total_lines, desc="Processing"):
            if idx < start_line:
                continue  # Skip processed lines

            sentence = line.strip()
            if not sentence:
                outfile.write("\n")
                continue

            # Run Stanza
            doc = nlp(sentence)

            # Extract lemmas
            lemmas = []
            for sent in doc.sentences:
                for word in sent.words:
                    lemmas.append(word.lemma)

            # Write original + lemmas
            outfile.write(f"{sentence}\t{' '.join(lemmas)}\n")

            count += 1

    print(f"Done! Total lines processed: {count + start_line}")

    
languages = ["de","es","pt","ru","ja","ko","zh-hans","fr","it"]

for i in languages:
    temp = f"{i}_sentences_with_lemmas.txt"
    infile = os.path.join("/home/salmon/anki/lemmatize/git goon/N-plus-1-Sentence-Generator/corpora/", i, "sentences_only.txt")
    outfile = os.path.join("/home/salmon/anki/lemmatize/git goon/N-plus-1-Sentence-Generator/corpora/", i, temp)
    print(infile)
    print(outfile)
    process_file(infile, outfile, i, True)
    print()