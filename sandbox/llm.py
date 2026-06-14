import anthropic
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

client = anthropic.Anthropic()


def call_llm(messages: list[dict], temperature: float = 0, max_tokens: int = 256, system: Optional[str] = None) -> str:
    kwargs = dict(model="claude-haiku-4-5-20251001", max_tokens=max_tokens, messages=messages, temperature=temperature)
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)

    print("input tokens", response.usage.input_tokens)
    print("output tokens", response.usage.output_tokens)
    input_cost  = response.usage.input_tokens  * (0.80 / 1_000_000)
    output_cost = response.usage.output_tokens * (4.00 / 1_000_000)
    total_cost  = input_cost + output_cost
    print(f"cost in USD ${total_cost:.6f}")

    return response.content[0].text


if __name__ == "__main__":
    prompt = [{
        "role": "user",
        "content": "Describe Saigon in one sentence."
    }]
    print("\n--- No system ---")
    rep1 = call_llm(prompt)
    print(rep1) 

    print("\n--- With system ---")
    rep1 = call_llm(prompt, system="You're a travel ghostwriter. Use only facts. Do not invent anything")
    print(rep1) 




