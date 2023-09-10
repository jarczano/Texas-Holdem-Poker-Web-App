from flask_socketio import SocketIO
from flask import Flask
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)
socketio = SocketIO(app)

# blinds
BB = 50
SB = 25

show_game = True
time_pause_round_end = 8

games = {}

key_vault_url = "https://apike.vault.azure.net/"
secret_name = "OpenAI"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)
openai_api_key = client.get_secret(secret_name).value

openai.api_key = openai_api_key




