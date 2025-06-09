FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour LlamaIndex et ChromaDB
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de configuration
COPY pyproject.toml requirements.txt ./
COPY odoo_config.json.example ./

# Installer les dépendances Python (séparément pour optimiser le cache Docker)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
COPY run_server.py ./
COPY test_indexing.py ./

# Installer le package en mode développement
RUN pip install --no-cache-dir -e .

# Créer le répertoire pour ChromaDB
RUN mkdir -p /app/chroma_db

# Exposer le port (si nécessaire pour HTTP)
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONPATH=/app/src
ENV ODOO_URL=https://your-odoo-instance.com
ENV ODOO_DB=your-database-name
ENV ODOO_USERNAME=your-username
ENV ODOO_PASSWORD=your-password

# Variables d'environnement pour l'indexation LlamaIndex (optionnelles)
ENV OPENAI_API_KEY=""
ENV CHROMA_DB_PATH="/app/chroma_db"

# Commande par défaut pour lancer le serveur MCP
CMD ["python", "run_server.py"] 