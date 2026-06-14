import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def call_llm(messages: list[dict], temperature: float = 0, max_tokens: int = 256) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max_tokens,
        messages=messages,
        temperature=temperature
    )
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
    print("\n--- Temp 0 ---")
    for _ in range(3):
        rep1 = call_llm(prompt)
        print(rep1) 

    print("\n--- Temp 1 ---")
    for _ in range(3):
        rep1 = call_llm(prompt, temperature=1)
        print(rep1) 

    





