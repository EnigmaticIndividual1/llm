from __future__ import annotations

from flask import Blueprint, render_template, request

from projects.project2_virtual_tutor.service import TASK_LABELS, VirtualTutorService
from shared.config import get_settings


blueprint = Blueprint("project2", __name__, url_prefix="/proyecto-2")

DEFAULT_FORM = {
    "task": "explain",
    "topic": "",
    "question": "",
    "level": "secundaria",
    "learning_goal": "entender el concepto principal",
}


@blueprint.route("/", methods=["GET", "POST"])
def index():
    settings = get_settings()
    service = VirtualTutorService(settings)
    form_data = DEFAULT_FORM.copy()
    result = None
    error = None

    if request.method == "POST":
        form_data.update(
            {
                "task": request.form.get("task", DEFAULT_FORM["task"]),
                "topic": request.form.get("topic", "").strip(),
                "question": request.form.get("question", "").strip(),
                "level": request.form.get("level", DEFAULT_FORM["level"]),
                "learning_goal": request.form.get("learning_goal", "").strip(),
            }
        )
        try:
            result = service.handle_request(**form_data)
        except Exception as exc:  # pragma: no cover
            error = str(exc)

    return render_template(
        "project2/index.html",
        form_data=form_data,
        result=result,
        error=error,
        task_labels=TASK_LABELS,
        api_enabled=settings.api_enabled,
        model_name=settings.openai_model,
        demo_mode=not settings.api_enabled,
    )
