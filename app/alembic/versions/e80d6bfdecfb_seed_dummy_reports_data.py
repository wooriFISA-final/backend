"""seed dummy reports data

Revision ID: e80d6bfdecfb
Revises: f03fc7c270b2
Create Date: 2025-11-19 22:59:50.852242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'e80d6bfdecfb'
down_revision: Union[str, Sequence[str], None] = 'f03fc7c270b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    reports_table = sa.table(
    "reports",
    sa.column("user_id", sa.BigInteger),
    sa.column("created_at", sa.DateTime),
    sa.column("summarize", sa.Text),
    sa.column("spend_chart_json", sa.JSON),
    sa.column("spend_analysis_text", sa.Text),
    sa.column("policy_changes", sa.Text),
    sa.column("summary_3lines", sa.String),
    sa.column("user_info_changes", sa.Text),
    )
    
    op.bulk_insert(
    reports_table,
        [
            {
                "user_id": 1,
                "created_at": datetime.utcnow(),
                "summarize": "11월 소비 패턴 및 자산 현황을 종합 분석한 리포트입니다.",
                "spend_chart_json": {
                    "period": "2025-11",
                    "total_spend": 1230000,
                    "by_category": [
                        {"category": "식비", "amount": 300000},
                        {"category": "교통", "amount": 150000},
                        {"category": "주거", "amount": 400000},
                        {"category": "문화", "amount": 180000},
                        {"category": "기타", "amount": 30000},
                    ],
                },
                "spend_analysis_text": "식비와 주거비 비중이 전체 소비의 약 57%를 차지합니다...",
                "policy_changes": "주택담보대출 DSR 규제가 2026년부터 일부 완화될 예정입니다...",
                "summary_3lines": "1) 고정비 비중이 다소 높습니다. 2) 여유 자금 일부를 적립식 투자로 전환 가능. 3) 향후 정책 변화를 활용한 대출 리파이낸싱 검토.",
                "user_info_changes": "최근 월 소득이 400 → 450만원으로 증가했습니다.",
            },
            {
                "user_id": 2,
                "created_at": datetime.utcnow(),
                "summarize": "10월~11월 두 달간의 소비 추세를 비교한 리포트입니다.",
                "spend_chart_json": None,
                "spend_analysis_text": "10월 대비 11월에는 교통비와 문화비 지출이 증가했습니다...",
                "policy_changes": None,
                "summary_3lines": "1) 교통비 지출이 일시적으로 상승. 2) 구독형 서비스 점검 필요. 3) 다음 달 예산 상한선 설정 권장.",
                "user_info_changes": None,
            },
        ],
    )


def downgrade():
    """Downgrade schema."""
    # 테스트용이면 그냥 pass 해도 되고,
    # 필요하면 여기서 조건 걸어서 delete 쿼리 날려도 됨
    pass