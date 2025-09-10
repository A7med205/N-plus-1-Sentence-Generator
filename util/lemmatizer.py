#Example: python lemmatizer.py --lang en --input eng_sentences_only.txt --output eng_sentences_with_lemmas.txt --continue_mode

import stanza
import argparse
import os
import string

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

    # Process input
    count = 0
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "a", encoding="utf-8") as outfile:
        for idx, line in enumerate(infile):
            if idx < start_line:
                continue  # Skip processed lines

            sentence = line.strip()
            if not sentence:
                outfile.write("\n")
                continue

            # Remove punctuation
            sentence_clean = sentence.translate(str.maketrans("", "", string.punctuation))

            # Run Stanza
            doc = nlp(sentence_clean)

            # Extract lemmas
            lemmas = []
            for sent in doc.sentences:
                for word in sent.words:
                    lemmas.append(word.lemma)

            # Write original + lemmas
            outfile.write(f"{sentence}\t{' '.join(lemmas)}\n")

            count += 1
            if count % 100 == 0:
                print(f"Processed {count + start_line} lines...")

    print(f"Done! Total lines processed: {count + start_line}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stanza Lemmatization Pipeline")
    parser.add_argument("--lang", required=True, help="Language code (e.g., en, fr, de)")
    parser.add_argument("--input", required=True, help="Input file with sentences")
    parser.add_argument("--output", required=True, help="Output file with lemmas")
    parser.add_argument("--continue_mode", action="store_true", help="Continue processing if output exists")
    args = parser.parse_args()

    process_file(args.input, args.output, args.lang, args.continue_mode)

