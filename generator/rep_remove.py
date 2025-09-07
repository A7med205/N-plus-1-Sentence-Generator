def remove_duplicate_words(input_file, output_file):
    seen = set()
    unique_words = []
    repeated_words = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            word = line.strip()
            if word:
                if word not in seen:
                    seen.add(word)
                    unique_words.append(word)
                else:
                    repeated_words.append(word)

    # Write unique words to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in unique_words:
            outfile.write(word + '\n')

    print(f"Duplicates removed. Cleaned file saved as: {output_file}")
    if repeated_words:
        print("\nRepeated words found:")
        for word in repeated_words:
            print(word)
    else:
        print("\nNo repeated words found.")

# Example usage:
input_path = "1.txt"          # input file
output_path = "unique_words.txt"  # output file
remove_duplicate_words(input_path, output_path)

