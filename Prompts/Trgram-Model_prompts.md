# Phase III — Trigram Language Model Prompts

This file contains all LLM prompts used during the development of the Trigram Language Model for the Urdu Story Generation System.

---

## Prompt 1 — Core Trigram Model Implementation

**Purpose:** Build unigram, bigram, and trigram counts with MLE and linear interpolation from the BPE-encoded corpus.

```
I am implementing Phase III of my NLP assignment: Trigram Language Model.

Context:
- I already trained a custom BPE tokenizer in Phase II.
- I have:
    - merge_list
    - final_vocab
    - encoded training corpus (list of tokens)
- The corpus already contains special tokens:
    <EOS> (sentence end)
    <EOP> (paragraph end)
    <EOT> (story end)

Now I need to implement a 3-gram Language Model using Maximum Likelihood Estimation (MLE).

Strict Requirements:

1. Build:
   - Unigram counts
   - Bigram counts
   - Trigram counts

2. Implement Interpolation:
   P(w3 | w1, w2) = λ1 * P_trigram(w3 | w1, w2)
                  + λ2 * P_bigram(w3 | w2)
                  + λ3 * P_unigram(w3)
   where λ1 + λ2 + λ3 = 1

3. Use MLE for probability estimation.

4. Implement text generation:
   - Input: prefix tokens (already BPE encoded)
   - Generate next token iteratively
   - Stop when <EOT> is generated
   - Or stop at max_length

5. Add Temperature parameter:
   - Control randomness in sampling
   - If temperature < 1 → more deterministic
   - If temperature > 1 → more random

6. Optional but recommended:
   - Implement top-k sampling (k parameter)
   - Prevent repetitive loops (penalize recently used tokens)

7. Use only standard Python libraries:
   - collections
   - math
   - random

8. Code must be:
   - Minimal
   - Clean
   - Easy to explain in viva
   - Not overly object-oriented
   - No external ML libraries

9. Output:
   - Complete Python implementation
   - Example usage:
       - Train model from encoded corpus
       - Generate story from Urdu prefix
   - Short comments only

Important:
Do NOT use any NLP libraries.
Do NOT use neural networks.
Do NOT use smoothing methods other than interpolation.
Keep implementation straightforward and classical (as taught in class).
```

---

## Prompt 2 — Text Generation with Sampling Controls

**Purpose:** Implement the generation loop with temperature scaling, top-k filtering, and repetition penalty.

```
I have trained a trigram language model with unigram, bigram, and trigram counts.

Now write a generate_text() function with this signature:

generate_text(prefix_tokens, unigram_counts, bigram_counts, trigram_counts,
              total_tokens, vocab, max_length=500, temperature=0.8,
              top_k=10, stop_token="<EOT>")

Generation logic must strictly follow:

1. Start with prefix_tokens as the initial generated sequence.
2. At each step, take the last 2 tokens as context (w1, w2).
3. Compute interpolated probability for every token in vocab.
4. Apply temperature scaling:
   - scaled_prob = prob ^ (1 / temperature)
   - Renormalize after scaling.
5. Apply top-k filtering:
   - Keep only top k tokens by probability.
   - Renormalize after filtering.
6. Apply repetition penalty:
   - Multiply probability by 0.7 for any token seen in the last 10 tokens.
   - Renormalize after penalty.
7. Sample next token using random.choices with weights.
8. Append to generated sequence.
9. Stop if next token == stop_token or length >= max_length.

Constraints:
- Use only: random, collections
- No external libraries
- Keep code minimal and readable
- Must handle edge cases: empty prob list, prefix shorter than 2 tokens

Return only clean Python code.
```

---

## Prompt 3 — Interpolation Function

**Purpose:** Implement the linear interpolation probability function used at each generation step.

```
Write a standalone interpolated_prob() function for a trigram language model.

Function signature:
interpolated_prob(w1, w2, w3, unigram_counts, bigram_counts,
                  trigram_counts, total_tokens, l1=0.6, l2=0.3, l3=0.1)

Logic:

- P_trigram = trigram_counts[(w1,w2,w3)] / bigram_counts[(w1,w2)]
              (0 if bigram_counts[(w1,w2)] == 0)

- P_bigram  = bigram_counts[(w2,w3)] / unigram_counts[w2]
              (0 if unigram_counts[w2] == 0)

- P_unigram = unigram_counts[w3] / total_tokens

- Return: l1 * P_trigram + l2 * P_bigram + l3 * P_unigram

Constraints:
- No division by zero
- No external libraries
- Keep it a pure function (no side effects)
- Add one short comment per calculation

Return only the function code.
```

---

## Prompt 4 — Post-processing Generated Tokens

