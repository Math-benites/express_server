# Usar imagem base do Python
FROM python:3.11

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos para o container
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir variáveis de ambiente
ENV MQTT_SERVER=mqtt.eclipseprojects.io
ENV MQTT_PORT=1883
ENV MYSQL_HOST=mysql
ENV MYSQL_USER=mysql
ENV MYSQL_PASSWORD=senha_mysql
ENV MYSQL_DB=express

# Comando para rodar o script
CMD ["python", "mqtt_listener.py"]
