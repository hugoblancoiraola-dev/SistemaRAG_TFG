
from bert_score import BERTScorer

class EvaluadorBERTScore:
    def __init__(self, modelo_bert="bert-base-multilingual-cased"):
        self.scorer = BERTScorer(model_type=modelo_bert, lang="es") 

    def evaluar(self, predicciones, referencias):
        """
        predicciones: lista de respuestas generadas por el modelo
        referencias: lista de respuestas correctas esperadas
        """
        P, R, F1 = self.scorer.score(predicciones, referencias)
        
        print(f"\n--- Resultados BERTScore ---")
        print(f"Precisión (P): {P.mean().item():.4f}")
        print(f"Recall (R): {R.mean().item():.4f}")
        print(f"F1 Score: {F1.mean().item():.4f}")
        
        resultados = {
            "precision": P.mean().item(),
            "recall": R.mean().item(),
            "f1": F1.mean().item()
        }
        return resultados
