# Usa a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos da aplicação para o container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Define o comando para rodar a aplicação
CMD ["python", "app.py"]
