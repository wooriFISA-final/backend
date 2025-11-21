"""seed user_consume from json

Revision ID: 6e333f76f4d4
Revises: e80d6bfdecfb
Create Date: 2025-11-20 16:53:42.066468

"""
from typing import Sequence, Union
from pathlib import Path
from datetime import datetime
import json

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6e333f76f4d4"
down_revision: Union[str, Sequence[str], None] = "e80d6bfdecfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_user_consume_table(bind) -> sa.Table:
    """user_consume 테이블 리플렉션"""
    metadata = sa.MetaData()
    metadata.bind = bind
    return sa.Table("user_consume", metadata, autoload_with=bind)


def _load_json() -> list[dict]:
    """
    JSON 파일을 읽어서 list[dict] 로 반환.

    - 최상위가 리스트인 경우: 그대로 사용
    - 최상위가 dict인 경우:
      1) 'data' / 'items' / 'rows' 키에 리스트가 있으면 그걸 사용
      2) 그 외에는 value 들을 전부 리스트로 묶어서 사용
    """
    # 이 파일 경로: backend/app/alembic/versions/xxx.py 라고 가정
    # parents[0] = versions, [1] = alembic, [2] = app, [3] = backend
    base_dir = Path(__file__).resolve().parents[3]  # backend/
    json_path = base_dir / "app" / "data" / "jinsoo_data.json"

    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 1) 이미 리스트인 경우 그대로 반환
    if isinstance(data, list):
        return data

    # 2) dict 인 경우: 흔한 패턴 처리 (예: {"data": [ ... ]})
    if isinstance(data, dict):
        # 우선 data/items/rows 키에 리스트가 있으면 그걸 사용
        for key in ("data", "items", "rows"):
            if key in data and isinstance(data[key], list):
                return data[key]

        # 그렇지 않다면, value 들이 개별 레코드일 가능성이 있으므로
        # value 들만 모아서 리스트로 사용 (dict 인 것만 필터링)
        values = list(data.values())
        rows = [v for v in values if isinstance(v, dict)]
        if rows:
            return rows

    # 여기까지 왔다는 것은 우리가 예상한 형태가 아니라는 뜻
    raise ValueError(
        "JSON 구조를 파싱할 수 없습니다. "
        "최상위는 리스트이거나, {'data': [...]} / {'2022-11': {...}} 같은 dict 구조여야 합니다."
    )


