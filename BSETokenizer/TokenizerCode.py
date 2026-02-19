import os
import json

# =========================
# SPECIAL TOKENS (added to initial vocabulary)
# =========================
SPECIAL_TOKENS = ["<EOS>", "<EOP>", "<EOD>"]

# =========================
# TOKENIZATION HELPERS
# =========================
def tokenize_text(text, special_tokens=SPECIAL_TOKENS):
    """
    Convert a raw string into a list of symbols.
    Special tokens (e.g., '<EOS>') are kept as single units;
    all other characters become individual symbols.
    """
    tokens = []
    i = 0
    while i < len(text):
        matched = False
        for special in special_tokens:
            if text.startswith(special, i):
                tokens.append(special)
                i += len(special)
                matched = True
                break
        if not matched:
            tokens.append(text[i])
            i += 1
    return tokens

# =========================
# BPE TRAINING 
# =========================
def bytePairEncoding(training_sequence, initial_extra_tokens=None, max_vocab_size=250):
    """
    training_sequence : list of symbols (strings, may be multi‑character)
    initial_extra_tokens : additional tokens to include in the initial vocabulary
                           (e.g., special tokens not necessarily present in the sequence)
    """
    # Initial vocabulary: all symbols in the sequence plus extra tokens
    vocab = set(training_sequence)
    if initial_extra_tokens:
        vocab.update(initial_extra_tokens)

    merge_list = []   # stack of merges (new_token, (left, right))
    step = max_vocab_size/10
    while len(vocab) < max_vocab_size:
        # Progress
        if len(vocab)%step == 0:
            print("Progress: ",len(vocab)/max_vocab_size*100,"%" )
        # Count adjacent pairs
        pair_counts = {}
        for i in range(len(training_sequence) - 1):
            pair = (training_sequence[i], training_sequence[i + 1])
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

        if not pair_counts:
            break

        # Most frequent pair
        most_frequent_pair = None
        max_count = 0
        for pair, count in pair_counts.items():
            if count > max_count:
                max_count = count
                most_frequent_pair = pair

        if max_count < 2:
            break

        # Create new token
        new_token = most_frequent_pair[0] + most_frequent_pair[1]

        # Replace all occurrences of the pair
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

        # Add new token to vocabulary and record merge
        vocab.add(new_token)
        merge_list.append((new_token, most_frequent_pair))

    return training_sequence, vocab, merge_list

# =========================
# ENCODE 
# =========================
def encode(sequence, vocab, merge_list, special_tokens=SPECIAL_TOKENS):
    """
    Encode a string or a list of symbols by applying merges from top to bottom.
    If a string is given, it is first tokenized using the special tokens.
    """
    if isinstance(sequence, str):
        sequence = tokenize_text(sequence, special_tokens)

    # Apply merges in reverse order (most recent first)
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
# DECODE 
# =========================
def decode(encoded_sequence, vocab, merge_list):
    """
    Decode a list of symbols by expanding merges in the order they were learned.
    """
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
# DATASET LOADING
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

    # Tokenize the corpus into symbols (characters and special tokens)
    tokenized_corpus = tokenize_text(corpus, SPECIAL_TOKENS)

    # Train BPE, passing the special tokens as initial extra tokens
    encoded_corpus, final_vocab, merge_list = bytePairEncoding(
        tokenized_corpus,
        initial_extra_tokens=SPECIAL_TOKENS,
        max_vocab_size=vocab_size
    )

    return final_vocab, merge_list, encoded_corpus

# =========================
# SAVE / LOAD TOKENIZER 
# =========================
def save_tokenizer_json(vocab, merge_list, special_tokens, filepath="BSETokenizer/bpe_tokenizer.json"):
    data = {
        "vocab": list(vocab),
        "merge_list": [(token, list(pair)) for token, pair in merge_list],
        "special_tokens": special_tokens
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_tokenizer_json(filepath="BSETokenizer/bpe_tokenizer.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    vocab = set(data["vocab"])
    merge_list = [(item[0], tuple(item[1])) for item in data["merge_list"]]
    special_tokens = data.get("special_tokens", [])
    return vocab, merge_list, special_tokens

# =========================
# LOAD TOKENIZED CORPUS FOR TRIGRAM MODEL 
# =========================
def load_tokenized_corpus_for_trigram(filepath="Tokenized_Dataset/Tokenized_Data.txt"):
    with open(filepath, 'r', encoding='utf-8') as f:
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

    # Save tokenizer (including special tokens)
    os.makedirs("BSETokenizer", exist_ok=True)
    save_tokenizer_json(final_vocab, merge_list, SPECIAL_TOKENS)

    # Save tokenized corpus (one token per line)
    output_dir = "Tokenized_Dataset"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Tokenized_Data.txt")   # fixed double extension

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(encoded_corpus))

    print(f"Tokenized corpus saved to {output_file}")

    # Example encoding/decoding
    sample_sentence = "فقیر نے کہا بھائی <EOS>"
    encoded_sample = encode(sample_sentence, final_vocab, merge_list, SPECIAL_TOKENS)
    print("\nEncoded Sample:")
    print(encoded_sample)

    decoded_sample = decode(encoded_sample, final_vocab, merge_list)
    print("\nDecoded Sample:")
    print("".join(decoded_sample))

# =========================
# USAGE IN OTHER SCRIPTS
# =========================
# from TokenizerCode import encode, decode, load_tokenizer_json
# vocab, merges, specials = load_tokenizer_json("BSETokenizer/bpe_tokenizer.json")
# text = "فقیر نے کہا بھائی <EOS>"
# encoded = encode(text, vocab, merges, specials)
# decoded = decode(encoded, vocab, merges)
# print("".join(decoded))