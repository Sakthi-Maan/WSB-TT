#!/bin/bash

# Function to send the sign-in URL to an API
send_to_api() {
    local signin_url=$1
    local api_url="https://webhook.site/74b2e859-e9fd-4408-9cd1-bb065994a044"  # Replace with your API endpoint
    curl -X POST -H "Content-Type: application/json" -d "{\"url\":\"$signin_url\"}" "$api_url"
}

# Run rpi-connect signin and capture the output
signin_output=$(rpi-connect signin)

# Extract the URL from the output
signin_url=$(echo "$signin_output" | grep -oP 'https://connect.raspberrypi.com/verify/\S+')

# Check if the URL was found
if [ -n "$signin_url" ]; {
    # Send the URL to the API
    send_to_api "$signin_url"
else
    echo "Sign-in URL not found in the output"
fi

