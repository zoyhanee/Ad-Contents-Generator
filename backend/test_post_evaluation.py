from pprint import pprint

from app.db.database import SessionLocal
from app.services.evaluation_service import (
    build_ad_evaluation_request,
    evaluate_generated_ad,
    save_ad_evaluation,
)


def main():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("AUTO POST EVALUATION TEST")
        print("=" * 60)

        # 1. DB에서 평가 입력 자동 구성
        print("\n[1] 평가 입력 자동 구성")

        evaluation_input = build_ad_evaluation_request(
            db=db,
            project_id=1,
            draft_id=1,
        )

        pprint(
            evaluation_input.model_dump(),
            sort_dicts=False,
        )

        # 2. 광고 사후 평가
        print("\n[2] 광고 사후 평가")

        evaluation = evaluate_generated_ad(
            evaluation_input
        )

        pprint(
            evaluation.model_dump(),
            sort_dicts=False,
        )

        # 3. DB 저장
        print("\n[3] 평가 결과 저장")

        saved = save_ad_evaluation(
            db=db,
            project_id=evaluation_input.project_id,
            draft_id=evaluation_input.draft_id,
            evaluation=evaluation,
        )

        print(
            f"저장 완료: "
            f"evaluation_id={saved.id}, "
            f"draft_id={saved.draft_id}, "
            f"overall_score={saved.overall_score}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()