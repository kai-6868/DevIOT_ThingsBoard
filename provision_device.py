"""
Device Provisioning Program using MQTT
This program registers a new device with ThingsBoard and receives an ACCESS_TOKEN
"""

import paho.mqtt.client as mqtt
import json
import time
import config

# Global variable to store the received access token
access_token = None


def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("✓ Connected to ThingsBoard MQTT Broker")
        # Subscribe to provision response topic
        client.subscribe("/provision/response")
        print("✓ Subscribed to /provision/response")
        
        # Send provision request
        send_provision_request(client)
    else:
        print(f"✗ Connection failed with code {rc}")


def on_message(client, userdata, msg):
    """Callback when message is received"""
    global access_token
    
    print(f"\n✓ Received response on topic: {msg.topic}")
    
    try:
        response = json.loads(msg.payload.decode())
        print(f"Response: {json.dumps(response, indent=2)}")
        
        if response.get("status") == "SUCCESS":
            access_token = response.get("credentialsValue")
            print(f"\n✓ Device provisioned successfully!")
            print(f"✓ ACCESS_TOKEN: {access_token}")
            
            # Save token to file
            with open("access_token.txt", "w") as f:
                f.write(access_token)
            print(f"✓ Token saved to access_token.txt")
        else:
            print(f"\n✗ Provisioning failed: {response}")
    except Exception as e:
        print(f"✗ Error parsing response: {e}")
    
    # Disconnect after receiving response
    client.disconnect()


def send_provision_request(client):
    """Send provision request to ThingsBoard"""
    provision_request = {
        "deviceName": config.DEVICE_NAME,
        "provisionDeviceKey": config.PROVISION_DEVICE_KEY,
        "provisionDeviceSecret": config.PROVISION_DEVICE_SECRET
    }
    
    print("\nSending provision request...")
    print(f"Payload: {json.dumps(provision_request, indent=2)}")
    
    result = client.publish("/provision/request", json.dumps(provision_request))
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("✓ Provision request sent successfully")
    else:
        print(f"✗ Failed to send provision request: {result.rc}")


def main():
    """Main function to provision device"""
    print("=" * 60)
    print("ThingsBoard Device Provisioning via MQTT")
    print("=" * 60)
    print(f"\nDevice Name: {config.DEVICE_NAME}")
    print(f"ThingsBoard Host: {config.THINGSBOARD_HOST}:{config.THINGSBOARD_PORT}")
    print()
    
    # Create MQTT client
    client = mqtt.Client()
    
    # Set username for provisioning
    client.username_pw_set("provision")
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to ThingsBoard
        print(f"Connecting to {config.THINGSBOARD_HOST}:{config.THINGSBOARD_PORT}...")
        client.connect(config.THINGSBOARD_HOST, config.THINGSBOARD_PORT, 60)
        
        # Start loop and wait for response
        client.loop_start()
        
        # Wait for provisioning to complete (max 10 seconds)
        timeout = 10
        elapsed = 0
        while access_token is None and elapsed < timeout:
            time.sleep(0.5)
            elapsed += 0.5
        
        if access_token is None:
            print("\n✗ Timeout waiting for provision response")
        
        client.loop_stop()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
