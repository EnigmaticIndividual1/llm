from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template

from projects.project1_writing_assistant.routes import blueprint as project1_blueprint
from projects.project2_virtual_tutor.routes import blueprint as project2_blueprint
from projects.project3_customer_support.routes import blueprint as project3_blueprint
from shared.config import get_settings


def create_app() -> Flask:
    project_root = Path(__file__).resolve().parent
    settings = get_settings()

    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config["SECRET_KEY"] = settings.secret_key

    app.register_blueprint(project1_blueprint)
    app.register_blueprint(project2_blueprint)
    app.register_blueprint(project3_blueprint)

    @app.get("/")
    def home():
        projects = [
            {
                "title": "Proyecto 1",
                "subtitle": "Asistente de escritura automatica",
                "description": "Genera borradores, mejora estilo, corrige gramatica y resume contenido.",
                "endpoint": "project1.index",
            },
            {
                "title": "Proyecto 2",
                "subtitle": "Tutor virtual inteligente",
                "description": "Explica conceptos, responde dudas y propone practica guiada.",
                "endpoint": "project2.index",
            },
            {
                "title": "Proyecto 3",
                "subtitle": "Atencion al cliente automatizada",
                "description": "Simula soporte conversacional con respuestas utiles y contexto de cliente.",
                "endpoint": "project3.index",
            },
        ]
        return render_template(
            "home.html",
            projects=projects,
            api_enabled=settings.api_enabled,
            model_name=settings.openai_model,
            demo_mode=not settings.api_enabled,
        )

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app
