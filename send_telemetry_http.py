"""
Send Telemetry Data to ThingsBoard using HTTP
This program sends sensor data to ThingsBoard using the HTTP REST API
"""

import requests
import json
import time
import random
import config
import os
from datetime import datetime


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
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(40.0, 80.0), 2),
        "pressure": round(random.uniform(980.0, 1020.0), 2),
        "light": random.randint(0, 100)
    }


def send_telemetry_http(access_token, telemetry_data):
    """Send telemetry data via HTTP POST"""
    # Construct URL
    url = f"https://{config.THINGSBOARD_HOST}/api/v1/{access_token}/telemetry"
    
    # Set headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, json=telemetry_data, timeout=10)
        
        if response.status_code == 200:
            return True, "Success"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    
    except requests.exceptions.RequestException as e:
        return False, str(e)


def main():
    """Main function to send telemetry via HTTP"""
    print("=" * 60)
    print("Send Telemetry to ThingsBoard via HTTP")
    print("=" * 60)
    
    # Load access token
    access_token = load_access_token()
    if not access_token:
        print("✗ No ACCESS_TOKEN available")
        return
    
    print(f"\nThingsBoard Host: {config.THINGSBOARD_HOST}:{config.THINGSBOARD_HTTP_PORT}")
    print(f"Using ACCESS_TOKEN: {access_token[:10]}...")
    print()
    
    # Send telemetry data multiple times
    num_messages = int(input("How many telemetry messages to send? [default: 5]: ") or "5")
    interval = float(input("Interval between messages (seconds)? [default: 2]: ") or "2")
    
    print(f"\nSending {num_messages} messages with {interval}s interval...\n")
    
    success_count = 0
    fail_count = 0
    
    for i in range(num_messages):
        # Generate telemetry data
        telemetry = generate_telemetry_data()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] Message {i+1}/{num_messages}:")
        print(f"Data: {json.dumps(telemetry, indent=2)}")
        
        # Send via HTTP
        success, message = send_telemetry_http(access_token, telemetry)
        
        if success:
            print(f"✓ Sent successfully")
            success_count += 1
        else:
            print(f"✗ Failed: {message}")
            fail_count += 1
        
        # Wait before sending next message
        if i < num_messages - 1:
            time.sleep(interval)
    
    print("\n" + "=" * 60)
    print(f"Summary: {success_count} successful, {fail_count} failed")
    print("=" * 60)


if __name__ == "__main__":
    main()
