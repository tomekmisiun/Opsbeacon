from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.monitor import Monitor

DEMO_MONITORS = [
    ("GitHub", "https://github.com"),
    ("Cloudflare", "https://www.cloudflare.com"),
    ("Python", "https://www.python.org"),
]


def seed() -> None:
    with SessionLocal() as db:
        for name, url in DEMO_MONITORS:
            exists = db.scalar(select(Monitor).where(Monitor.url == url))
            if not exists:
                db.add(Monitor(name=name, url=url))
        db.commit()


if __name__ == "__main__":
    seed()
