# =========================
# IMPORTS
# =========================
from collections import defaultdict, Counter
import random

import sys
import os

# Add the parent directory (Assignment-1) to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import BPE functions from tokenizer.py
from BSETokenizer.TokenizerCode import load_tokenized_corpus_for_trigram, load_tokenizer_json, encode, decode

# =========================
# TRIGRAM LM TRAINING
# =========================

def train_trigram_lm(encoded_corpus):
    unigram_counts = Counter(encoded_corpus)
    bigram_counts = defaultdict(int)
    trigram_counts = defaultdict(int)

    for i in range(len(encoded_corpus) - 1):
        bigram = (encoded_corpus[i], encoded_corpus[i + 1])
        bigram_counts[bigram] += 1

    for i in range(len(encoded_corpus) - 2):
        trigram = (encoded_corpus[i],
                   encoded_corpus[i + 1],
                   encoded_corpus[i + 2])
        trigram_counts[trigram] += 1

    total_tokens = len(encoded_corpus)
    return unigram_counts, bigram_counts, trigram_counts, total_tokens

# =========================
# INTERPOLATED PROBABILITY
# =========================

def interpolated_prob(w1, w2, w3,
                      unigram_counts,
                      bigram_counts,
                      trigram_counts,
                      total_tokens,
                      l1=0.6, l2=0.3, l3=0.1):

    trigram = (w1, w2, w3)
    bigram = (w2, w3)

    p_tri = trigram_counts[trigram] / bigram_counts[(w1, w2)] if bigram_counts[(w1, w2)] > 0 else 0
    p_bi = bigram_counts[bigram] / unigram_counts[w2] if unigram_counts[w2] > 0 else 0
    p_uni = unigram_counts[w3] / total_tokens

    return l1 * p_tri + l2 * p_bi + l3 * p_uni

# =========================
# TEXT GENERATION
# =========================

def generate_text(prefix_tokens,
                  unigram_counts,
                  bigram_counts,
                  trigram_counts,
                  total_tokens,
                  vocab,
                  max_length=1000,
                  temperature=1.0,
                  top_k=None):

    generated = prefix_tokens[:]
    recent_window = 10

    while len(generated) < max_length:
        if len(generated) < 2:
            break

        w1, w2 = generated[-2], generated[-1]

        tokens = []
        probs = []

        for w3 in vocab:
            p = interpolated_prob(w1, w2, w3,
                                  unigram_counts,
                                  bigram_counts,
                                  trigram_counts,
                                  total_tokens)
            if p > 0:
                tokens.append(w3)
                probs.append(p)

        if not probs:
            break

        # Temperature scaling
        probs = [p ** (1.0 / temperature) for p in probs]
        total_p = sum(probs)
        probs = [p / total_p for p in probs]

        # Top-k sampling
        if top_k is not None and top_k < len(tokens):
            sorted_pairs = sorted(zip(tokens, probs), key=lambda x: x[1], reverse=True)[:top_k]
            tokens, probs = zip(*sorted_pairs)
            probs = list(probs)
            total_p = sum(probs)
            probs = [p / total_p for p in probs]

        # Repetition penalty
        for i in range(len(tokens)):
            if tokens[i] in generated[-recent_window:]:
                probs[i] *= 0.7

        total_p = sum(probs)
        probs = [p / total_p for p in probs]

        next_token = random.choices(tokens, weights=probs, k=1)[0]
        generated.append(next_token)

        if next_token == "<EOD>":
            break

    return generated

def postprocess_story(tokens):
    """
    tokens: list of strings (decoded tokens)
    Returns a list with special tokens replaced/removed.
    """
    processed = []
    for token in tokens:
        if token == "<EOS>":
            processed.append("۔")          # Urdu full stop
        elif token == "<EOP>":
            processed.append("\n")         # newline for paragraph break
        elif token == "<EOD>":
            continue                        # remove end-of-story token
        else:
            processed.append(token)
    return processed

# =========================
# MAIN PIPELINE
# =========================

if __name__ == "__main__":
    dataset_folder = "urdu_stories_dataset"

    # 1 Train BPE on full dataset
    final_vocab, merge_list, special_tokens = load_tokenizer_json("BSETokenizer/bpe_tokenizer.json")
    encoded_corpus = load_tokenized_corpus_for_trigram()
    print("BPE vocab size:", len(final_vocab))
    print("Total merges:", len(merge_list))

    # 2 Train trigram LM
    unigram_counts, bigram_counts, trigram_counts, total_tokens = train_trigram_lm(encoded_corpus)

    # 3 Sample Urdu prefix
    sample_prefix = "فقیر نے کہا"
    encoded_prefix = encode(sample_prefix, final_vocab, merge_list)

    # Ensure at least 2 tokens
    if len(encoded_prefix) < 2:
        encoded_prefix = encoded_prefix + encoded_prefix

    # 4️ Generate story
    generated_tokens = generate_text(
        encoded_prefix,
        unigram_counts,
        bigram_counts,
        trigram_counts,
        total_tokens,
        final_vocab,
        max_length=5000,
        temperature=0.8,
        top_k=7
    )

    # 5 Decode back to Urdu
    decoded_story = decode(generated_tokens, final_vocab, merge_list)
    display_story = postprocess_story(decoded_story)
    print("\nGenerated Story:\n")
    print("".join(display_story))
