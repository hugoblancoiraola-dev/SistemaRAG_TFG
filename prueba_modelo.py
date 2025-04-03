from main import ChatPDF

chat = ChatPDF()
#chat.ingest("tfgs.json")  #Probar el modelo con 25 tfgs scrappeados
chat.ingest("tfgs_pequeño.json")  #Probar el modelo solo con 6 tfgs scrappeados

# PREGUNTAS PARA EL MODELO

#print(chat.ask("Dime un TFG cuyo autor sea Daniel Peña Porras"))
#print(chat.ask("Dime un TFG cuyo autor sea Peña Porras, Daniel"))
print(chat.ask("Dime el título del TFG cuyo autor sea Díaz Fernández, Sofía"))
print(chat.ask("Dime el título del TFG cuyo autor sea Díaz Fernández, Sofía"))
#print(chat.ask("¿Qué TFG escribió Daniel Peña?"))
#print(chat.ask("¿De qué trata el TFG de Daniel Peña Porras?"))
#print(chat.ask("Dime los TFGs relacionados con la ODS número 8. Trabajo decente y crecimiento económico"))
#print(chat.ask("¿Podrías hacerme una lista con los títulos de los tfg que tienes de contexto para responder?"))