import anthropic
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel, ValidationError

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

def call_llm_structured(messages: list[dict], schema: type[BaseModel], temperature: float = 0, max_tokens: int = 256, system: Optional[str] = None):
    primed = messages + [{"role": "assistant", "content": "{"}]
    raw = call_llm(primed, temperature=temperature, max_tokens=max_tokens, system=system)

    raw = "{" + raw
    try:
        return schema.model_validate_json(raw)
    except ValidationError as e:
        print(f"Validation failed. Raw model output was:\n{raw}")
        raise

class NoteSummary(BaseModel):
    summary: str
    tags: list[str]

if __name__ == "__main__":
    prompt = [{
        "role": "user",
        "content": "Describe Saigon in one sentence."
    }]

    notes = [{
        "role": "user",
        "content": (
            "Summarize these trip notes. Return JSON.\n"
            "- Arrive 5am Sunday, long immigration line.\n"
            "- Hot and humid. Streets crazy busy.\n"
            "- Food sooo good, pho amazing.\n"
            "- War Remnants Museum, heartbreaking.\n"
            "- Cafes and shopping in the evening."
        )
    }]

    system = (
        "You are a JSON API. Return ONLY a valid JSON object, no markdown, "
        "no code fences, no prose. Schema: "
        '{"summary": "<one sentence string>", "tags": ["<string>", ...]}'
    )
    
    result = call_llm_structured(notes, schema=NoteSummary, system=system)
    print(result)
    result = NoteSummary.model_validate_json('{"summary": "oops", "tags": "not-a-list"}')



