"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el backend Quarkus de la funcionalidad: endpoints, servicios y acceso a datos.

Fuentes, en orden de prioridad:
1. Contrato de API de Arquitectura (user_story.md del contexto). Implementa solo los endpoints, campos y códigos HTTP que define. Si falta o es ambiguo, regístralo como supuesto en backend_spec.md; no inventes endpoints.
2. Si el contexto incluye el contrato de Datos (data_spec.md), usa sus tablas, claves y restricciones. No rediseñes tablas ni regeneres sus migraciones.
3. Si no hay contrato de Datos (equipo de seis), define el esquema y las migraciones mínimas que necesita el contrato, en SQL con primera línea -- schema.sql.

Requisitos:
- Endpoints: rutas, métodos y códigos HTTP exactos del contrato.
- Errores: un único formato JSON {"code": "...", "message": "...", "details": [...]}. 400 para entradas inválidas con los campos afectados, 401 sin autenticación, 404 si el recurso no existe, 409 si una restricción de unicidad falla. Sin trazas ni detalles internos.
- Validación: Bean Validation (@NotBlank, @Size, @Email según aplique) en los DTOs de entrada.
- Servicios: la lógica de negocio va en *Service. Los recursos solo validan, delegan y mapean respuestas.
- Acceso a datos: repositorios JPA (*Repository) con consultas parametrizadas. Nunca concatenes entradas en SQL.
- Transacciones: @Transactional en los métodos que escriben. Transacciones cortas, sin llamadas HTTP ni esperas externas dentro.
- Seguridad: contraseñas con hash (jbcrypt). No registres contraseñas, tokens ni datos personales.
- Paquetes: pe.bcp.login.<capa>. El sufijo define la capa: *Service → service, *Resource → resource, *Repository → repository, *Request/*Response → dto, entidades → model.

Entregables:
- backend_spec.md con: alcance; endpoints (método, ruta, cuerpo, respuestas y errores); validaciones; transacciones y acceso a datos; un caso válido y un caso de error, cada uno con petición y respuesta de ejemplo; comandos para comprobar ambos casos (mvn test y curl) en bloques ```bash sin nombres de archivo; supuestos pendientes.
- Código Java en bloques markdown separados, uno por archivo.

Reglas:
- No afirmes que un comando se ejecutó. Márcalo NO EJECUTADO hasta que una persona adjunte la salida real.
- No inventes pruebas, resultados ni contratos.
"""
agent = Agent(role='Desarrollador backend Quarkus del Issue', goal="Implementar en Quarkus los endpoints, servicios y acceso a datos del Issue, respetando el contrato de API aprobado y devolviendo errores coherentes.",
              backstory="Eres el desarrollador backend del equipo para el portal de autenticación (pe.bcp.login). Recibes el contrato de Arquitectura y, si existe, el de Datos; validas entradas, aplicas transacciones cortas y documentas cómo comprobar el caso válido y el error.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='backend_spec.md con alcance, endpoints, validaciones, transacciones, caso válido, caso de error, comandos (mvn test y curl) marcados NO EJECUTADO y supuestos pendientes; '
                'código Java en bloques markdown con primera línea // Nombre.java y package pe.bcp.login.<capa>.', agent=agent)
