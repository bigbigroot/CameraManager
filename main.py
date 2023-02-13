from paho.mqtt import client

mqtt_conn = client.Client()


def client_conncet(client, userdata, flags, rc):
    mqtt_conn.subscribe('networking/manager')


def recv_message(client, userdata, msg):
    print(msg.payload.decode())
    mqtt_conn.publish('networking/app', 'data'.encode())


def main():
    mqtt_conn.connect('192.168.5.6', 1883)
    mqtt_conn.username_pw_set('test', 'test')
    mqtt_conn.on_connect = client_conncet
    mqtt_conn.on_message = recv_message
    mqtt_conn.loop_forever()

if __name__ == '__main__':
    main()
