# Sistema RAG para consulta de TFGs

Proyecto de Trabajo Fin de Grado de **Hugo Blanco Iraola**, desarrollado en Ingeniería del Software (ETSISI, UPM). **Calificación del TFG: 10/10.**

Prototipo de Retrieval-Augmented Generation (RAG) para consultar trabajos académicos mediante lenguaje natural. Combina adquisición de metadatos, recuperación semántica y generación con un modelo local.

## Qué demuestra

- Integración de un flujo de datos académicos con LangChain y Chroma.
- Recuperación semántica con embeddings en español.
- Generación local con Ollama, sin una API de generación comercial.
- Evaluación de respuestas mediante BERTScore.

## Arquitectura implementada

```mermaid
flowchart TD
    A["JSON: resúmenes y metadatos / PDF"] --> B["Documentos LangChain"]
    B --> C["Embeddings Jina en español"]
    C --> D["Chroma: recuperación de 5 documentos"]
    D --> E["Prompt con contexto"]
    E --> F["StableLM2 mediante Ollama"]
    F --> G["Respuesta"]
    G --> H["BERTScore frente a referencias"]
```

`ChatPDF.ingest()` admite JSON y PDF. Para JSON indexa el resumen y conserva los metadatos. `ask()` recupera cinco documentos y construye un contexto con metadatos y los primeros 500 caracteres de cada resumen.

El código configura un divisor de texto (1024 caracteres, solapamiento 100), pero **no lo aplica en la ingesta actual**. Chroma se crea sin una ruta de persistencia explícita; la carpeta histórica `chroma_db/` no se carga en este flujo.

## Archivos

| Archivo | Función |
| --- | --- |
| `main.py` | Clase `ChatPDF`: ingesta, recuperación y generación |
| `prueba_modelo.py` | Prueba manual con el JSON de seis TFGs |
| `scrapping_prueba.py` | Extracción de metadatos del repositorio UPM; escribe `tfgs.json` |
| `evaluador.py` | BERTScore: precisión, recall y F1 medios |
| `evaluar_respuestas.py` | Preguntas y referencias para evaluar respuestas |
| `tfgs.json` | Conjunto original de 25 registros |
| `tfgs_pequeño.json` | Conjunto original de seis registros |
| `data/sample_tfgs.json` | Ejemplo ficticio con el mismo esquema |
| `requirements.txt` | Dependencias directas deducidas de los imports |
| `docs/REVIEW.md` | Limitaciones y revisión de esta edición |

Se mantienen los archivos originales en la raíz para preservar imports y rutas relativas.

## Puesta en marcha

Necesitas Python, Ollama y acceso inicial para descargar los modelos. Chrome es necesario únicamente para el scraper.

Desde la raíz del repositorio:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

python -m pip install -r requirements.txt
ollama pull stablelm2
```

Ollama debe estar en ejecución. Los embeddings usados son `jinaai/jina-embeddings-v2-base-es`; BERTScore utiliza `bert-base-multilingual-cased`.

**Las dependencias se han reconstruido a partir del código, no del entorno original. No son un lockfile ni una instalación validada.** La restricción de LangChain mantiene los imports anteriores a su versión 1.

### Consulta con datos ficticios

```python
from main import ChatPDF

chat = ChatPDF()
chat.ingest("data/sample_tfgs.json")
print(chat.ask("¿Qué trabajo trata sobre recuperación semántica?"))
```

### Prueba original

```bash
python prueba_modelo.py
```

Ejecutarla desde la raíz conserva la resolución de `tfgs_pequeño.json`.

## Evaluación y limitaciones

`EvaluadorBERTScore` devuelve precisión, recall y F1 de similitud semántica; **no son métricas de clasificación ni una garantía de exactitud factual**. Esta edición no añade resultados numéricos ni afirma que exista una evaluación ROC/AUC en estos scripts.

`evaluar_respuestas.py` importa `main_prueba.ChatPDF`, pero ese módulo no está disponible en la ruta consultada. El script no puede ejecutarse tal como está. Se conserva para no sustituir una posible variante experimental por otra sin conocerla.

El autor se guarda en los metadatos, pero no se incorpora al contexto del prompt actual. Las consultas por autor de la prueba manual pueden verse afectadas. El scraper también tiene limitaciones de paginación y control del número de registros; véase la revisión.

## Datos y publicación

Los JSON originales incluyen nombres, resúmenes, enlaces y campos de derechos de trabajos de terceros procedentes de UPM. El ejemplo de `data/` es ficticio y no contiene textos de esos trabajos.

La presencia de datos en un repositorio académico de acceso abierto no implica que todos puedan redistribuirse bajo una misma licencia. No se añade una licencia que abarque contenido de terceros. El repositorio permanece privado.

`.gitignore` evita futuras incorporaciones de cachés, configuración del IDE, bases vectoriales y secretos habituales. **No elimina archivos ya versionados ni los borra del historial.**

## Autor

[Hugo Blanco Iraola](https://github.com/hugoblancoiraola-dev) · [Portfolio del máster en IA aplicada](https://github.com/hugoblancoiraola-dev/Applied_AI_Master_Portfolio)
