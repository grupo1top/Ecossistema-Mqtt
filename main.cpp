#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// ================= WIFI =================
const char* ssid = "iot";
const char* password = "iotsenai502";

// ================= MQTT =================
const char* mqtt_server = "192.168.0.72";

// usuário e senha MQTT
const char* mqtt_user = "grupo1";
const char* mqtt_password = "grupo1";

WiFiClient espClient;
PubSubClient client(espClient);

// ================= LED =================
#define PIN_LED 13

bool piscando = false;

// ========================================
// FUNÇÕES DO LED
// ========================================

void Ligar_led() {
  digitalWrite(PIN_LED, HIGH);
  piscando = false;

  Serial.println("LED LIGADO");
}

void Desligar_led() {
  digitalWrite(PIN_LED, LOW);
  piscando = false;

  Serial.println("LED DESLIGADO");
}

void Piscar_led() {
  piscando = true;

  Serial.println("LED PISCANDO");
}

// ========================================
// CALLBACK MQTT
// ========================================

void callback(char* topic, byte* payload, unsigned int length) {

  String mensagem;

  for (int i = 0; i < length; i++) {
    mensagem += (char)payload[i];
  }

  Serial.print("Mensagem recebida: ");
  Serial.println(mensagem);

  if (mensagem == "ON") {
    Ligar_led();
  }

  else if (mensagem == "OFF") {
    Desligar_led();
  }

  else if (mensagem == "BLINK") {
    Piscar_led();
  }
}

// ========================================
// CONEXÃO WIFI
// ========================================

void setup_wifi() {

  delay(10);

  Serial.println();
  Serial.print("Conectando ao WiFi ");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println(WiFi.localIP());
}

// ========================================
// RECONEXÃO MQTT
// ========================================

void reconnect() {

  while (!client.connected()) {

    Serial.print("Tentando conexão MQTT...");

    // conexão COM usuário e senha
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {

      Serial.println("conectado");

      client.subscribe("esp32/led");

    } else {

      Serial.print("falhou, rc=");
      Serial.print(client.state());

      Serial.println(" tentando novamente em 5 segundos");

      delay(5000);
    }
  }
}

// ========================================
// SETUP
// ========================================

void setup() {

  Serial.begin(115200);

  pinMode(PIN_LED, OUTPUT);

  setup_wifi();

  client.setServer(mqtt_server, 1883);

  client.setCallback(callback);
}

// ========================================
// LOOP
// ========================================

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  if (piscando) {

    digitalWrite(PIN_LED, HIGH);
    delay(500);

    digitalWrite(PIN_LED, LOW);
    delay(500);
  }
}