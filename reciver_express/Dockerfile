# Usar imagem base do Python
FROM python:3.11

# Definir diretório de trabalho
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


# Comando para rodar o script
CMD ["python", "mqtt_listener.py"]