**Purpose:** Convert the raw generated BPE token list back into readable Urdu text.

```
After generating a list of BPE tokens using my trigram language model,
I need to convert them back into readable Urdu text.

Write a postprocess_story() function:

postprocess_story(tokens, special_tokens)

Where special_tokens = ["<EOS>", "<EOP>", "<EOT>"]

Logic:
- Join all tokens into one string.
- Replace <EOS> with Urdu full stop: ۔
- Replace <EOP> with newline: \n
- Remove <EOT> completely.
- Strip extra whitespace.

Constraints:
- No regex
- No external libraries
- Keep it minimal — under 10 lines

Return only the function code.
```

---

## Prompt 5 — Debugging Nonsense Output

**Purpose:** Understand and fix poor generation quality caused by small BPE vocabulary on Urdu subword tokens.

```
I implemented a Trigram Language Model on top of a BPE tokenizer (vocab size 250)
trained on 600 Urdu stories.

The generated output looks like this:
"فقیر نے کہاں سے بانٹے کو دیکھا تھا <EOS> وہ گھرمت کرنے لگے"

Words like "گھرمت" and "دوسرختلی" appear — these are not real Urdu words.

Please explain:
1. Why does this happen with BPE + trigram LM?
2. How does small vocab size (250) cause broken word combinations?
3. What specific changes would improve output quality?
4. Should I use word-level tokenization instead of BPE for a trigram LM?
5. What is a realistic expectation for output quality from a classical trigram LM?

Do NOT rewrite my code.
Just explain the root cause and give practical recommendations
I can implement quickly and explain in viva.
```

---

## Prompt 6 — Full Pipeline Integration Test

**Purpose:** Verify the complete Phase II → Phase III pipeline works end to end before submission.

```
I have completed Phase II (BPE Tokenizer) and Phase III (Trigram LM).

Write a minimal integration test that:

1. Loads the trained BPE tokenizer from bpe_tokenizer.json.
2. Loads the tokenized corpus from Tokenized_Data.txt.
3. Trains the trigram model on the corpus.
4. Takes this Urdu prefix: "فقیر نے کہا"
5. BPE-encodes the prefix.
6. Generates a story with max_length=200, temperature=0.8, top_k=7.
7. BPE-decodes the generated tokens.
8. Post-processes and prints the final Urdu story.
9. Prints: vocab size, total merges, tokens generated.

Constraints:
- Use only my existing functions — do not rewrite any logic.
- Keep the test script under 30 lines.
- Add minimal comments.

Return only the test script.
```

---

## Prompt 7 — Improving Generation Quality (Added)

**Purpose:** Systematically improve output coherence by tuning sampling parameters.

```
My trigram LM generates Urdu text but output quality is poor due to subword BPE tokens.

Without changing the core algorithm, suggest and implement:

1. An optimal lambda combination (λ1, λ2, λ3) for Urdu subword trigrams.
2. The best temperature value for more coherent Urdu output.
3. The best top_k value to balance diversity and coherence.
4. A repetition penalty strategy that avoids repeating the same subword.
5. A minimum probability threshold to filter near-zero probability tokens.

For each suggestion:
- Give the recommended value.
- Give a one-line reason why.

Then update only the generate_text() function with these improvements.
Do not change training logic.
```

---

## Prompt 8 — Edge Case Handling (Added)

**Purpose:** Make the generation robust against empty probabilities, short prefixes, and infinite loops.

```
My trigram generate_text() function sometimes crashes or loops infinitely.

Add defensive handling for these edge cases:

1. If prob list is empty at any step → fall back to uniform sampling from vocab.
2. If prefix has fewer than 2 tokens → duplicate the last token to reach length 2.
3. If the same token is generated 5 times in a row → force sample a different token.
4. If max_length is reached without <EOT> → append <EOT> manually and stop.
5. If all probabilities are 0 after filtering → reset to unfiltered distribution.

Constraints:
- Do not change the core sampling logic.
- Add edge case checks as small if-blocks inside the existing loop.
- Keep changes minimal and easy to explain.

Return only the updated generate_text() function.
```

---

## Summary

| Prompt | Purpose |
|--------|---------|
| Prompt 1 | Core trigram model — counts + interpolation + generation |
| Prompt 2 | Generation loop — temperature, top-k, repetition penalty |
| Prompt 3 | Interpolation probability function |
| Prompt 4 | Post-processing tokens to readable Urdu text |
| Prompt 5 | Debugging nonsense output from BPE + trigram combination |
| Prompt 6 | Full pipeline integration test Phase II → Phase III |
| Prompt 7 | Improving generation quality through parameter tuning |
| Prompt 8 | Edge case handling for robust generation |
