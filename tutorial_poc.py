#!/usr/bin/env python3
"""
Tutorial PoC for AiNiee HTTP API testing

AiNiee is primarily a PyQt5 desktop application for AI translation.
This PoC demonstrates how to interact with its optional HTTP API service.
"""

import requests
import json
import sys
import os


class AiNieeClient:
    """Client for testing AiNiee HTTP API endpoints."""

    def __init__(self, base_url="http://localhost:3388"):
        self.base_url = base_url
        self.session = requests.Session()

    def test_connection(self):
        """Test if the HTTP service is accessible."""
        try:
            response = self.session.get(f"{self.base_url}/api/status", timeout=5)
            print(f"[*] Testing connection: {self.base_url}")
            print(f"    Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"    Response: {json.dumps(data, indent=2)}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"[!] Error connecting to AiNiee: {e}")
            return False

    def get_status(self):
        """Get the current application status."""
        try:
            response = self.session.get(f"{self.base_url}/api/status", timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[!] Error getting status: {e}")
        return None

    def start_translation(self, input_folder=None, output_folder=None):
        """Start a translation task."""
        url = f"{self.base_url}/api/translate"
        data = {}

        if input_folder:
            data["input_folder"] = input_folder
        if output_folder:
            data["output_folder"] = output_folder

        try:
            if data:
                response = self.session.post(url, json=data, timeout=30)
            else:
                response = self.session.get(url, timeout=30)

            print(f"[*] Starting translation: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"    Response: {json.dumps(result, indent=2)}")
                return result
        except Exception as e:
            print(f"[!] Error starting translation: {e}")
        return None

    def stop_translation(self):
        """Stop the current translation task."""
        try:
            response = self.session.get(f"{self.base_url}/api/stop", timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"[*] Stop response: {json.dumps(result, indent=2)}")
                return result
        except Exception as e:
            print(f"[!] Error stopping translation: {e}")
        return None


def test_http_endpoints(base_url="http://localhost:3388"):
    """Test HTTP endpoints of the AiNiee app."""
    print("=" * 60)
    print("AiNiee HTTP API Test Suite")
    print("=" * 60)

    client = AiNieeClient(base_url)

    # Test 1: Connection
    print("\n[1] Testing Connection")
    print("-" * 40)
    connected = client.test_connection()

    if not connected:
        print("\n[!] Failed to connect to AiNiee HTTP service.")
        print("\nTo enable the HTTP service:")
        print("1. Create Resource/config.json with the following content:")
        print("   {")
        print('     "http_server_enable": true,')
        print('     "http_listen_address": "0.0.0.0:3388"')
        print("   }")
        print("2. Run: docker run -v $(pwd)/config.json:/app/Resource/config.json ...")
        return False

    # Test 2: Get status
    print("\n[2] Getting Application Status")
    print("-" * 40)
    status = client.get_status()
    if status:
        print(f"    App Status: {status.get('app_status', 'N/A')}")
    else:
        print("    Unable to retrieve status")

    # Test 3: Start translation (dry run)
    print("\n[3] Testing Translation Start (Dry Run)")
    print("-" * 40)
    result = client.start_translation()
    if result:
        print(f"    Translation started: {result.get('status', 'N/A')}")
    else:
        print("    Unable to start translation")

    # Test 4: Stop translation
    print("\n[4] Testing Translation Stop")
    print("-" * 40)
    client.stop_translation()

    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)

    return True


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AiNiee HTTP API Test PoC"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:3388",
        help="Base URL of the AiNiee HTTP service (default: http://localhost:3388)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Only get application status"
    )

    args = parser.parse_args()

    if args.status:
        client = AiNieeClient(args.url)
        status = client.get_status()
        if status:
            print(json.dumps(status, indent=2))
        else:
            print("Failed to get status")
            sys.exit(1)
    else:
        test_http_endpoints(args.url)


if __name__ == "__main__":
    main()
