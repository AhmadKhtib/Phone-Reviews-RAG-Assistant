from dataclasses import dataclass

@dataclass(frozen=True)
class Intent:
    name: str  # "qa" | "recommend" | "list_brands"


def detect_intent(question: str) -> Intent:
    q = question.strip().lower()

    # list/metadata intents
    if ("list" in q or "show" in q) and ("brand" in q or "brands" in q):
        return Intent("list_brands")

    # recommendation intents
    if any(w in q for w in ["recommend", "choose", "suggest", "pick", "best phone", "best phones"]):
        return Intent("recommend")

    # default: Q&A
    return Intent("qa")
