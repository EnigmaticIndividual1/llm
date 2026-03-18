from __future__ import annotations

from flask import Blueprint, render_template, request

from projects.project3_customer_support.service import CustomerSupportService
from shared.config import get_settings


blueprint = Blueprint("project3", __name__, url_prefix="/proyecto-3")

DEFAULT_FORM = {
    "issue_type": "soporte tecnico",
    "customer_name": "",
    "order_id": "",
    "customer_message": "",
    "priority": "media",
}


@blueprint.route("/", methods=["GET", "POST"])
def index():
    settings = get_settings()
    service = CustomerSupportService(settings)
    form_data = DEFAULT_FORM.copy()
    result = None
    error = None

    if request.method == "POST":
        form_data.update(
            {
                "issue_type": request.form.get("issue_type", DEFAULT_FORM["issue_type"]),
                "customer_name": request.form.get("customer_name", "").strip(),
                "order_id": request.form.get("order_id", "").strip(),
                "customer_message": request.form.get("customer_message", "").strip(),
                "priority": request.form.get("priority", DEFAULT_FORM["priority"]),
            }
        )
        try:
            result = service.handle_request(**form_data)
        except Exception as exc:  # pragma: no cover
            error = str(exc)

    return render_template(
        "project3/index.html",
        form_data=form_data,
        result=result,
        error=error,
        api_enabled=settings.api_enabled,
        model_name=settings.openai_model,
        demo_mode=not settings.api_enabled,
    )
