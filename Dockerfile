# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de requisitos (se necessário) e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do aplicativo para o contêiner
COPY mqtt_to_sql.py mqtt_to_sql.py

# Comando para executar o script
CMD ["python", "mqtt_to_sql.py"]
