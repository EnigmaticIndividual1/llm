from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DemoResult:
    content: str
    mode: str = "demo"


class DemoWritingAssistant:
    def respond(
        self,
        *,
        task: str,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> DemoResult:
        handlers = {
            "generate": self._generate_draft,
            "improve": self._improve_text,
            "correct": self._correct_text,
            "summarize": self._summarize_text,
        }
        handler = handlers.get(task, self._generate_draft)
        content = handler(
            brief=brief,
            source_text=source_text,
            tone=tone,
            audience=audience,
            target_length=target_length,
        )
        return DemoResult(content=content)

    def _generate_draft(
        self,
        *,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> str:
        return (
            f"Hola,\n\n"
            f"Comparto un primer borrador sobre {brief.strip() or 'el tema indicado'} para {audience}.\n"
            f"El tono solicitado es {tone} y la extension esperada es {target_length}.\n\n"
            "Texto sugerido:\n"
            f"Este borrador desarrolla la idea central con una estructura clara, beneficios concretos "
            f"y un cierre accionable. El contenido esta pensado para conectar con {audience} de forma {tone}.\n\n"
            "Cierre sugerido:\n"
            "Quedo atento a tus comentarios para hacer ajustes y ampliar cualquier punto necesario."
        )

    def _improve_text(
        self,
        *,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> str:
        cleaned = self._normalize_text(source_text)
        sentences = self._split_sentences(cleaned) or [
            "No se recibio texto suficiente para mejorar, por lo que se genero una version base."
        ]
        refined = " ".join(sentence.capitalize() for sentence in sentences)
        return (
            f"Version mejorada para {audience} con tono {tone}:\n\n"
            f"{refined}\n\n"
            "Ajustes aplicados en modo demo:\n"
            "- Se clarifico la redaccion.\n"
            "- Se eliminaron repeticiones visibles.\n"
            "- Se mejoro la fluidez general."
        )

    def _correct_text(
        self,
        *,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> str:
        corrected = self._normalize_text(source_text)
        corrected = re.sub(r"\s+([,.;:!?])", r"\1", corrected)
        corrected = corrected[:1].upper() + corrected[1:] if corrected else corrected
        if corrected and corrected[-1] not in ".!?":
            corrected = f"{corrected}."
        return (
            "Texto corregido:\n\n"
            f"{corrected or 'No se proporciono texto para corregir.'}\n\n"
            "Cambios simulados en modo demo:\n"
            "- Espacios y puntuacion normalizados.\n"
            "- Inicio de oracion capitalizado."
        )

    def _summarize_text(
        self,
        *,
        brief: str,
        source_text: str,
        tone: str,
        audience: str,
        target_length: str,
    ) -> str:
        cleaned = self._normalize_text(source_text)
        sentences = self._split_sentences(cleaned)
        short_summary = " ".join(sentences[:2]).strip() or "No se encontro contenido suficiente para resumir."
        keywords = [word for word in re.findall(r"[A-Za-z0-9áéíóúÁÉÍÓÚñÑ]+", cleaned) if len(word) > 5]
        highlights = ", ".join(dict.fromkeys(keywords[:4])) or "sin palabras clave destacadas"
        return f"Resumen:\n\n{short_summary}\n\nPuntos clave: {highlights}."

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _split_sentences(self, text: str) -> list[str]:
        return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
