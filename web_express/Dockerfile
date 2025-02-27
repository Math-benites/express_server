# Usando a imagem oficial do Python
FROM python:3.9

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do Flask para dentro do container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do app Flask para dentro do container
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Comando para rodar o app Flask
CMD ["python", "app.py"]
