from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    secret_key: str
    openai_api_key: str | None
    openai_model: str
    use_demo_mode: bool
    max_input_chars: int

    @property
    def api_enabled(self) -> bool:
        return bool(self.openai_api_key) and not self.use_demo_mode


def get_settings() -> Settings:
    return Settings(
        secret_key=os.getenv("FLASK_SECRET_KEY", "dev-secret-key"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        use_demo_mode=os.getenv("OPENAI_USE_DEMO", "false").lower() == "true",
        max_input_chars=int(os.getenv("MAX_INPUT_CHARS", "5000")),
    )
