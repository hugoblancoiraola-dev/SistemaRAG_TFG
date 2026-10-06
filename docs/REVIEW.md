# Revisión de preparación del portfolio

## Alcance

Se leyeron los cinco scripts Python originales y ambos JSON (25 y 6 registros). No se alteran código, modelos, prompts, imports, rutas, datasets ni archivos históricos. Se añaden documentación, dependencias inferidas, reglas de exclusión y un ejemplo ficticio.

## Hallazgos

- Modelo generativo: stablelm2 en Ollama, temperatura 0.
- Embeddings: jinaai/jina-embeddings-v2-base-es.
- Recuperador: k=5; contexto limitado a 500 caracteres del resumen por documento.
- Divisor de texto configurado pero no aplicado.
- Los metadatos guardan autor; el contexto no lo incluye.
- Evaluación implementada: BERTScore con bert-base-multilingual-cased. No hay resultados medidos añadidos ni implementación ROC/AUC en los scripts revisados.
- evaluar_respuestas.py depende de main_prueba.py, que no se encuentra en la ruta consultada.
- El scraper inicializa Selenium, pero no navega a la URL antes de buscar el botón Siguiente; requests vuelve a usar base_url. El límite de seis se comprueba fuera del bucle de enlaces, por lo que puede superarse. Su ejecución sobrescribe tfgs.json.
- Los JSON contienen resúmenes y datos identificativos de trabajos de terceros, con campos de derechos que incluyen restricciones.

## Comprobaciones y límites

Los cinco scripts se comprueban mediante análisis sintáctico y los tres JSON mediante parseo. Se revisan patrones habituales de credenciales en los archivos originales leídos, sin encontrar coincidencias; esto no constituye una auditoría completa de secretos.

No se revisa todo el historial Git ni el contenido binario de chroma_db, cachés o configuración del IDE. No se ejecutan el scraper, Ollama, descargas de modelos ni una instalación completa. Las dependencias no representan las versiones verificadas del entorno original.

Las reglas de .gitignore no retiran archivos ya versionados. Las carpetas históricas y los datos se conservan para evitar borrar material sin comprobar sus dependencias. Antes de publicación quedan pendientes la revisión del historial, los archivos auxiliares y los permisos de redistribución.

No se reorganizan scripts porque sus imports y rutas relativas dependen de la raíz. No se añade LICENSE para no decidir una licencia del código ni extenderla al contenido de terceros.
