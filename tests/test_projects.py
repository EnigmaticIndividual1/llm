import unittest

from app import app
from projects.project1_writing_assistant.demo import DemoWritingAssistant
from projects.project2_virtual_tutor.demo import DemoVirtualTutor
from projects.project3_customer_support.demo import DemoCustomerSupport


class ProjectRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_home_and_projects_are_available(self) -> None:
        for route in ["/", "/proyecto-1/", "/proyecto-2/", "/proyecto-3/", "/health"]:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)


class DemoLogicTests(unittest.TestCase):
    def test_project1_demo_generates_text(self) -> None:
        result = DemoWritingAssistant().respond(
            task="generate",
            brief="un correo para pedir una reunion",
            source_text="",
            tone="professional",
            audience="un cliente",
            target_length="media",
        )
        self.assertIn("borrador", result.content.lower())

    def test_project2_demo_returns_guided_practice(self) -> None:
        result = DemoVirtualTutor().respond(
            task="practice",
            topic="fotosintesis",
            question="",
            level="secundaria",
            learning_goal="preparar un examen",
        )
        self.assertIn("Practica guiada", result.content)

    def test_project3_demo_simulates_lookup(self) -> None:
        result = DemoCustomerSupport().respond(
            issue_type="pedido",
            customer_name="Ana",
            order_id="ORD-10",
            customer_message="Mi pedido no llega",
            priority="alta",
        )
        self.assertIn("Consultando base de datos", result.lookup_status)


if __name__ == "__main__":
    unittest.main()
