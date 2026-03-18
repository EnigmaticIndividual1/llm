from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from projects.project3_customer_support.demo import DemoCustomerSupport
from shared.config import Settings


@dataclass(frozen=True)
class SupportResponse:
    content: str
    lookup_status: str
    mode: str


class CustomerSupportService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.demo_support = DemoCustomerSupport()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.api_enabled else None

    def handle_request(
        self,
        *,
        issue_type: str,
        customer_name: str,
        order_id: str,
        customer_message: str,
        priority: str,
    ) -> SupportResponse:
        self._validate_request(
            issue_type=issue_type,
            customer_name=customer_name,
            order_id=order_id,
            customer_message=customer_message,
        )
        lookup_status = self._simulate_lookup(customer_name=customer_name, order_id=order_id)

        if self.client is None:
            result = self.demo_support.respond(
                issue_type=issue_type,
                customer_name=customer_name,
                order_id=order_id,
                customer_message=customer_message,
                priority=priority,
            )
            return SupportResponse(content=result.content, lookup_status=result.lookup_status, mode=result.mode)

        prompt = self._build_prompt(
            issue_type=issue_type,
            customer_name=customer_name,
            order_id=order_id,
            customer_message=customer_message,
            priority=priority,
            lookup_status=lookup_status,
        )
        response = self.client.responses.create(model=self.settings.openai_model, input=prompt)
        return SupportResponse(content=response.output_text.strip(), lookup_status=lookup_status, mode="openai")

    def _validate_request(
        self,
        *,
        issue_type: str,
        customer_name: str,
        order_id: str,
        customer_message: str,
    ) -> None:
        if not issue_type.strip():
            raise ValueError("Selecciona el tipo de consulta del cliente.")
        if not customer_message.strip():
            raise ValueError("Escribe el mensaje del cliente.")
        if len(customer_name) > self.settings.max_input_chars:
            raise ValueError("El nombre del cliente es demasiado largo.")
        if len(order_id) > self.settings.max_input_chars:
            raise ValueError("El numero de orden es demasiado largo.")
        if len(customer_message) > self.settings.max_input_chars:
            raise ValueError("El mensaje del cliente excede el limite permitido.")

    def _simulate_lookup(self, *, customer_name: str, order_id: str) -> str:
        order_text = order_id or "sin orden proporcionada"
        name_text = customer_name or "cliente sin nombre"
        return f"Consultando base de datos de clientes: cliente={name_text}, orden={order_text}."

    def _build_prompt(
        self,
        *,
        issue_type: str,
        customer_name: str,
        order_id: str,
        customer_message: str,
        priority: str,
        lookup_status: str,
    ) -> str:
        return f"""
Eres un agente de atencion al cliente que responde en espanol.

Tipo de consulta: {issue_type}
Nombre del cliente: {customer_name or 'No proporcionado'}
Numero de orden: {order_id or 'No proporcionado'}
Prioridad: {priority}
Mensaje del cliente:
{customer_message}

Simulacion del sistema interno:
{lookup_status}

Reglas:
- Responde con tono profesional, empatico y claro.
- Ofrece un siguiente paso concreto.
- Si falta informacion, pidela de forma puntual.
- No prometas acciones que no esten respaldadas por el contexto.
- Entrega solo la respuesta final para el cliente.
        """.strip()
