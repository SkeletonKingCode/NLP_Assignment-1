"""
Phase 4 — FastAPI Inference Service for Urdu Story Generation.

Loads the BPE tokenizer and trigram language model at startup,
then exposes /generate and /health endpoints.
"""

import sys
import os
from contextlib import asynccontextmanager

# ---------------------------------------------------------------------------
# Ensure the repository root is on sys.path so that
# "from BSETokenizer.TokenizerCode import ..." and
# "from Trigram_Language_Model.trigram_model import ..." resolve correctly
# when running via `uvicorn api.main:app` from the repo root.
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from BSETokenizer.TokenizerCode import (
    load_tokenizer_json,
    load_tokenized_corpus_for_trigram,
    encode,
    decode,
)
from Trigram_Language_Model.trigram_model import (
    train_trigram_lm,
    generate_text,
    postprocess_story,
)

# ============================================================================
# Request / Response schemas
# ============================================================================

class GenerateRequest(BaseModel):
    prefix: str = Field(..., min_length=1, description="Urdu text prefix (non-empty)")
    max_length: int = Field(500, ge=50, le=2000, description="Maximum tokens to generate")
    temperature: float = Field(0.8, ge=0.1, le=2.0, description="Sampling temperature")
    top_k: int = Field(7, ge=1, le=50, description="Top-K sampling parameter")


class GenerateResponse(BaseModel):
    story: str
    tokens_generated: int


class HealthResponse(BaseModel):
    status: str
    model: str
    vocab_size: int


# ============================================================================
# Application lifespan — load models once at startup
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load tokenizer + trigram model once; store in app.state."""
    # 1. Load tokenizer
    vocab, merge_list, special_tokens = load_tokenizer_json(
        os.path.join(REPO_ROOT, "BSETokenizer", "bpe_tokenizer.json")
    )
    # 2. Load tokenized corpus
    encoded_corpus = load_tokenized_corpus_for_trigram(
        os.path.join(REPO_ROOT, "Tokenized_Dataset", "Tokenized_Data.txt")
    )
    # 3. Train trigram model
    unigram_counts, bigram_counts, trigram_counts, total_tokens = train_trigram_lm(
        encoded_corpus
    )

    # Store everything in app.state
    app.state.vocab = vocab
    app.state.merge_list = merge_list
    app.state.special_tokens = special_tokens
    app.state.unigram_counts = unigram_counts
    app.state.bigram_counts = bigram_counts
    app.state.trigram_counts = trigram_counts
    app.state.total_tokens = total_tokens

    yield  # ← application is running


# ============================================================================
# FastAPI app
# ============================================================================

app = FastAPI(
    title="Urdu Story Generator API",
    description="Generates Urdu children's stories using a trigram language model with BPE tokenization.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins so the frontend can call from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health():
    """Simple health-check endpoint."""
    return HealthResponse(status="ok", model="trigram", vocab_size=250)


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Generate an Urdu story continuation from a prefix."""
    try:
        vocab = app.state.vocab
        merge_list = app.state.merge_list
        special_tokens = app.state.special_tokens

        # Encode the prefix
        encoded_prefix = encode(request.prefix, vocab, merge_list, special_tokens)

        # Ensure at least 2 tokens for trigram context
        if len(encoded_prefix) < 2:
            encoded_prefix = encoded_prefix + encoded_prefix

        # Stop token is <EOD> (third special token)
        stop_token = special_tokens[2] if len(special_tokens) > 2 else "<EOD>"

        # Generate tokens
        generated_tokens = generate_text(
            prefix_tokens=encoded_prefix,
            unigram_counts=app.state.unigram_counts,
            bigram_counts=app.state.bigram_counts,
            trigram_counts=app.state.trigram_counts,
            total_tokens=app.state.total_tokens,
            vocab=vocab,
            max_length=request.max_length,
            temperature=request.temperature,
            top_k=request.top_k,
            stop_token=stop_token,
        )

        # Decode back to characters
        decoded_tokens = decode(generated_tokens, vocab, merge_list)

        # Post-process into clean Urdu text
        story = postprocess_story(decoded_tokens, special_tokens)

        return GenerateResponse(
            story=story,
            tokens_generated=len(generated_tokens),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Story generation failed: {str(exc)}",
        )
