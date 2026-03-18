from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from projects.project2_virtual_tutor.demo import DemoVirtualTutor
from shared.config import Settings


TASK_LABELS = {
    "explain": "Explicar concepto",
    "answer": "Responder duda",
    "practice": "Generar practica",
}


@dataclass(frozen=True)
class TutorResponse:
    content: str
    mode: str
    task_label: str


class VirtualTutorService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.demo_tutor = DemoVirtualTutor()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.api_enabled else None

    def handle_request(
        self,
        *,
        task: str,
        topic: str,
        question: str,
        level: str,
        learning_goal: str,
    ) -> TutorResponse:
        self._validate_request(task=task, topic=topic, question=question, learning_goal=learning_goal)
        task_label = TASK_LABELS.get(task, "Tutoria virtual")

        if self.client is None:
            result = self.demo_tutor.respond(
                task=task,
                topic=topic,
                question=question,
                level=level,
                learning_goal=learning_goal,
            )
            return TutorResponse(content=result.content, mode=result.mode, task_label=task_label)

        prompt = self._build_prompt(
            task=task,
            topic=topic,
            question=question,
            level=level,
            learning_goal=learning_goal,
        )
        response = self.client.responses.create(model=self.settings.openai_model, input=prompt)
        return TutorResponse(content=response.output_text.strip(), mode="openai", task_label=task_label)

    def _validate_request(self, *, task: str, topic: str, question: str, learning_goal: str) -> None:
        if task not in TASK_LABELS:
            raise ValueError("La tarea del tutor no es valida.")
        if not topic.strip():
            raise ValueError("Ingresa el tema o materia de estudio.")
        if task == "answer" and not question.strip():
            raise ValueError("Escribe la duda del estudiante para poder responderla.")
        if len(topic) > self.settings.max_input_chars or len(question) > self.settings.max_input_chars:
            raise ValueError("El texto ingresado excede el limite permitido.")
        if len(learning_goal) > self.settings.max_input_chars:
            raise ValueError("El objetivo de aprendizaje es demasiado largo.")

    def _build_prompt(
        self,
        *,
        task: str,
        topic: str,
        question: str,
        level: str,
        learning_goal: str,
    ) -> str:
        task_instructions = {
            "explain": "Explica el concepto de forma clara, progresiva y facil de entender.",
            "answer": "Responde la duda del estudiante con precision y lenguaje pedagogico.",
            "practice": "Genera una actividad breve con solucion o guia de retroalimentacion.",
        }
        return f"""
Eres un tutor virtual inteligente que ensena en espanol.

Tarea: {TASK_LABELS[task]}.
Instruccion: {task_instructions[task]}
Tema: {topic}
Nivel del estudiante: {level}
Objetivo de aprendizaje: {learning_goal or 'Comprender mejor el tema'}
Pregunta del estudiante: {question or 'No aplica'}

Reglas:
- Adapta el lenguaje al nivel del estudiante.
- Organiza la respuesta con claridad.
- Incluye un ejemplo concreto.
- Cierra con una recomendacion breve para continuar aprendiendo.
- Entrega solo la respuesta final.
        """.strip()
