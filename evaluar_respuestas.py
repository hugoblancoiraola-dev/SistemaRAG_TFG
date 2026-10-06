# evaluar_modelo.py

from main import ChatPDF
from evaluador import EvaluadorBERTScore
import pandas as pd

# Inicializar modelo
chat = ChatPDF()
chat.ingest("tfgs.json")

# Inicializar evaluador
evaluador = EvaluadorBERTScore()

# Definir preguntas y respuestas esperadas (preguntas variadas sobre distintos metadatos)
preguntas = [
    "¿Qué TFG trata sobre la segmentación de tumores cerebrales mediante modelos de difusión?",
    "¿Quién es el autor del TFG sobre control de una silla de ruedas usando redes neuronales?",
    "¿Qué TFG se centra en el desarrollo de un sistema de análisis de datos geográficos y medioambientales?",
    "¿Cuál es el ODS relacionado con el TFG de Carmen Miralles Martín?",
    "¿Qué asignaturas están relacionadas con el TFG 'Sistema de gestión de un restaurante'?",
    "¿En qué fecha fue defendido el TFG 'Diseño e implementación de una red neuronal para el manejo de una silla de ruedas'?",
    "¿Qué TFG está relacionado con el uso de la plataforma KNIME en el análisis financiero?",
    "¿Quién dirigió el TFG 'Diseño y programación de una aplicación web para la reserva de laboratorios'?",
    "¿Qué palabras clave se asocian al TFG de Che Cui sobre segmentación de tumores?",
    "¿Qué TFG aborda la personalización de modelos para usuarios con movilidad reducida usando Raspberry Pi?"
]

# Respuestas reales correspondientes a las preguntas
respuestas_reales = [
    "Diffusion Model Based Brain Tumour Segmentation Enhanced With Inpainting Method",
    "Díaz Fernández, Sofía",
    "Desarrollo de un sistema para el análisis de datos geográficos y temporales sobre el medioambiente",
    "03. Salud y bienestar, 11. Ciudades y comunidades sostenibles, 13. Acción por el clima",
    "Informática",
    "Marzo 2025",
    "Prototipo de modelo predictivo implementado en KNIME Analytics Platform basado en aprendizaje profundo para la toma de decisiones en el mercado de valores financieros",
    "Bordel Sánchez, Borja",
    "Segmentación de tumor; Imágenes médicas; Supervisión débil; Traducción imagen a imagen; Modelos de difusión; Restauración de imagen; Inpainting; Denoising Diffusion Probabilistic Models (DDPM)",
    "Diseño e implementación de una red neuronal para el manejo de una silla de ruedas"
]

# Obtener predicciones
respuestas_generadas = []

print("Evaluando respuestas...")

for pregunta in preguntas:
    respuesta = chat.ask(pregunta)
    print(f"Pregunta: {pregunta}")
    print(f"Respuesta del modelo: {respuesta}\n")
    respuestas_generadas.append(respuesta)

# Evaluar
resultados = evaluador.evaluar(respuestas_generadas, respuestas_reales)

print("\nEvaluación finalizada.")
