from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SupportDemoResult:
    content: str
    lookup_status: str
    mode: str = "demo"


class DemoCustomerSupport:
    def respond(
        self,
        *,
        issue_type: str,
        customer_name: str,
        order_id: str,
        customer_message: str,
        priority: str,
    ) -> SupportDemoResult:
        lookup_status = self._simulate_lookup(customer_name=customer_name, order_id=order_id)
        reply = (
            f"Hola {customer_name or 'cliente'},\n\n"
            f"Hemos recibido tu consulta sobre {issue_type}. "
            f"Nuestro sistema identifico la solicitud con prioridad {priority} y ya estamos revisando el caso.\n\n"
            f"Respuesta sugerida:\n"
            f"Con base en tu mensaje, el siguiente paso es validar la informacion del pedido o servicio asociado y darte una actualizacion clara. "
            "Mientras tanto, te recomendamos conservar el numero de orden y cualquier evidencia relevante para acelerar la solucion.\n\n"
            "Si lo deseas, podemos continuar con un seguimiento personalizado en este mismo canal."
        )
        return SupportDemoResult(content=reply, lookup_status=lookup_status)

    def _simulate_lookup(self, *, customer_name: str, order_id: str) -> str:
        order_text = order_id or "sin orden proporcionada"
        name_text = customer_name or "cliente sin nombre"
        return f"Consultando base de datos de clientes: cliente={name_text}, orden={order_text}."
