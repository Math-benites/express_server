import json
import mysql.connector
from mysql.connector import Error
from paho.mqtt import client as mqtt_client

# Configurações do MQTT
mqtt_server = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_user = ""
mqtt_password = ""
base_topic = "express/#"

# Configurações do MySQL
db_config = {
    "host": "localhost",  # Nome do serviço no Docker Compose
    "user": "mysql",
    "password": "senha_mysql",
    "database": "iot_data"
}

# Função para salvar os dados no banco MySQL
def save_data(iot_id, data):
    try:
        # Conexão com o banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o dispositivo IoT está cadastrado na tabela iot_devices
        cursor.execute("SELECT id FROM iot_devices WHERE iot_id = %s", (iot_id,))
        device = cursor.fetchone()

        if not device:
            print(f"Dispositivo IoT não encontrado: {iot_id}. Certifique-se de que ele está cadastrado.")
            return

        # Extrai o ID do dispositivo
        device_id = device[0]

        # Insere os dados de monitoramento na tabela iot_data
        print(f"Inserindo dados de monitoramento no banco para o dispositivo {iot_id}: {data}")
        cursor.execute('''
            INSERT INTO iot_data (iot_id, credit, salescounter) 
            VALUES (%s, %s, %s)
        ''', (iot_id, data.get("credit", 0), data.get("salescounter", 0)))
        
        # Confirma a transação
        conn.commit()

        print(f"Dados de monitoramento salvos com sucesso no MySQL para o dispositivo {iot_id}: {data}")

    except Error as e:
        # Tratamento de erros no MySQL
        print(f"Erro ao salvar no banco de dados: {e}")
    
    finally:
        # Garante que a conexão com o banco será fechada
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Função para processar mensagens MQTT
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Recebido tópico: {topic}, mensagem: {payload}")

        # Extrai o ID do IoT do tópico
        iot_id = topic.split("/")[1]

        # Converte o payload para JSON
        data = json.loads(payload)

        # Salva os dados no banco MySQL
        save_data(iot_id, data)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Função para conectar ao MQTT
def connect_mqtt():
    client = mqtt_client.Client()
    client.username_pw_set(mqtt_user, mqtt_password)
    client.on_connect = lambda c, u, f, rc: print("Conectado ao MQTT!") if rc == 0 else print("Falha ao conectar.")
    client.on_message = on_message

    try:
        client.connect(mqtt_server, mqtt_port)
        return client
    except Exception as e:
        print(f"Erro ao conectar ao MQTT: {e}")
        return None

# Função principal
def main():
    # Conecta ao MQTT
    client = connect_mqtt()
    if not client:
        return

    # Assina o tópico base
    client.subscribe(base_topic)
    print(f"Assinado no tópico: {base_topic}")

    # Inicia o loop para processar mensagens
    client.loop_forever()

if __name__ == "__main__":
    main()
