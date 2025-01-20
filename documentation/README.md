
# Secure Communications

## Overview
The Secure Communications repository has been enhanced to include advanced encryption, real-time communication, and AI-powered analysis.

### New Features
1. **AI-Powered Message Analysis**
    - Endpoint: `/analyze_message`
    - Method: `POST`
    - Description: Analyzes the sentiment and intent of messages.
    - Example Request:
      ```json
      {
          "message": "Urgent: This is a critical situation."
      }
      ```
    - Example Response:
      ```json
      {
          "analysis": [{"label": "NEGATIVE", "score": 0.98}]
      }
      ```

2. **Secure Messaging**
    - Endpoint: `/secure_message`
    - Method: `POST`
    - Description: Encrypts messages using post-quantum encryption.
    - Example Request:
      ```json
      {
          "peer_public_key": "abcd1234...",
          "message": "Secure message content"
      }
      ```
    - Example Response:
      ```json
      {
          "encrypted_message": "ef5678...",
          "iv": "123456..."
      }
      ```

3. **Real-Time Communication**
    - Enables real-time messaging using Flask-SocketIO.
    - Events:
      - `send_message`: Send a message to connected clients.
      - `receive_message`: Receive broadcasted messages.

### Getting Started
1. Install dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the application:
    ```bash
    python app.py
    ```
