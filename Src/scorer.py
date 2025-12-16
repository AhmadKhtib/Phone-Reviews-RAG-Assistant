from dataclasses import dataclass
from typing import List, Tuple
from langchain_core.documents import Document


@dataclass
class UseCaseWeights:
    performance: float = 0.0
    camera: float = 0.0
    battery: float = 0.0
    display: float = 0.0


def detect_usecase(question: str) -> UseCaseWeights:
    q = question.lower()

    # defaults: light balanced recommendation
    w = UseCaseWeights(performance=0.25, camera=0.25, battery=0.25, display=0.25)

    if any(k in q for k in ["game", "gaming", "gamer", "fps", "pubg", "cod", "fortnite"]):
        return UseCaseWeights(performance=0.50, display=0.30, battery=0.15, camera=0.05)

    if any(k in q for k in ["camera", "photo", "photos", "video", "portrait", "selfie"]):
        return UseCaseWeights(camera=0.55, display=0.15, performance=0.15, battery=0.15)

    if any(k in q for k in ["battery", "long lasting", "all day", "power", "endurance"]):
        return UseCaseWeights(battery=0.55, performance=0.15, display=0.15, camera=0.15)

    return w


def _safe_float(x) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def score_docs(docs: List[Document], weights: UseCaseWeights) -> List[Tuple[float, Document]]:
    scored = []
    for d in docs:
        md = d.metadata or {}
        perf = _safe_float(md.get("performance_rating"))
        cam = _safe_float(md.get("camera_rating"))
        batt = _safe_float(md.get("battery_life_rating"))
        disp = _safe_float(md.get("display_rating"))

        # rating can be used as a small stabilizer
        overall = _safe_float(md.get("rating"))

        score = (
            weights.performance * perf +
            weights.camera * cam +
            weights.battery * batt +
            weights.display * disp +
            0.10 * overall
        )
        scored.append((score, d))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored
