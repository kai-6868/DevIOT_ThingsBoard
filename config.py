"""Configuration module that loads settings from .env file"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ThingsBoard Configuration
THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST", "demo.thingsboard.io")
THINGSBOARD_PORT = int(os.getenv("THINGSBOARD_PORT", "1883"))
THINGSBOARD_HTTP_PORT = int(os.getenv("THINGSBOARD_HTTP_PORT", "8080"))

# Device Provisioning credentials
PROVISION_DEVICE_KEY = os.getenv("PROVISION_DEVICE_KEY", "PUT_PROVISION_KEY_HERE")
PROVISION_DEVICE_SECRET = os.getenv("PROVISION_DEVICE_SECRET", "PUT_PROVISION_SECRET_HERE")

# Device name
DEVICE_NAME = os.getenv("DEVICE_NAME", "MyIoTDevice")
