import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cotacol import crud, models
from cotacol.db import Base, get_db
from cotacol.main import app


engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def staff_user():
    db = TestingSessionLocal()
    db.add(models.User(username="staff", is_staff=True))
    db.commit()
    yield db.query(models.User).filter(models.User.username == "staff").first()


@pytest.fixture
def climb():
    db = TestingSessionLocal()
    koppenberg_id = 551
    climb = crud.get_climb(db, koppenberg_id)

    if not climb:
        db.add(
            models.Climb(
                id=koppenberg_id,
                name="Koppenberg",
                city="Melden",
                province="Oost-Vl",
                cotacol_points=172,
                distance=600,
                elevation_diff=65,
                avg_grade=10.8,
                surface="cobbles",
                aliases=[],
            )
        )
        db.commit()
        climb = crud.get_climb(db, koppenberg_id)

    yield climb
