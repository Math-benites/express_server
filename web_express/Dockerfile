# Usa uma imagem base com Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para o contêiner
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000
EXPOSE 5000

# Comando de execução
CMD ["gunicorn", "-w", "4", "-t", "120", "--threads", "4", "-b", "0.0.0.0:5000", "app:app"]
