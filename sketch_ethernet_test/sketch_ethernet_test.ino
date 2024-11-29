#include <SPI.h>
#include <Ethernet.h>

// MAC address for your Ethernet Shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// Static IP address for the Arduino (must not conflict with other devices) -  192.168.85.247
IPAddress ip(192, 168, 8, 115); 


// Initialize the Ethernet server (port 80 for HTTP)
EthernetServer server(80);

void setup() {
  
  // Initialize Ethernet with a static IP
  Ethernet.begin(mac, ip);
  server.begin();
  // Start the Serial Monitor for debugging
  Serial.begin(115200); 
}

void loop() {
  // Listen for incoming clients
  EthernetClient client = server.available();
  Serial.println("Client connected1.");
  if (client) {
      Serial.println("Client connected.");
      String html = "<html><head><title>Arduino Web Server</title></head>";
      html += "<body><h1>Hello from Arduino!</h1><p>Click the link below to visit a website:</p></body></html>"; 
      
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: text/html");
      client.println("Connection: close");
      client.println();
      client.println(html);
      
      delay(100);
      client.stop();
      Serial.println("Client disconnected.");
      
    
    
  }
  delay(5000);
}