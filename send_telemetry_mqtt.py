"""
Send Telemetry Data to ThingsBoard using MQTT
This program sends sensor data to ThingsBoard using the MQTT protocol
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import config
import os
from datetime import datetime


def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("✓ Connected to ThingsBoard MQTT Broker")
    else:
        print(f"✗ Connection failed with code {rc}")


def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(f"✓ Message {mid} published successfully")


def load_access_token():
    """Load ACCESS_TOKEN from file or prompt user"""
    if os.path.exists("access_token.txt"):
        with open("access_token.txt", "r") as f:
            token = f.read().strip()
            print(f"✓ Loaded ACCESS_TOKEN from file")
            return token
    else:
        print("⚠ access_token.txt not found")
        token = input("Enter your ACCESS_TOKEN: ").strip()
        return token


def generate_telemetry_data():
    """Generate simulated sensor data"""
    return {
        "ts": int(time.time() * 1000),  # Current timestamp in milliseconds
        "values": {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 80.0), 2),
            "pressure": round(random.uniform(980.0, 1020.0), 2),
            "light": random.randint(0, 100)
        }
    }


def main():
    """Main function to send telemetry via MQTT"""
    print("=" * 60)
    print("Send Telemetry to ThingsBoard via MQTT")
    print("=" * 60)
    
    # Load access token
    access_token = load_access_token()
    if not access_token:
        print("✗ No ACCESS_TOKEN available")
        return
    
    print(f"\nThingsBoard Host: {config.THINGSBOARD_HOST}:{config.THINGSBOARD_PORT}")
    print(f"Using ACCESS_TOKEN: {access_token[:10]}...")
    print()
    
    # Create MQTT client
    client = mqtt.Client()
    
    # Set username as ACCESS_TOKEN
    client.username_pw_set(access_token)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Connect to ThingsBoard
        print(f"Connecting to {config.THINGSBOARD_HOST}:{config.THINGSBOARD_PORT}...")
        client.connect(config.THINGSBOARD_HOST, config.THINGSBOARD_PORT, 60)
        
        # Start loop
        client.loop_start()
        time.sleep(2)  # Wait for connection
        
        # Send telemetry data multiple times
        num_messages = int(input("How many telemetry messages to send? [default: 5]: ") or "5")
        interval = float(input("Interval between messages (seconds)? [default: 2]: ") or "2")
        
        print(f"\nSending {num_messages} messages with {interval}s interval...\n")
        
        for i in range(num_messages):
            # Generate telemetry data
            telemetry = generate_telemetry_data()
            
            # Publish to telemetry topic
            result = client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{current_time}] Message {i+1}/{num_messages}:")
            print(f"Timestamp: {telemetry['ts']}")
            print(f"Data: {json.dumps(telemetry['values'], indent=2)}")
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"✗ Failed to publish: {result.rc}")
            
            # Wait before sending next message
            if i < num_messages - 1:
                time.sleep(interval)
        
        # Wait for all messages to be sent
        time.sleep(2)
        
        client.loop_stop()
        client.disconnect()
        
        print("\n✓ All messages sent successfully")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
