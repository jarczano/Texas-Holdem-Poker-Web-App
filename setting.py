from flask_socketio import SocketIO
from flask import Flask
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Create app flask
app = Flask(__name__)
socketio = SocketIO(app)

# Set small and big blind value
BB = 50
SB = 25

# To peek text information about game
show_game = True

# Length of the break  after round
#time_pause_round_end = 1000
time_pause_round_end_split = 8
time_pause_round_end_one_winner = 4


# A dictionary that stores all actively playing clients. "sid number" : "game instance"
games = {}

# Here login to your OpenAI account. You need key to API. To get access to key can use Azure key vault, another service,
# or just write key
"""
key_vault_url = "https://apike.vault.azure.net/"
secret_name = "OpenAI"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)
openai_api_key = client.get_secret(secret_name).value
"""
# without azure key vault:
openai_api_key = 'xxx'

openai.api_key = openai_api_key




