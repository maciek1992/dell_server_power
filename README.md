# **Dell Server Power Monitor (Proxmox & Home Assistant via HACS)**

This is a **custom Home Assistant integration** designed for monitoring **Dell R620 (or similar) server's power consumption** using **iDRAC, Proxmox, and MQTT**. The integration is compatible with **HACS (Home Assistant Community Store)** and supports full configuration via UI.

---

## **📌 Features**
✅ **Reads power consumption (Watts) from Dell iDRAC**  
✅ **Sends real-time data to Home Assistant via MQTT**  
✅ **Fully compatible with HACS**  
✅ **Supports MQTT authentication (username & password)**  
✅ **Works directly from Proxmox**  
✅ **Auto-starts on Proxmox reboot**  
✅ **Can calculate cost based on kWh price**  

---

## **📁 Directory Structure**
```
dell_server_power/
├── custom_components/
│   ├── dell_server_power/
│   │   ├── __init__.py
│   │   ├── manifest.json
│   │   ├── const.py
│   │   ├── sensor.py
│   │   ├── config_flow.py
│   │   ├── translations/
│   │   │   ├── en.json
│   │   │   ├── pl.json
│   │   ├── hacs.json
│   │   ├── services.yaml
```

---

## **📥 Installation via HACS**

### **1️⃣ Add Custom Repository in HACS**
1. Open Home Assistant UI.
2. Go to `HACS → Integrations → Add Repository`.
3. Enter the repository URL:
   ```
   https://github.com/maciek1992/dell_server_power
   ```
4. Choose **"Integration"** type and click **Add**.
5. Install the integration from HACS.

### **2️⃣ Restart Home Assistant**
```sh
ha core restart
```

### **3️⃣ Configure the Integration**
1. Go to `Settings → Integrations → Add Integration`.
2. Search for **"Dell Server Power Monitor"**.
3. Enter:
   - **iDRAC IP Address**
   - **iDRAC Username & Password**
   - **MQTT Broker Address (Proxmox IP or External Broker)**
   - **MQTT Port (default: 1883)**
   - **MQTT Username & Password (optional)**

---

## **⚙️ Proxmox Configuration**
### **1️⃣ Install Required Packages**
```sh
apt update
apt install -y mosquitto mosquitto-clients python3-requests python3-paho-mqtt
```

### **2️⃣ Create MQTT Power Monitoring Script**
1. Create the script:
   ```sh
   nano /root/send_power_to_mqtt.sh
   ```
2. Paste the following:
   ```bash
   #!/bin/bash
   MQTT_HOST="YOUR_MQTT_IP"
   MQTT_TOPIC="homeassistant/sensor/dell_r620_power"
   MQTT_USER="mqtt_user"
   MQTT_PASS="mqtt_password"
   
   while true; do
       POWER=$(racadm get system.ServerPwr.Watts | grep "System.ServerPwr.Watts" | awk -F= '{print $2}')
       if [[ -n "$POWER" ]]; then
           mosquitto_pub -h "$MQTT_HOST" -u "$MQTT_USER" -P "$MQTT_PASS" -t "$MQTT_TOPIC" -m "$POWER"
           echo "Sent power data: $POWER W"
       else
           echo "Error fetching power data"
       fi
       sleep 30
   done
   ```
3. Save and exit (`CTRL+X`, `Y`, `Enter`).
4. Make it executable:
   ```sh
   chmod +x /root/send_power_to_mqtt.sh
   ```

---

## **🔄 Auto-start the Script on Proxmox Reboot**
### **1️⃣ Create a Systemd Service**
1. Create a new service file:
   ```sh
   nano /etc/systemd/system/dell_power_monitor.service
   ```
2. Add the following:
   ```ini
   [Unit]
   Description=Dell Server Power Monitor via MQTT
   After=network.target

   [Service]
   ExecStart=/root/send_power_to_mqtt.sh
   Restart=always
   User=root
   WorkingDirectory=/root

   [Install]
   WantedBy=multi-user.target
   ```
3. Save and exit (`CTRL+X`, `Y`, `Enter`).
4. Enable and start the service:
   ```sh
   systemctl daemon-reload
   systemctl enable dell_power_monitor.service
   systemctl start dell_power_monitor.service
   ```
5. Verify it's running:
   ```sh
   systemctl status dell_power_monitor.service
   ```

---

## **📜 Verifying MQTT Data**
1️⃣ **Check if Proxmox is sending power data**
```sh
mosquitto_sub -h YOUR_MQTT_IP -t "homeassistant/sensor/dell_r620_power" -u "mqtt_user" -P "mqtt_password"
```
2️⃣ **Check if messages appear:**
```
82  # (Power in Watts)
```

---

## **📜 License**
MIT License

---

## **👨‍💻 Contributing**
Feel free to submit pull requests or issues on GitHub!

---

🚀 **Now you can monitor your Dell server's power consumption in real time via Home Assistant & MQTT!**

