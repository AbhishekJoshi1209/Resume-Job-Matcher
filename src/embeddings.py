import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        Using sentence-transformers for fast, efficient embeddings
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()  # Set to evaluation mode
        
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Use mean pooling (average of token embeddings)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()[0]
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            emb = self.generate_embedding(text)
            embeddings.append(emb)
        return np.array(embeddings)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        sample_text = "sample"
        return len(self.generate_embedding(sample_text))


# Example usage
if __name__ == "__main__":
    generator = EmbeddingGenerator()
    
    text1 = "Python developer with 5 years experience"
    text2 = "Senior Python programmer"
    
    emb1 = generator.generate_embedding(text1)
    emb2 = generator.generate_embedding(text2)
    
    print(f"Embedding dimension: {len(emb1)}")
    print(f"Embeddings generated successfully!")