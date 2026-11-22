import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileIngestor:
    def __init__(self, repo_path="data"):
        self.repo_path = repo_path
        # Extensions we care about (add .js, .java, etc. if needed)
        self.allowed_extensions = {'.py', '.md', '.txt', '.js', '.ts'}
        # Folders to ignore
        self.ignore_dirs = {'.git', '__pycache__', 'venv', 'node_modules'}

    def load_repo(self):
        """
        Walks through the directory structure and yields file contents.
        Returns a list of dicts: [{'path': 'src/main.py', 'content': '...'}]
        """
        documents = []
        
        for root, dirs, files in os.walk(self.repo_path):
            # Modify dirs in-place to skip ignored folders
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.allowed_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Store relative path (e.g., "src/main.py") not full path
                            rel_path = os.path.relpath(file_path, self.repo_path)
                            documents.append({"path": rel_path, "content": content})
                    except Exception as e:
                        logger.warning(f"Could not read {file_path}: {e}")
        
        logger.info(f"Loaded {len(documents)} files from {self.repo_path}")
        return documents

    def chunk_code(self, text, chunk_size=2000, overlap=200):
        """
        Code needs larger chunks than text to keep context (functions together).
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + chunk_size
            if end >= text_len:
                chunks.append(text[start:])
                break
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
            
        return chunks