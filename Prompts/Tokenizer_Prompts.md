# Phase II — BPE Tokenizer Prompts

This file contains all LLM prompts used during the development of the custom Byte Pair Encoding (BPE) tokenizer for the Urdu Story Generation System.

---

## Prompt 1 — BPE Training (Classroom Version)

**Purpose:** Implement the core `bytePairEncoding()` function exactly as taught in class.

```
You are helping me implement Byte Pair Encoding exactly as taught in my NLP class.

Write clean and minimal Python code for a function:

bytePairEncoding(training_sequence, vocab, max_vocab_size=250)

Algorithm requirements (must strictly follow this logic):

1. Initialize an empty merge_list.
2. Find the most frequent adjacent pair in training_sequence.
3. Create a new token for that most frequent pair.
4. Replace all occurrences of that pair in training_sequence with the new token.
5. Add the new token to vocab.
6. Store mapping (new_token, most_frequent_pair) inside merge_list.
7. Repeat until vocab size reaches max_vocab_size.

Important constraints:
- Do NOT use any tokenizer libraries.
- Do NOT use regex libraries.
- Keep implementation simple and readable.
- training_sequence should be treated as list of symbols.
- merge_list should behave like a stack.
- Code must be modular with small helper functions.
- Optimized to handle Urdu Unicode characters properly.

Return only clean Python code.
```

---

## Prompt 2 — Encoding Function

**Purpose:** Implement `encode()` that applies merges from top to bottom of the merge stack.

```
Using the previously implemented bytePairEncoding function, write an encode() function.

Function signature:
encode(sequence, vocab, merge_list)

Encoding logic must strictly follow:

- merge_list behaves like a stack.
- Encoding is done from top to bottom of merge_list (left to right in merge order).
- For each (new_token, pair) in merge_list:
    replace occurrences of pair in the sequence with new_token.
- sequence should be treated as a list of symbols.

Constraints:
- No external libraries.
- No regex.
- Must handle special tokens <EOS>, <EOP>, <EOT> correctly.
- Keep code simple and readable.
- Do not rewrite the training algorithm.
- Assume merge_list already exists.

Return minimal Python code.
```

---

## Prompt 3 — Decoding Function

**Purpose:** Implement `decode()` that reverses the merge stack to reconstruct original text.

```
Write a decode() function for the BPE implementation.

Function signature:
decode(encoded_sequence, vocab, merge_list)

Decoding logic must strictly follow:

- merge_list behaves like a stack.
- Decoding is done from bottom to top of merge_list (reverse order).
- For each (new_token, pair) in reversed merge_list:
    replace new_token with its original pair.
- encoded_sequence should be treated as a list of symbols.

Constraints:
- No external libraries.
- No regex.
- Keep implementation minimal.
- Must correctly reconstruct original Urdu text including special tokens.

Return clean and readable Python code only.
```

---

## Prompt 4 — Full Dataset Integration and Final Refined Training Prompt

**Purpose:** Extend the classroom BPE implementation to train on the full 600-story corpus.

