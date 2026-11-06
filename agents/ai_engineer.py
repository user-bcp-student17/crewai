"""Agente responsable de implementar backend y frontend de forma integrada."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'ai-engineer'
LABEL = 'AI Engineer'
SPEC_FILE = 'ai_engineer_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Implementa de forma coherente el backend Quarkus y el frontend Angular "
    "según el requerimiento y los contratos aprobados. Incluye servicios, "
    "endpoints, validaciones, persistencia e interacción con la API. "
    "Considera estados de carga, vacío y error, accesibilidad y validación en el servidor. "
    "No afirmes haber ejecutado pruebas sin evidencia."
)
agent = Agent(role=LABEL, goal="Implementar la solución integrada de backend y frontend.",
              backstory="Eres el AI Engineer responsable de la implementación del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Implementación integrada y código en bloques markdown: Java con primera línea '
                '// Nombre.java y el package correspondiente; TypeScript con // nombre.ts; '
                'HTML con <!-- nombre.html --> y CSS con /* nombre.css */. '
                'Indica supuestos y pruebas propuestas sin inventar resultados.', agent=agent)
