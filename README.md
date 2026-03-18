# Proyecto 8: LLM

## Descripcion

Este repositorio implementa los **tres proyectos propuestos** en la actividad de LLM, agrupados por carpetas para que la revision sea clara:

- **Proyecto 1: Asistente de escritura automatica**
- **Proyecto 2: Tutor virtual inteligente**
- **Proyecto 3: Sistema de atencion al cliente automatizado**

La aplicacion esta construida con **Flask** y ofrece una pantalla inicial desde la cual se puede entrar a cada proyecto por separado. La integracion con OpenAI usa la **Responses API** y, para asegurar que el evaluador pueda ejecutar el sistema aun sin credenciales, tambien existe un **modo demo local**.

## Funcionalidades

- Pantalla principal con acceso a los 3 proyectos.
- Integracion con OpenAI usando `responses.create`.
- Modo demo si no existe `OPENAI_API_KEY`.
- Endpoint de salud en `/health`.

### Proyecto 1

- Generar borradores.
- Mejorar estilo.
- Corregir gramatica y puntuacion.
- Resumir contenido.

### Proyecto 2

- Explicar conceptos.
- Responder dudas de estudiantes.
- Generar practica guiada.
- Adaptar la explicacion por nivel academico.

### Proyecto 3

- Responder consultas de soporte.
- Simular consulta interna de clientes y ordenes.
- Ajustar prioridad del caso.
- Generar una respuesta clara y profesional para el cliente.

## Tecnologias

- Python
- Flask
- OpenAI Python SDK
- python-dotenv

## Estructura del proyecto

```text
.
├── app.py
├── webapp.py
├── shared/
│   └── config.py
├── projects/
│   ├── project1_writing_assistant/
│   ├── project2_virtual_tutor/
│   └── project3_customer_support/
├── requirements.txt
├── static/
├── templates/
└── tests/
```

## Instrucciones para ejecutar

### 1. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Opcionalmente, edita `.env`:

- `OPENAI_API_KEY`: tu llave de OpenAI.
- `OPENAI_MODEL`: por defecto `gpt-5-mini`.
- `OPENAI_USE_DEMO`: usa `true` para forzar el modo demo.

Si no defines `OPENAI_API_KEY`, la aplicacion funcionara en modo demo.

### 4. Ejecutar la aplicacion

```bash
python app.py
```

Abre el navegador en:

```text
http://127.0.0.1:5000
```

## Como usar el sistema

1. Entra a `http://127.0.0.1:5000`.
2. Desde la pantalla inicial elige `Proyecto 1`, `Proyecto 2` o `Proyecto 3`.
3. Llena el formulario correspondiente.
4. Presiona el boton principal para generar la respuesta.

La salida aparece en el panel derecho. La interfaz indica si el resultado proviene del modo `openai` o `demo`.

### Uso del Proyecto 1

- Selecciona una tarea de escritura.
- Describe el encargo o pega un texto base.
- Ajusta tono, audiencia y longitud.

### Uso del Proyecto 2

- Selecciona si deseas explicar, responder una duda o generar practica.
- Escribe el tema, el nivel del estudiante y el objetivo de aprendizaje.
- Si corresponde, agrega la duda del estudiante.

### Uso del Proyecto 3

- Selecciona el tipo de consulta y prioridad.
- Captura nombre del cliente, numero de orden y mensaje.
- El sistema simula una consulta interna y genera una respuesta de soporte.

## Pruebas basicas

Con el entorno virtual activo:

```bash
python -m unittest discover -s tests
```

## Notas tecnicas

- La configuracion compartida esta en `shared/config.py`.
- Cada proyecto tiene su propia carpeta con `routes.py`, `service.py` y `demo.py`.
- `webapp.py` registra las rutas principales y conecta los tres proyectos.

## Referencias

- OpenAI Responses API: <https://platform.openai.com/docs/api-reference/responses>
- OpenAI Models: <https://platform.openai.com/docs/models>
