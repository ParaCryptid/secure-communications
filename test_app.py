
import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the home route
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Secure Communications System is fully functional.' in response.data

# Test the send_message route
def test_send_message(client):
    data = {"message": "Confidential message"}
    response = client.post('/send_message', json=data)
    assert response.status_code == 200
    assert "encrypted_message" in response.get_json()

# Test the receive_message route
def test_receive_message(client):
    data = {"message": "Confidential message"}
    send_response = client.post('/send_message', json=data)
    encrypted_message = send_response.get_json()["encrypted_message"]

    receive_response = client.post('/receive_message', json={"encrypted_message": encrypted_message})
    assert receive_response.status_code == 200
    assert receive_response.get_json()["decrypted_message"] == "Confidential message"

# Test the log_message route
def test_log_message(client):
    data = {"message": "Log this message"}
    response = client.post('/log_message', json=data)
    assert response.status_code == 200
    assert "Message logged to blockchain." in response.get_json()["status"]
