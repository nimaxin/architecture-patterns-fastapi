from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import settings

db_url = URL.create(
    drivername=settings.db_driver,
    username=settings.db_user,
    password=settings.db_pass,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
).render_as_string(hide_password=False)


engine_kwargs = {}

if settings.db_driver.startswith("sqlite"):
    engine_kwargs.update(
        connect_args={"check_same_thread": False},
    )
else:
    engine_kwargs.update(
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_recycle=settings.db_pool_recycle,
        pool_timeout=settings.db_pool_timeout,
    )

engine = create_async_engine(
    url=db_url,
    **engine_kwargs,
)

Session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
