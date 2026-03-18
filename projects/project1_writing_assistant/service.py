from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from projects.project1_writing_assistant.demo import DemoWritingAssistant
from shared.config import Settings


TASK_LABELS = {
    "generate": "Generar borrador",
    "improve": "Mejorar estilo",
    "correct": "Corregir gramatica",
    "summarize": "Resumir contenido",
}


@dataclass(frozen=True)
class WritingResponse:
    content: str
    mode: str
    task_label: str


class WritingAssistantService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.demo_assistant = DemoWritingAssistant()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.api_enabled else None

    def handle_request(
        self,
        *,
        task: str,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> WritingResponse:
        self._validate_request(task=task, brief=brief, source_text=source_text)
        task_label = TASK_LABELS.get(task, "Asistencia de escritura")

        if self.client is None:
            demo_result = self.demo_assistant.respond(
                task=task,
                brief=brief,
                source_text=source_text,
                tone=tone,
                audience=audience,
                target_length=target_length,
            )
            return WritingResponse(content=demo_result.content, mode=demo_result.mode, task_label=task_label)

        prompt = self._build_prompt(
            task=task,
            brief=brief,
            source_text=source_text,
            tone=tone,
            audience=audience,
            target_length=target_length,
        )
        response = self.client.responses.create(model=self.settings.openai_model, input=prompt)
        return WritingResponse(content=response.output_text.strip(), mode="openai", task_label=task_label)

    def _validate_request(self, *, task: str, brief: str, source_text: str) -> None:
        if task not in TASK_LABELS:
            raise ValueError("La tarea seleccionada no es valida.")
        if task == "generate" and not brief.strip():
            raise ValueError("Describe brevemente el texto que quieres generar.")
        if task in {"improve", "correct", "summarize"} and not source_text.strip():
            raise ValueError("Ingresa un texto para procesarlo.")
        if len(brief) > self.settings.max_input_chars:
            raise ValueError("La descripcion del encargo es demasiado larga.")
        if len(source_text) > self.settings.max_input_chars:
            raise ValueError("El texto original excede el limite permitido.")

    def _build_prompt(
        self,
        *,
        task: str,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> str:
        task_instructions = {
            "generate": "Genera un borrador listo para usar. Organiza el contenido con claridad.",
            "improve": "Reescribe el texto para que sea mas claro, fluido y profesional sin cambiar su idea central.",
            "correct": "Corrige ortografia, puntuacion y gramatica. Conserva el sentido original.",
            "summarize": "Resume el texto en un formato breve y facil de leer. Destaca la idea principal y los puntos clave.",
        }
        return f"""
Eres un asistente de escritura en espanol para usuarios finales.

Tu tarea: {TASK_LABELS[task]}.
Instruccion especifica: {task_instructions[task]}
Tono solicitado: {tone}.
Audiencia objetivo: {audience or 'general'}.
Longitud deseada: {target_length}.

Contexto del encargo:
{brief or 'No aplica.'}

Texto base del usuario:
{source_text or 'No aplica.'}

Reglas:
- Entrega unicamente el texto final.
- No incluyas notas metodologicas.
- Si el usuario pide generar un borrador, inventa contenido util y coherente.
- Si el texto base esta en otro idioma, manten ese idioma.
        """.strip()
