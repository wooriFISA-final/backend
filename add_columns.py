import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# .env 파일 로드 시도 (프로젝트 루트 및 backend 폴더)
load_dotenv()
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))

def add_columns():
    # 환경변수에서 DB 정보 읽기 (기본값 설정)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "fisa")
    
    # 비밀번호가 비어있으면 경고
    if not DB_PASSWORD:
        print("⚠️ 경고: DB_PASSWORD 환경변수가 설정되지 않았습니다. 접속에 실패할 수 있습니다.")
    
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # 보안을 위해 비밀번호 마스킹하여 출력
    masked_url = DATABASE_URL.replace(DB_PASSWORD, "****") if DB_PASSWORD else DATABASE_URL
    print(f"DB 연결 시도: {masked_url}")
    
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("✅ DB 연결 성공! 컬럼 추가 작업 시작...")
            
            # 1. trend_chart_json 컬럼 추가
            try:
                conn.execute(text("ALTER TABLE reports ADD COLUMN trend_chart_json JSON COMMENT '월별 투자 수익률 추이 그래프 데이터'"))
                print("✅ trend_chart_json 컬럼 추가 성공")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print("ℹ️ trend_chart_json 컬럼이 이미 존재합니다.")
                else:
                    print(f"ℹ️ trend_chart_json 컬럼 추가 건너뜀: {e}")
                
            # 2. fund_comparison_json 컬럼 추가
            try:
                conn.execute(text("ALTER TABLE reports ADD COLUMN fund_comparison_json JSON COMMENT '펀드 상품별 손익 비교 그래프 데이터'"))
                print("✅ fund_comparison_json 컬럼 추가 성공")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print("ℹ️ fund_comparison_json 컬럼이 이미 존재합니다.")
                else:
                    print(f"ℹ️ fund_comparison_json 컬럼 추가 건너뜀: {e}")
                
            conn.commit()
            print("작업 완료.")
            
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
        print("환경변수(.env) 파일이 올바른 위치에 있는지, DB 서버가 실행 중인지 확인해주세요.")

if __name__ == "__main__":
    add_columns()
