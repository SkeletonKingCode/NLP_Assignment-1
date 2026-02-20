// frontend/lib/api.js

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function generateStory({ prefix, maxLength, temperature, topK }) {
  const response = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prefix,
      max_length: maxLength,
      temperature,
      top_k: topK,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Server error: ${response.status}`);
  }

  return response.json(); // { story, tokens_generated }
}

export async function checkHealth() {
  try {
    const response = await fetch(`${BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
