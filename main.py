import json
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



class ChatPDF:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        
        self.model = ChatOllama(model="stablelm2", temperature=0)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

        self.prompt = PromptTemplate.from_template(
            """
            Eres un asistente experto en búsqueda de información en TFGs.
            Usa el siguiente contexto para responder la pregunta.
            Responde de manera concisa  
            
            Contexto: {context} 

            Pregunta: {question} 

            Si no sabes la respuesta, di que no lo sabes.
            
            Respuesta: 
            """
        )

    def _load_json(self, file_path: str):
        #Convierte los datos JSON en documentos de Langchain
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []
        for i, entry in enumerate(data):
            doc = Document(
                page_content= entry.get('resumen', 'No especificado'),
                metadata={
                    "id": i,
                    "título": entry.get('título', 'No especificado'),
                    "autor": entry.get('autor', 'No especificado'),
                    "director": entry.get('director', 'No especificado'),
                    "grado": entry.get('grado', 'No especificado'),
                    "fecha": entry.get('fecha', 'No especificado'),
                    "asignaturas": entry.get('asignaturas', 'No especificado'),
                    "ods": entry.get('ods', 'No especificado'),
                    "palabras_clave": entry.get('palabras_clave', 'No especificado'),
                    "institución": entry.get('institución', 'No especificado'),
                    "departamento": entry.get('departamento', 'No especificado'),
                    "derechos": entry.get('derechos', 'No especificado'),
                    "PDF_link": entry.get('PDF_link', 'No especificado'),
                }
            )
            documents.append(doc)

        print(f"{len(documents)} documentos generados desde el JSON") 
        return documents    

    def ingest(self, pdf_file_path: str):
        print(f"Cargando datos desde: {pdf_file_path}")
        #Carga documentos PDF y JSON 
        if pdf_file_path.endswith(".pdf"):
            docs = PyPDFLoader(file_path=pdf_file_path).load()
        elif pdf_file_path.endswith(".json"):
            docs = self._load_json(pdf_file_path)
        else:
            raise ValueError("Formato no compatible. Usa PDF o JSON")  
          
        print(f"{len(docs)} documentos cargados antes de dividir.")  

        #Crea el vector store con los datos embebidos
        self.vector_store = Chroma.from_documents(
            documents=docs, 
            embedding=HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-es")
        )
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={
                "k": 5
            },
        )
        print("Datos ingeridos correctamente en Chroma.")

        print(f"{len(docs)} fragmentos generados para indexar en Chroma:")



    def ask(self, query: str):
        if not self.retriever:
            raise ValueError("El sistema no ha sido inicializado con datos. Llama a ingest() primero.")

        
        def format_docs(docs):
            return "\n\n".join([
                f"Título: {d.metadata.get('título', 'No especificado')}\n"
                f"Director: {d.metadata.get('director', 'No especificado')}\n"
                f"Fecha: {d.metadata.get('fecha', 'No especificado')}\n"
                f"Grado: {d.metadata.get('grado', 'No especificado')}\n"
                f"Materias: {d.metadata.get('asignaturas', 'No especificado')}\n"
                f"ODS: {d.metadata.get('ods', 'No especificado')}\n"
                f"Palabras clave: {d.metadata.get('palabras_clave', 'No especificado')}\n"
                f"Institución: {d.metadata.get('institución', 'No especificado')}\n"
                f"Departamento: {d.metadata.get('departamento', 'No especificado')}\n"
                f"Derechos: {d.metadata.get('derechos', 'No especificado')}\n"
                f"Resumen: {d.page_content[:500]}\n"
                for d in docs])

        try:
            chain = (
                {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
                | self.prompt
                | self.model
                | StrOutputParser()
            )
            # Obtener documentos relevantes desde ChromaDB
            return chain.invoke(query)
        except Exception as e:
            print(f"Error de búsqueda: {str(e)}")
            return "Error al procesar tu consulta"

        
