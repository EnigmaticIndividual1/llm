from __future__ import annotations

from flask import Blueprint, render_template, request

from projects.project1_writing_assistant.service import TASK_LABELS, WritingAssistantService
from shared.config import get_settings


blueprint = Blueprint("project1", __name__, url_prefix="/proyecto-1")

DEFAULT_FORM = {
    "task": "generate",
    "brief": "",
    "source_text": "",
    "tone": "professional",
    "audience": "un cliente potencial",
    "target_length": "media",
}


@blueprint.route("/", methods=["GET", "POST"])
def index():
    settings = get_settings()
    service = WritingAssistantService(settings)
    form_data = DEFAULT_FORM.copy()
    result = None
    error = None

    if request.method == "POST":
        form_data.update(
            {
                "task": request.form.get("task", DEFAULT_FORM["task"]),
                "brief": request.form.get("brief", "").strip(),
                "source_text": request.form.get("source_text", "").strip(),
                "tone": request.form.get("tone", DEFAULT_FORM["tone"]),
                "audience": request.form.get("audience", "").strip(),
                "target_length": request.form.get("target_length", DEFAULT_FORM["target_length"]),
            }
        )
        try:
            result = service.handle_request(**form_data)
        except Exception as exc:  # pragma: no cover
            error = str(exc)

    return render_template(
        "project1/index.html",
        form_data=form_data,
        result=result,
        error=error,
        task_labels=TASK_LABELS,
        api_enabled=settings.api_enabled,
        model_name=settings.openai_model,
        demo_mode=not settings.api_enabled,
    )
