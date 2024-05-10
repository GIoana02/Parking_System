#ifndef WiFiManager_h
#define WiFiManager_h

#include <WiFi.h>

class WiFiManager {
public:
    void connect(const char* ssid, const char* password);
    bool isConnected();
};

#endif
