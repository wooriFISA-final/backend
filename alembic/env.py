import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- ✅ 현재 디렉토리 기준으로 상위 경로를 추가 (models, db 인식용)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.session import DATABASE_URL
from db.base import Base
from models import *   # 모든 모델 import

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# --- DB URL 적용 ---
def get_url():
    return DATABASE_URL

# --- Offline 모드 ---
def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# --- Online 모드 ---
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# --- 실행 ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
