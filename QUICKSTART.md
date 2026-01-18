# Quick Start Guide

## Before You Begin

You need to get provisioning credentials from ThingsBoard first.

### Get Credentials from ThingsBoard:

1. Go to https://demo.thingsboard.io (or your ThingsBoard instance)
2. Log in to your account
3. Navigate to: **Device profiles** → **default** (or your profile)
4. Click on **Device provisioning** tab
5. Enable "Allow device creation" if not already enabled
6. Copy these values:
   - **Provision device key**
   - **Provision device secret**

## Configuration Steps

1. Open `.env` file and update:
```bash
THINGSBOARD_HOST=demo.thingsboard.io
PROVISION_DEVICE_KEY=paste_your_key_here
PROVISION_DEVICE_SECRET=paste_your_secret_here
DEVICE_NAME=MyTestDevice
```

**Important:** Never share or commit your `.env` file!

## Running the Programs

### 1. Provision Device (Get ACCESS_TOKEN)
```bash
python provision_device.py
```

Expected output:
```
✓ Connected to ThingsBoard MQTT Broker
✓ Device provisioned successfully!
✓ ACCESS_TOKEN: xxxxxxxxxx
✓ Token saved to access_token.txt
```

### 2. Send Data via MQTT
```bash
python send_telemetry_mqtt.py
```

You'll be asked:
- How many messages? (default: 5)
- Interval? (default: 2 seconds)

### 3. Send Data via HTTP
```bash
python send_telemetry_http.py
```

Same prompts as MQTT version.

## Verify on ThingsBoard

1. Go to **Devices** page
2. Find your device (e.g., "MyTestDevice")
3. Click on it
4. Go to **Latest telemetry** tab
5. You should see: temperature, humidity, pressure, light

## Common Issues

**"Connection refused"**
- Check if `THINGSBOARD_HOST` is correct
- Verify internet connection
- Try `demo.thingsboard.io` if using demo server

**"Provisioning failed"**
- Double-check provision key and secret
- Make sure device provisioning is enabled
- Device name might already exist (try a different name)

**"No ACCESS_TOKEN"**
- Run `provision_device.py` first
- Check if `access_token.txt` was created

## Project Files

- `.env` - Configuration (EDIT THIS FIRST)
- `.env.example` - Template for .env file
- `config.py` - Loads configuration from .env
- `provision_device.py` - Get ACCESS_TOKEN
- `send_telemetry_mqtt.py` - Send via MQTT
- `send_telemetry_http.py` - Send via HTTP
- `access_token.txt` - Auto-generated token (don't edit)
