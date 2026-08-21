import socket
import threading
import time
import urllib.request

import pytest
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture()
def db() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionTesting = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with SessionTesting() as session:
        yield session


@pytest.fixture()
def live_server(db: Session) -> str:
    app.dependency_overrides[get_db] = lambda: db
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=port, log_level="critical", lifespan="off")
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(f"{base_url}/health", timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.05)
    else:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("test server did not start")

    yield base_url

    server.should_exit = True
    thread.join(timeout=5)
    app.dependency_overrides.clear()
