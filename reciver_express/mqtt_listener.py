import paho.mqtt.client as mqtt
import json
import pymysql
import queue
import threading
import time

# Configurações do MQTT
mqtt_server = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_user = ""
mqtt_password = ""
base_topic = "express/#"

# Configuração do MySQL
db_config = {
    "host": "localhost",  # Se rodando no Docker, mudar para "mysql"
    "user": "mysql",
    "password": "senha_mysql",
    "database": "express"
}

# Criar uma fila para armazenar as mensagens MQTT
message_queue = queue.Queue()

# Conectar ao MySQL
def connect_db():
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

# Função para processar as mensagens da fila
def process_messages(worker_id):
    print(f"⚙️ Worker {worker_id} iniciado.")
    while True:
        hardware_id, credit, salescounter, temperature, uptime = message_queue.get()

        try:
            connection = connect_db()
            with connection.cursor() as cursor:
                # Verificar se o dispositivo está autorizado
                cursor.execute("SELECT authorized FROM link_device WHERE hardware_id = %s", (hardware_id,))
                result = cursor.fetchone()

                if not result:
                    print(f"❌ Worker {worker_id}: Dispositivo {hardware_id} não encontrado.")
                    continue

                if not result["authorized"]:
                    print(f"⛔ Worker {worker_id}: Dispositivo {hardware_id} não autorizado.")
                    continue

                # Inserir dados na tabela data_iot
                cursor.execute(""" 
                    INSERT INTO data_iot (hardware_id, credit, salescounter, temperature, uptime)
                    VALUES (%s, %s, %s, %s, %s)
                """, (hardware_id, credit, salescounter, temperature, uptime))

                connection.commit()
                print(f"✅ Worker {worker_id}: Dados do dispositivo {hardware_id} armazenados com sucesso!")

        except Exception as e:
            print(f"⚠️ Worker {worker_id}: Erro ao processar mensagem: {e}")

        finally:
            connection.close()
            message_queue.task_done()

# Callback quando conecta no broker MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao MQTT Broker! Código de retorno: {rc}")
    client.subscribe(base_topic)

# Callback quando recebe uma mensagem MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        hardware_id = payload.get("hardware")
        credit = payload.get("credit")
        salescounter = payload.get("salescounter")
        temperature = payload.get("temperature")
        uptime = payload.get("uptime")  # Adicionado o campo uptime

        if not hardware_id:
            print("⚠️ Hardware ID ausente, ignorando mensagem.")
            return

        # Adicionar à fila somente se o dispositivo estiver autorizado
        check_and_enqueue(payload)

    except json.JSONDecodeError:
        print("⚠️ Erro ao decodificar JSON.")

# Função para adicionar à fila apenas se o dispositivo estiver cadastrado
def check_and_enqueue(payload):
    hardware_id = payload.get("hardware")
    connection = connect_db()

    with connection.cursor() as cursor:
        cursor.execute("SELECT authorized FROM link_device WHERE hardware_id = %s", (hardware_id,))
        result = cursor.fetchone()
        
        if result and result["authorized"]:
            # Incluir o uptime na fila
            message_queue.put((hardware_id, payload["credit"], payload["salescounter"], payload["temperature"], payload["uptime"]))
            print(f"📩 Mensagem do {hardware_id} adicionada à fila.")
        else:
            print(f"⛔ Dispositivo {hardware_id} não autorizado ou não encontrado.")
    
    connection.close()

# Criar múltiplos workers
def start_workers(num_workers):
    for worker_id in range(1, num_workers + 1):
        worker_thread = threading.Thread(target=process_messages, args=(worker_id,), daemon=True)
        worker_thread.start()

# Configurar o cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if mqtt_user:
    client.username_pw_set(mqtt_user, mqtt_password)

# Criar 5 workers para processar as mensagens
start_workers(5)

# Conectar ao MQTT
client.connect(mqtt_server, mqtt_port, 60)
client.loop_forever()
