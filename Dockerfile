FROM public.ecr.aws/lambda/python:3.11

# Crée le répertoire de travail
WORKDIR /var/task

# Copier les fichiers
COPY src/ src/
COPY config/ config/
COPY api/lambda_function.py api/lambda_function.py
COPY requirements.txt .

# Installer les dépendances dans le bon dossier
RUN pip install --upgrade pip \
    && pip install "numpy<2.0.0" -t . \
    && pip install faiss-cpu==1.7.4 -t . \
    && pip install pydantic pydantic-core -t . \
    && pip install -r requirements.txt -t . --prefer-binary --only-binary=:all:

RUN pip check

# Définir le handler
CMD ["api.lambda_function.lambda_handler"]