```
I am implementing Phase II (BPE Tokenizer) for my NLP assignment.

IMPORTANT:
This is the exact BPE code that was taught by my instructor in class.
You MUST NOT change the core BPE logic.
You are only allowed to extend and optimize it to work on my full dataset.

Here is my current BPE implementation:

def bytePairEncoding(training_sequence, vocab, max_vocab_size=250):

    if isinstance(training_sequence, str):
        training_sequence = list(training_sequence)

    vocab = set(training_sequence)
    vocab.add("<EOS>")
    vocab.add("<EOP>")
    vocab.add("<EOT>")

    merge_list = []

    while len(vocab) < max_vocab_size:

        pair_counts = {}
        for i in range(len(training_sequence) - 1):
            pair = (training_sequence[i], training_sequence[i + 1])
            if pair in pair_counts:
                pair_counts[pair] += 1
            else:
                pair_counts[pair] = 1

        if not pair_counts:
            break

        most_frequent_pair = None
        max_count = 0
        for pair, count in pair_counts.items():
            if count > max_count:
                max_count = count
                most_frequent_pair = pair

        if max_count < 2:
            break

        new_token = most_frequent_pair[0] + most_frequent_pair[1]

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
        vocab.add(new_token)
        merge_list.append((new_token, most_frequent_pair))

    return training_sequence, vocab, merge_list


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


Context:

- I have a folder named "dataset" containing 600 .txt files.
- Each file contains ONE fully preprocessed Urdu story.
- Special tokens are already inserted inside the stories:
    <EOS>  → sentence end
    <EOP>  → paragraph end
    <EOT>  → story end

Task:

Modify my code so that:

1. It reads ALL 600 .txt files from the dataset folder.
2. Concatenates them into ONE large training corpus.
3. Keeps all special tokens as normal symbols.
4. Trains BPE on the full corpus.
5. Vocabulary size must be 250.
6. Returns:
   - final_vocab
   - merge_list
   - encoded full corpus
7. Keep encode() and decode() working correctly.
8. Keep stack behavior of merge_list exactly as implemented.
9. Handle Urdu Unicode characters properly.
10. Keep the code minimal and clean because I must explain it in viva.
11. Do NOT use any external libraries except:
      os
      collections (if needed)
12. Do NOT use HuggingFace or any tokenizer library.

Output format:
- Full final Python code.
- Show example usage:
   - Train on dataset folder
   - Encode a sample Urdu sentence
   - Decode it back
- Keep comments short.
- Do not over-engineer or create complex classes.
- Keep logic similar to original structure.

Important:
Do not rewrite the algorithm differently.
Just extend it properly for multiple files and full corpus training.
```

---

## Prompt 5 — Code Review and Logic Verification

**Purpose:** Use the LLM as a professor to verify correctness of the implementation before submission.

```
I have implemented Byte Pair Encoding (BPE) from scratch for my NLP assignment.

Please review my implementation carefully and check for:

1. Correct character-level vocabulary initialization.
2. Correct most frequent adjacent pair counting.
3. Proper replacement of pairs in the training sequence.
4. Correct stopping condition when vocab size reaches 250.
5. Proper storage of (new_token, pair) in merge_list.
6. Whether merge_list correctly behaves like a stack.
7. Whether encode() applies merges from top to bottom.
8. Whether decode() applies merges from bottom to top.
9. Whether special tokens <EOS>, <EOP>, <EOT> are preserved correctly.
10. Whether encode(decode(text)) returns the original text.

Do NOT rewrite the entire code.
Only point out logical mistakes, edge cases, or potential viva issues.

Explain clearly if something is wrong and why.
```

---

## Prompt 6 — Practical Validation Test

**Purpose:** Run a small end-to-end test to validate encode/decode correctness on real Urdu text.

```
Using my BPE implementation, create a small Urdu sample text and:

1. Train BPE with max_vocab_size=50 (small for testing).
2. Encode the sample text.
3. Decode it back.
4. Show whether original text and decoded text match exactly.
5. Print final vocab size and merge_list length.

Do not modify my implementation logic.
Just test it.
```

---

## Prompt 7 — Theoretical Correctness Check

**Purpose:** Verify that the implementation aligns with the classical BPE algorithm from NLP literature.

```
Is my BPE implementation consistent with the classical Byte Pair Encoding algorithm used in NLP?

If not, explain the theoretical difference.
```

---

## Summary

| Prompt | Purpose |
|--------|---------|
| Prompt 1 | Core BPE training function — classroom version |
| Prompt 2 | Encoding function — top to bottom merge order |
| Prompt 3 | Decoding function — reverse merge order |
| Prompt 4 | Full dataset integration — 600 story corpus — Final refined training prompt |
| Prompt 5 | Code review and logic verification |
| Prompt 6 | Practical encode/decode validation test |
| Prompt 7 | Theoretical correctness check |
