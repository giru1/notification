import os
from pathlib import Path

import dotenv
import firebase_admin
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class DbSettings(BaseModel):
    db_name: str = os.getenv("DB_NAME")
    db_path: Path = Path(__file__).parent.parent / "db.sqlite3"
    db_username: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASS")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    url: str = f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    url_sync: str = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    echo: bool = bool(int(os.getenv("DB_ECHO")))


class PushSettings(BaseModel):
    fcm_post_url: str = "https://fcm.googleapis.com/fcm/send"
    wp_post_url_chrome: str = fcm_post_url
    wp_post_url_opera: str = fcm_post_url
    wp_post_url_firefox: str = "https://updates.push.services.mozilla.com/wpush/v1"
    wp_post_url_firefox_v2: str = "https://updates.push.services.mozilla.com/wpush/v2"
    wp_post_url_edge: str = "https://wns2-par02p.notify.windows.com/w"
    wp_post_url_safari: str = "https://web.push.apple.com"
    wp_private_key: str = 'credentials/wp/private_key.pem'
    wp_claims: str = {'sub': f"mailto:{os.getenv('MAILTO')}"}
    fcm_max_recipients: int = 1000
    google_application_credentials: str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    def get_wp_post_url(self, browser_name: str) -> str:
        mapper = {
            "CHROME": self.wp_post_url_chrome,
            "OPERA": self.wp_post_url_opera,
            "FIREFOXv1": self.wp_post_url_firefox,
            "FIREFOXv2": self.wp_post_url_firefox,
            "EDGE": self.wp_post_url_edge,
            "SAFARI": self.wp_post_url_safari
        }
        return mapper.get(browser_name)


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    push_settings: PushSettings = PushSettings()
    rabbit_con_url: str = (f"amqp://{os.getenv("RABBITMQ_USER")}:"
                           f"{os.getenv("RABBITMQ_PASS")}@{os.getenv("RABBITMQ_HOST")}:"
                           f"{os.getenv("RABBITMQ_PORT")}/")
    rabbit_queue_name: str = os.getenv("QUEUE_NAME")


settings = Settings()
fcm_app: firebase_admin.App = firebase_admin.initialize_app()
