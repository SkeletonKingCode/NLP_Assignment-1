import os

# =========================
# BPE TRAINING (UNCHANGED CORE)
# =========================

def bytePairEncoding(training_sequence, vocab=None, max_vocab_size=250):
    
    # Ensure list of symbols (Unicode safe)
    if isinstance(training_sequence, str):
        training_sequence = list(training_sequence)

    # Initialize vocab from characters
    vocab = set(training_sequence)

    merge_list = []   # stack

    while len(vocab) < max_vocab_size:
        
        # Step 1: Count adjacent pairs
        pair_counts = {}
        for i in range(len(training_sequence) - 1):
            pair = (training_sequence[i], training_sequence[i + 1])
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

        if not pair_counts:
            break

        # Step 2: Most frequent pair
        most_frequent_pair = None
        max_count = 0

        for pair, count in pair_counts.items():
            if count > max_count:
                max_count = count
                most_frequent_pair = pair

        if max_count < 2:
            break

        # Step 3: Create new token
        new_token = most_frequent_pair[0] + most_frequent_pair[1]

        # Step 4: Replace pair
        i = 0
        new_sequence = []

        while i < len(training_sequence):
            if (i < len(training_sequence) - 1 and
                training_sequence[i] == most_frequent_pair[0] and
                training_sequence[i + 1] == most_frequent_pair[1]):

                new_sequence.append(new_token)
                i += 2
            else:
                new_sequence.append(training_sequence[i])
                i += 1

        training_sequence = new_sequence

        # Step 5: Add to vocab
        vocab.add(new_token)

        # Step 6: Store merge (stack behavior)
        merge_list.append((new_token, most_frequent_pair))

    return training_sequence, vocab, merge_list


# =========================
# ENCODE (UNCHANGED)
# =========================

def encode(sequence, vocab, merge_list):

    if isinstance(sequence, str):
        sequence = list(sequence)

    for new_token, pair in reversed(merge_list):

        i = 0
        new_sequence = []

        while i < len(sequence):
            if (i < len(sequence) - 1 and
                sequence[i] == pair[0] and
                sequence[i + 1] == pair[1]):

                new_sequence.append(new_token)
                i += 2
            else:
                new_sequence.append(sequence[i])
                i += 1

        sequence = new_sequence

    return sequence


# =========================
# DECODE (STACK BOTTOM → TOP)
# =========================

def decode(encoded_sequence, vocab, merge_list):

    if isinstance(encoded_sequence, str):
        encoded_sequence = list(encoded_sequence)

    sequence = encoded_sequence[:]

    for new_token, pair in merge_list:

        new_sequence = []

        for symbol in sequence:
            if symbol == new_token:
                new_sequence.append(pair[0])
                new_sequence.append(pair[1])
            else:
                new_sequence.append(symbol)

        sequence = new_sequence

    return sequence


# =========================
# READ ALL DATASET FILES
# =========================

def load_full_corpus(folder_path):

    full_text = ""

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                full_text += f.read() + " "

    return full_text


# =========================
# TRAIN ON FULL DATASET
# =========================

def train_bpe_on_dataset(folder_path, vocab_size=250):

    corpus = load_full_corpus(folder_path)

    # Train BPE
    encoded_corpus, final_vocab, merge_list = bytePairEncoding(
        corpus,
        max_vocab_size=vocab_size
    )

    return final_vocab, merge_list, encoded_corpus

# =========================
# Saving the Tokenizer
# =========================

import json

def save_tokenizer_json(vocab, merge_list, filepath="BSETokenizer/bpe_tokenizer.json"):
    # Convert set to list for JSON
    data = {
        "vocab": list(vocab),
        "merge_list": [(token, list(pair)) for token, pair in merge_list]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_tokenizer_json(filepath="BSETokenizer/bpe_tokenizer.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    vocab = set(data["vocab"])
    # Convert pair back to tuple
    merge_list = [(item[0], tuple(item[1])) for item in data["merge_list"]]
    return vocab, merge_list

# =========================
# LOAD TOKENIZED CORPUS FOR TRIGRAM MODEL
# =========================

def load_tokenized_corpus_for_trigram(filepath="Tokenized_Dataset/Tokenized_Data.txt"):
    """
    Reads a tokenized corpus file (one token per line) and returns a list of segments.
    Segments are delimited by <EOS>, <EOP>, <EOD> tokens.
    Each segment is a list of tokens, including the boundary token as its last element.

    Parameters:
        filepath (str): Path to the tokenized corpus file.

    Returns:
        list of list of str: Segments ready for trigram model training.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read all non-empty lines (tokens)
        tokens = [line.strip() for line in f if line.strip()]

    return tokens

# =========================
# EXAMPLE USAGE
# =========================

if __name__ == "__main__":

    dataset_folder = "urdu_stories_dataset"

    # Train on all files
    final_vocab, merge_list, encoded_corpus = train_bpe_on_dataset(dataset_folder, 250)

    print("Final Vocabulary Size:", len(final_vocab))
    print("Total Merges Learned:", len(merge_list))

    # Save tokenizer for later use (optional)
    save_tokenizer_json(final_vocab, merge_list)

    # ===== NEW: Save the tokenized corpus =====
    output_dir = "Tokenized_Dataset"
    os.makedirs(output_dir, exist_ok=True)                 # create folder if missing
    output_file = os.path.join(output_dir, "Tokenized_Data.txt.txt")

    # Write each token on a new line (preserves token boundaries)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(encoded_corpus))

    print(f"Tokenized corpus saved to {output_file}")

    # Example encoding/decoding of a sample sentence
    sample_sentence = "فقیر نے کہا بھائی <EOS>"
    encoded_sample = encode(sample_sentence, final_vocab, merge_list)
    print("\nEncoded Sample:")
    print(encoded_sample)

    decoded_sample = decode(encoded_sample, final_vocab, merge_list)
    print("\nDecoded Sample:")
    print("".join(decoded_sample))

# USAGE IN OTHER FILES

# new_script.py
# from TokenizerCode import encode, decode, load_tokenizer_json

# vocab, merges = load_tokenizer_json("urdu_bpe.json")

# text = "فقیر نے کہا بھائی <EOS>"
# encoded = encode(text, vocab, merges)
# print("Encoded:", encoded)

# decoded = decode(encoded, vocab, merges)
# print("Decoded:", "".join(decoded))
