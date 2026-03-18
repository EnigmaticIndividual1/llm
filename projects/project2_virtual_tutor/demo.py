from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TutorDemoResult:
    content: str
    mode: str = "demo"


class DemoVirtualTutor:
    def respond(
        self,
        *,
        task: str,
        topic: str,
        question: str,
        level: str,
        learning_goal: str,
    ) -> TutorDemoResult:
        handlers = {
            "explain": self._explain,
            "answer": self._answer_question,
            "practice": self._practice,
        }
        handler = handlers.get(task, self._explain)
        return TutorDemoResult(content=handler(topic=topic, question=question, level=level, learning_goal=learning_goal))

    def _explain(self, *, topic: str, question: str, level: str, learning_goal: str) -> str:
        return (
            f"Explicacion guiada sobre {topic} para nivel {level}:\n\n"
            f"{topic} puede entenderse como un conjunto de ideas conectadas que se aplican para cumplir el objetivo de {learning_goal or 'aprender el tema'}.\n"
            "Primero identifica la idea central, luego observa un ejemplo concreto y finalmente practica con un caso sencillo.\n\n"
            "Ejemplo:\n"
            f"Si tuvieras que explicar {topic}, empezarias definiendo el concepto, mostrando una aplicacion real y cerrando con una regla practica para recordarlo.\n\n"
            "Siguiente paso:\n"
            "Intenta resumir el concepto en dos oraciones usando tus propias palabras."
        )

    def _answer_question(self, *, topic: str, question: str, level: str, learning_goal: str) -> str:
        return (
            f"Respuesta a la duda del estudiante:\n\n"
            f"Pregunta: {question}\n\n"
            f"Para responderla, conviene relacionar la pregunta con el tema {topic}. "
            f"En nivel {level}, la mejor estrategia es dividir la idea en partes pequenas, explicar cada una y verificar si ya puedes describirla con un ejemplo propio.\n\n"
            "Verificacion rapida:\n"
            "- Que significa el concepto.\n"
            "- Para que sirve.\n"
            "- Como lo aplicarias en un ejercicio sencillo."
        )

    def _practice(self, *, topic: str, question: str, level: str, learning_goal: str) -> str:
        return (
            f"Practica guiada sobre {topic}:\n\n"
            "1. Define el concepto principal con tus propias palabras.\n"
            "2. Escribe un ejemplo de uso o aplicacion.\n"
            "3. Resuelve una mini pregunta de comprobacion.\n\n"
            "Mini pregunta:\n"
            f"Como explicarias {topic} a otra persona de nivel {level} en menos de un minuto?\n\n"
            "Retroalimentacion esperada:\n"
            "Una buena respuesta incluye definicion, ejemplo y una conclusion corta."
        )
