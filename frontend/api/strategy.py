from api.client import post


def recommend_strategy(
    *,
    project_id: int,
    mode: str,
    reuse_tone: bool,
    platform: str,
    poster_size: str | None,
    goal: str | None,
    style: str | None,
) -> dict:
    return post(
        "/strategy/recommend",
        json={
            "project_id": project_id,
            "strategy": {
                "mode": mode,
                "reuse_tone": reuse_tone,
                "platform": platform,
                "poster_size": poster_size,
                "goal": goal,
                "style": style,
            },
        },
    )