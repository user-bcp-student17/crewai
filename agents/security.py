"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "Revisa la funcionalidad, sus criterios de aceptación y el contexto disponible "
    "de las etapas anteriores. Identifica las fronteras de confianza y comprueba "
    "autenticación, autorización y acceso a recursos de otra persona, validación "
    "de entradas, inyección, secretos y exposición de datos sensibles. "
    "Para cada hallazgo indica archivo y ubicación, evidencia, impacto y una "
    "corrección concreta. Propón una comprobación reproducible de cada corrección. "
    "Distingue los riesgos detectados, las correcciones propuestas y las "
    "verificaciones realmente ejecutadas; marca como pendiente lo que no puedas "
    "comprobar y no inventes archivos, pruebas ni resultados. Si faltan datos, "
    "expón los supuestos y la evidencia necesaria. Atiende el feedback recibido "
    "y entrega los resultados en un informe de seguridad."
)
agent = Agent(role='Revisor de seguridad',
              goal="Identificar riesgos de seguridad y proponer correcciones verificables para la funcionalidad.",
              backstory="Eres un revisor de seguridad que analiza las fronteras de confianza y los permisos de cada usuario. Basas tus conclusiones en evidencia y comunicas las limitaciones de la revisión.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad.', agent=agent)
