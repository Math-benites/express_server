# Usar imagem base do Python
FROM python:3.11

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_listener.py ./

# Comando para rodar o script
CMD ["python", "mqtt_listener.py"]
