import os

from huggingface_hub import InferenceClient

from .config import HF_MODEL, HF_TOKEN


client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto",
)


def generate(prompt: str, temperature: float = 0.2) -> str:
    completion = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
        max_tokens=2048,
    )

    content = completion.choices[0].message.content

    if not content:
        raise RuntimeError("Hugging Face returned an empty response.")

    return content.strip()