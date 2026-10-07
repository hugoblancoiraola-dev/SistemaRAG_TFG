# Revisión del repositorio y pruebas (2026-10-06)

## Cambios

- El evaluador importa `ChatPDF` de `main`, siguiendo la indicación del autor. No se modifica la implementación de ChatPDF, los prompts, los modelos ni las preguntas de evaluación.
- Se retiran de la versión actual `.idea/`, `__pycache__/` y `chroma_db/`. No se reescribe el historial.
- Se conservan íntegramente `tfgs.json` (25 registros) y `tfgs_pequeño.json` (6 registros). El autor indica que contó con autorización universitaria para usarlos en el RAG.
- Se limitan Transformers a la rama 4 y Sentence Transformers a la rama 3: con las versiones 5.19.0 / 6.1.0, la carga del modelo falla por `attn_implementation="torch"`.
- Se actualiza la documentación para reflejar pruebas y limitaciones.

## Historial

Se enumeraron los nueve commits anteriores a esta limpieza, desde el commit inicial hasta la preparación documental; una sola referencia Git, `main`, sin tags ni ramas adicionales. Se revisaron los árboles completos (sin truncar) y sus 24 blobs únicos. No hay un fuente `main_prueba.py` en ninguno de esos árboles; sí una caché compilada del módulo.

Se examinaron los textos de código, JSON, documentación y configuración, y se buscaron patrones comunes de claves, tokens, contraseñas y claves privadas. No se encontraron coincidencias de credenciales. También se inspeccionaron las cadenas imprimibles de las dos cachés Python y los binarios pequeños. Las cachés contienen una ruta local de Windows (`C:\\Users\\user\\Desktop\\TFG\\...`); siguen disponibles en commits antiguos.

**Límite de la revisión:** la base histórica `chroma.sqlite3` (aproximadamente 11 MB) no pudo descargarse con el conector: su respuesta de contenido base64 está vacía por el tamaño. La revisión de binarios y las búsquedas de patrones no equivalen a una garantía de ausencia de secretos. Los archivos retirados siguen existiendo en el historial.

## Pruebas

Se creó un entorno Python 3.12 aislado y se instalaron las dependencias. Se probó el código original de `main.py`, sin sustituir embeddings ni el generador por simulaciones.

| Comprobación | Resultado |
| --- | --- |
| Sintaxis de los cinco scripts y parseo de los JSON | Correctos |
| Imports de ChatPDF y EvaluadorBERTScore y creación de ChatPDF | Correctos |
| Conversión de JSON a documentos | Correcta: 25, 6 y 1 documentos |
| Consulta sin datos cargados | ValueError esperado |
| Ingesta de los seis TFG originales con Jina y Chroma | Completa, con aviso de pesos del modelo |
| Recuperación | Cinco documentos recuperados |
| Generación con StableLM2 | No validada: modelo no descargable por las restricciones de red |
| BERTScore real | No ejecutado: no se dispone de respuestas generadas para validar la evaluación |

Las primeras versiones instaladas (Transformers 5.19.0 y Sentence Transformers 6.1.0) fallaron al cargar Jina. Con Transformers 4.57.6 y Sentence Transformers 3.4.1, la ingesta y recuperación completaron. Componentes adicionales utilizados: LangChain 0.3.30, Community 0.3.31, Core 0.3.86, Ollama 0.3.10, Hugging Face 0.3.1 y Chroma 1.5.9. Se instaló PyTorch para CPU. El entorno de verificación también requirió socksio por su proxy; no se añade como requisito del proyecto.

## Hallazgos del entorno reconstruido

1. **Carga del modelo Jina:** el cargador actual selecciona BertModel genérico y muestra pesos sin cargar desde el checkpoint. No se debe interpretar una ingesta sin excepción como validación de los embeddings. Queda pendiente configurar y comprobar la arquitectura específica del modelo; no se modifica en esta limpieza.
2. **Generación real:** se instaló Ollama y se comprobó su servidor, pero la descarga de StableLM2 falla al acceder al almacenamiento remoto por las restricciones de red. La consulta devuelve el mensaje de error previsto cuando Ollama no está accesible desde la prueba. No se atribuye este fallo de conexión al algoritmo RAG.
3. **Evaluación:** ejecutar las diez preguntas con Ollama disponible y después BERTScore.
4. **Limitaciones previas:** el divisor de texto está configurado pero no se aplica; el autor no se incluye en el contexto del prompt; el scraper puede repetir páginas y superar el límite de seis y sobrescribe tfgs.json.

## Decisión de conservación (2026-10-07)

El autor confirma que probó el sistema hasta la entrega del TFG y que funcionaba en el entorno original. Decide conservar la implementación académica y autoriza publicar el repositorio. Los hallazgos anteriores pertenecen al entorno reconstruido de verificación; no permiten afirmar que el entorno de entrega tuviera los mismos avisos. La memoria aún no se ha consultado para recuperar preguntas, respuestas o resultados originales.

Se mantienen estructura, rutas y modelos originales. El único ajuste funcional realizado en esta preparación es el import del evaluador a main.ChatPDF, autorizado por el autor. No se añade licencia en esta fase.
