# **YapWrap**
Yap Wrap: The scarf that talks so you don’t have to! Tired of pointless small talk? Let Yap Wrap handle it
---

## **Features**
- **Auto Connect to WiFi:** Easily configure your Raspberry Pi to automatically connect to your network.
- **Run Python Project on Boot:** Set up your ElevenLabs and OpenAI API-powered Python script to launch when your Raspberry Pi starts up.
- **Audio Integration:** Configure USB microphones and speakers for a voice-enabled experience.

---

## **Getting Started**

### **1. Configure WiFi**
To auto-connect your Raspberry Pi to WiFi, edit the `wpa_supplicant.conf` file:

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add your network configuration at the end of the file:

```bash
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="YourNetworkSSID"
    psk="YourNetworkPassword"
}}
```

Save and exit (Ctrl + X, then Y, then Enter).

---

### **2. Run Project on Boot**

#### **A. Create a Shell Script**

1. Navigate to your project folder:

    ```bash
    cd /home/pi/Desktop/<your_project_folder>
    ```

2. Create the shell script to start your Python environment:

    ```bash
    nano start_script.sh
    ```

3. Add the following content to the file:

    ```bash
    #!/bin/bash
    cd /home/pi/Desktop/<your_project_folder>
    source venv/bin/activate
    python eleven.py
    ```

4. Save and exit (Ctrl + X, then Y, then Enter).
5. Make the script executable:

    ```bash
    chmod +x start_script.sh
    ```

---

#### **B. Create a systemd Service**

1. Create the service file:

    ```bash
    sudo nano /etc/systemd/system/eleven.service
    ```

2. Add the following content to the service file:

    ```ini
    [Unit]
    Description=Start Eleven Labs Python Script
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=simple
    User=pi
    WorkingDirectory=/home/pi/Desktop/labra
    ExecStart=/home/pi/Desktop/labra/start_script.sh
    Restart=on-failure
    Environment=OPENAI_API_KEY=your_openai_api_key
    Environment=ELEVENLABS_API_KEY=your_elevenlabs_api_key

    [Install]
    WantedBy=multi-user.target
    ```

3. Save and exit (Ctrl + X, then Y, then Enter).

---

### **3. Grant Access to Audio Devices**

Add your user to the audio group:

```bash
sudo usermod -a -G audio $USER
```

---

### **4. Enable and Test the Service**

1. Reload systemd to recognize the new service:

    ```bash
    sudo systemctl daemon-reload
    ```

2. Enable the service to run at boot:

    ```bash
    sudo systemctl enable eleven.service
    ```

3. Start the service now (for testing):

    ```bash
    sudo systemctl start eleven.service
    ```

4. Check the service status:

    ```bash
    sudo systemctl status eleven.service
    ```

---

## **Setup Steps**

### **Step 1: Update Raspberry Pi**
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### **Step 2: Install System Dependencies**
```bash
sudo apt-get install -y python3-pip python3-dev python3-venv portaudio19-dev libffi-dev libssl-dev libasound-dev libportaudio2 libportaudiocpp0 ffmpeg
```

### **Step 3: Create a Python Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 4: Install Python Libraries**
```bash
pip install --upgrade pip
pip install sounddevice scipy numpy openai gTTS pygame
```

### **Step 5: Set Up API Keys**

1. Obtain your OpenAI and ElevenLabs API keys from their respective dashboards.
2. Export them in your environment:

```bash
export OPENAI_API_KEY='your_openai_api_key'
export ELEVENLABS_API_KEY='your_elevenlabs_api_key'
```

---

### **Step 6: Verify Audio Devices**

- List input devices (microphone):

    ```bash
    arecord -l
    ```

- List output devices (speakers):

    ```bash
    aplay -l
    ```

Note your device numbers and update them in your code accordingly.

---

## **Important Notes**
- **Security Consideration:** Avoid hardcoding API keys directly in your scripts. Use environment files or a secure vault for sensitive information.
- **Logs:** To view the service logs, use:

    ```bash
    sudo journalctl -u eleven.service -f
    ```

---

By following this guide, your **Speak_4_me** project will be up and running, providing a smooth experience for voice-based interactions using ElevenLabs and OpenAI APIs.

Enjoy your automated Raspberry Pi setup!

