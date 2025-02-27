from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import pymysql
from db_config import db_config
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


# Função para conectar ao banco de dados
def connect_db():
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

# Página de cadastro de cliente
@app.route('/', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        # Dados do cliente
        client_name = request.form['client_name']
        client_email = request.form['client_email']
        client_phone = request.form['client_phone']

        try:
            connection = connect_db()
            with connection.cursor() as cursor:
                # Verificar se o e-mail já está cadastrado
                cursor.execute("SELECT * FROM data_clients WHERE email = %s", (client_email,))
                existing_client = cursor.fetchone()

                if existing_client:
                    message = f"Cliente com e-mail {client_email} já cadastrado."
                else:
                    # Inserir cliente
                    cursor.execute("INSERT INTO data_clients (name, email, phone) VALUES (%s, %s, %s)",
                                   (client_name, client_email, client_phone))
                    connection.commit()
                    message = f"Cliente {client_name} cadastrado com sucesso!"

            connection.close()
            return render_template('cadastro_cliente.html', message=message)
        except Exception as e:
            return f"Erro ao cadastrar cliente: {e}"

    return render_template('cadastro_cliente.html')

@app.route('/excluir_dispositivo/<int:client_id>/<string:hardware_id>', methods=['POST'])
def excluir_dispositivo(client_id, hardware_id):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            # Excluir o dispositivo da tabela de link_device
            cursor.execute("DELETE FROM link_device WHERE client_id = %s AND hardware_id = %s", (client_id, hardware_id))
            connection.commit()

        connection.close()
        flash("Dispositivo excluído com sucesso.", "success")
        return redirect(url_for('editar_cliente', client_id=client_id))  # Redireciona para a tela de edição do cliente
    except Exception as e:
        flash(f"Erro ao excluir dispositivo: {e}", "error")
        return redirect(url_for('editar_cliente', client_id=client_id))


# Página de listagem de clientes
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM data_clients")
            clientes = cursor.fetchall()
        connection.close()
        return render_template('listar_clientes.html', clientes=clientes)
    except Exception as e:
        return f"Erro ao buscar clientes: {e}"

@app.route('/editar_cliente/<int:client_id>', methods=['GET', 'POST'])
def editar_cliente(client_id):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            # Buscar dados do cliente para edição
            cursor.execute("SELECT * FROM data_clients WHERE id = %s", (client_id,))
            cliente = cursor.fetchone()

            # Buscar dispositivos IoT associados a este cliente
            cursor.execute("SELECT * FROM link_device WHERE client_id = %s", (client_id,))
            linked_devices = cursor.fetchall()

            if request.method == 'POST':
                # Se o formulário de edição do cliente for enviado
                if 'client_name' in request.form:
                    client_name = request.form['client_name']
                    client_email = request.form['client_email']
                    client_phone = request.form['client_phone']
                    cpf_cnpj = request.form['cpf_cnpj']
                    address = request.form['address']
                    company_name = request.form['company_name']

                    # Atualizar dados do cliente no banco de dados
                    cursor.execute("""
                        UPDATE data_clients 
                        SET name = %s, email = %s, phone = %s, cpf_cnpj = %s, address = %s, company_name = %s
                        WHERE id = %s
                    """, (client_name, client_email, client_phone, cpf_cnpj, address, company_name, client_id))
                    connection.commit()

                if 'add_device' in request.form:
                    new_device_id = request.form['new_device_id']
                    authorized = request.form['authorized']

                    print(f"Novo dispositivo ID: {new_device_id}")
                    print(f"Autorizado: {authorized}")

    # Inserir dispositivo diretamente na tabela link_device
                    cursor.execute("""
                    INSERT INTO link_device (client_id, hardware_id, authorized) 
                        VALUES (%s, %s, %s)
                    """, (client_id, new_device_id, authorized))
                    connection.commit()

                flash("Cliente atualizado com sucesso!", "success")
                return redirect(url_for('editar_cliente', client_id=client_id))  # Redireciona para edição do cliente

        connection.close()
        return render_template('editar_cliente.html', cliente=cliente, linked_devices=linked_devices)
    except Exception as e:
        flash(f"Erro ao editar cliente: {e}", "error")
        return redirect(url_for('editar_cliente', client_id=client_id))


@app.route('/alternar_autorizacao/<int:client_id>/<int:device_id>', methods=['GET'])
def alternar_autorizacao(client_id, device_id):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            # Verificar se o dispositivo existe
            cursor.execute("SELECT * FROM link_device WHERE client_id = %s AND hardware_id = %s", (client_id, device_id))
            device = cursor.fetchone()
            
            if device:
                # Alternar o estado de 'authorized'
                new_authorized = 1 if device['authorized'] == 0 else 0
                cursor.execute("UPDATE link_device SET authorized = %s WHERE client_id = %s AND hardware_id = %s",
                               (new_authorized, client_id, device_id))
                connection.commit()
                flash("Status de autorização atualizado com sucesso.", "success")
            else:
                flash("Dispositivo não encontrado para este cliente.", "error")
            
        connection.close()
        return redirect(url_for('editar_cliente', client_id=client_id))
    except Exception as e:
        flash(f"Erro ao alternar autorização: {e}", "error")
        return redirect(url_for('editar_cliente', client_id=client_id))

# Página de confirmação de exclusão
@app.route('/confirmar_exclusao/<int:client_id>', methods=['GET'])
def confirmar_exclusao(client_id):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM data_clients WHERE id = %s", (client_id,))
            cliente = cursor.fetchone()
        connection.close()
        if cliente:
            return render_template('confirmar_exclusao.html', cliente=cliente)
        else:
            return "Cliente não encontrado!"
    except Exception as e:
        return f"Erro ao buscar cliente para exclusão: {e}"

# Função para excluir o cliente
@app.route('/excluir_cliente/<int:client_id>', methods=['POST'])
def excluir_cliente(client_id):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM data_clients WHERE id = %s", (client_id,))
            connection.commit()
        connection.close()
        return redirect(url_for('listar_clientes'))  # Redireciona para a listagem de clientes
    except Exception as e:
        return f"Erro ao excluir cliente: {e}"

@app.route('/iot_status')
def iot_status():
    try:
        connection = connect_db()
        with connection.cursor(dictionary=True) as cursor:
            # Buscar todos os dispositivos IoT e suas últimas atualizações
            cursor.execute("SELECT id, hardware_id, timestamp FROM data_iot")
            devices = cursor.fetchall()
        
        connection.close()
        
        # Pegando o tempo do servidor para comparação
        server_time = datetime.now()

        return render_template('iot_status.html', devices=devices, server_time=server_time)
    
    except Exception as e:
        return f"Erro ao carregar status dos dispositivos: {e}"

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