def upgrade() -> None:
    """
    JSON 파일 내용을 읽어 user_consume 테이블에 INSERT
    """
    bind = op.get_bind()
    user_consume = _get_user_consume_table(bind)

    json_rows = _load_json()

    # JSON 키 -> DB 컬럼명 매핑 (슬래시/공백 처리)
    key_map = {
        # CAT1
        "CAT1_교육/문화": "CAT1_교육_문화",
        "CAT1_생활/주거": "CAT1_생활_주거",
        "CAT1_레저/여행": "CAT1_레저_여행",
        "CAT1_기타 지출": "CAT1_기타_지출",
        # CAT2
        "CAT2_자가용/연료": "CAT2_자가용_연료",
        "CAT2_택시/대리": "CAT2_택시_대리",
        "CAT2_항공/기차": "CAT2_항공_기차",
        "CAT2_잡화/뷰티": "CAT2_잡화_뷰티",
        "CAT2_명품/쥬얼리": "CAT2_명품_쥬얼리",
        "CAT2_외식/배달": "CAT2_외식_배달",
        "CAT2_가정식/식재료": "CAT2_가정식_식재료",
        "CAT2_주점/유흥": "CAT2_주점_유흥",
        "CAT2_커피/음료": "CAT2_커피_음료",
        "CAT2_사교육/학원": "CAT2_사교육_학원",
        "CAT2_도서/음반": "CAT2_도서_음반",
        "CAT2_문화생활/취미": "CAT2_문화생활_취미",
        "CAT2_공과금/통신": "CAT2_공과금_통신",
        "CAT2_병원/약국": "CAT2_병원_약국",
        "CAT2_인테리어/가구": "CAT2_인테리어_가구",
        "CAT2_보험/금융": "CAT2_보험_금융",
        "CAT2_국내여행/숙박": "CAT2_국내여행_숙박",
        "CAT2_해외여행/항공": "CAT2_해외여행_항공",
        "CAT2_레포츠/취미": "CAT2_레포츠_취미",
        "CAT2_기타 여가": "CAT2_기타_여가",
        "CAT2_자격증/어학": "CAT2_자격증_어학",
        "CAT2_운동/피트니스": "CAT2_운동_피트니스",
        "CAT2_온라인 구독": "CAT2_온라인_구독",
        "CAT2_도구/재료 구매": "CAT2_도구_재료_구매",
        "CAT2_경조사/기부": "CAT2_경조사_기부",
        "CAT2_해외 직구": "CAT2_해외_직구",
        "CAT2_금융 수수료": "CAT2_금융_수수료",
    }

    # user_id는 현재는 1(유진수)로 고정
    fixed_user_id = 1

    rows_to_insert: list[dict] = []

    for item in json_rows:
        # "2022-11" -> date(2022-11-01)
        ym = item.get("spend_month")
        if not ym:
            continue
        spend_month = datetime.strptime(ym + "-01", "%Y-%m-%d").date()

        total_spend = item.get("total_spend", 0)

        # 기본 row 틀 (모든 컬럼 0으로 초기화)
        row = {
            "user_id": fixed_user_id,
            "spend_month": spend_month,
            "total_spend": int(total_spend) if total_spend is not None else 0,
            # CAT1
            "CAT1_교통": 0,
            "CAT1_쇼핑": 0,
            "CAT1_식품": 0,
            "CAT1_교육_문화": 0,
            "CAT1_생활_주거": 0,
            "CAT1_레저_여행": 0,
            "CAT1_자기계발": 0,
            "CAT1_기타_지출": 0,
            # CAT2
            "CAT2_대중교통": 0,
            "CAT2_자가용_연료": 0,
            "CAT2_택시_대리": 0,
            "CAT2_항공_기차": 0,
            "CAT2_의류": 0,
            "CAT2_잡화_뷰티": 0,
            "CAT2_명품_쥬얼리": 0,
            "CAT2_전자제품": 0,
            "CAT2_외식_배달": 0,
            "CAT2_가정식_식재료": 0,
            "CAT2_주점_유흥": 0,
            "CAT2_커피_음료": 0,
            "CAT2_사교육_학원": 0,
            "CAT2_도서_음반": 0,
            "CAT2_문화생활_취미": 0,
            "CAT2_온라인강의": 0,
            "CAT2_공과금_통신": 0,
            "CAT2_병원_약국": 0,
            "CAT2_인테리어_가구": 0,
            "CAT2_보험_금융": 0,
            "CAT2_국내여행_숙박": 0,
            "CAT2_해외여행_항공": 0,
            "CAT2_레포츠_취미": 0,
            "CAT2_기타_여가": 0,
            "CAT2_자격증_어학": 0,
            "CAT2_운동_피트니스": 0,
            "CAT2_온라인_구독": 0,
            "CAT2_도구_재료_구매": 0,
            "CAT2_현금서비스": 0,
            "CAT2_경조사_기부": 0,
            "CAT2_해외_직구": 0,
            "CAT2_금융_수수료": 0,
        }

        # item의 각 키를 DB 컬럼으로 매핑해서 값 세팅
        for k, v in item.items():
            if k in ("spend_month", "total_spend"):
                continue

            # 매핑 딕셔너리 적용 (없으면 그대로)
            col = key_map.get(k, k)

            if col in row:
                row[col] = int(v) if v is not None else 0

        rows_to_insert.append(row)

    if rows_to_insert:
        bind.execute(sa.insert(user_consume), rows_to_insert)


def downgrade() -> None:
    """
    seed 데이터 롤백:
    JSON에 포함된 month + user_id=1 조건으로 DELETE
    """
    bind = op.get_bind()
    user_consume = _get_user_consume_table(bind)
    json_rows = _load_json()

    fixed_user_id = 1
    months = []

    for item in json_rows:
        ym = item.get("spend_month")
        if ym:
            months.append(datetime.strptime(ym + "-01", "%Y-%m-%d").date())

    if months:
        delete_stmt = (
            sa.delete(user_consume)
            .where(user_consume.c.user_id == fixed_user_id)
            .where(user_consume.c.spend_month.in_(months))
        )
        bind.execute(delete_stmt)
