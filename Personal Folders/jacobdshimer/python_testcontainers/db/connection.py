from contextlib import contextmanager

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.engine.base import Engine

from settings import Settings


class Connection:
    _instance: 'Connection' = None
    engine: Engine = None
    settings: Settings = None

    @classmethod
    def init(cls, settings: Settings | None = None, debug: bool = False):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            if settings:
                cls._instance.settings = settings
            else:
                cls._instance.settings = Settings()

            print(cls._instance.settings)
            cls._instance.engine = create_engine('postgresql+psycopg://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'.format(
                **cls._instance.settings.model_dump()
            ), echo=debug)

            return cls._instance
        else:
            raise RuntimeError('instance of connection already exists')

    @classmethod
    def instance(cls):
        return cls._instance

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def __repr__(self) -> str:
        return f'{self.settings=}, {self.engine=}'
