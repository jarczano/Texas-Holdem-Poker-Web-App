# Texas-Holdem-Poker-Web-App

## Overview:
The project is an online application that enables a player to engage in a two-player version of Texas Hold'em Poker, also known as heads-up poker, against various types of bots in real-time. The project comprises two primary components: a server implemented in Python using the Flask framework and Flask-SocketIO extension, and a web-based client developed with HTML, CSS, and JavaScript.

![Screenshot_20230916_154334_com android chrome](https://github.com/jarczano/Texas-Holdem-Poker-Web-App/assets/107764304/4c81f55d-8b20-41d0-bc6f-9cda61f64e5b)
![Screenshot_20230916_154453_com android chrome](https://github.com/jarczano/Texas-Holdem-Poker-Web-App/assets/107764304/8b1056f9-c429-49aa-b267-ec2337cdbe3b)

## Project Description
### Server (Python, Flask, Flask-SocketIO):

- The server is implemented in Python using the Flask framework and Flask-SocketIO extension to handle real-time communication.
- It manages the game state, handles player moves, and communicates with the bots.
- Ensures game security and validates player moves.

### Client (HTML, CSS, JavaScript):

- The client provides the graphical user interface for the game, accessible through a web browser.
- It uses HTML for structure, CSS for styling, and JavaScript for user interaction.
- Enables players to make decisions, place bets, and interact with the bots in real-time.

---
### Types of Bots:

#### Bob - Probability-Based Bot with a Mathematical Approach:

- Bot Bob employs a mathematical approach to the game, relying on the analysis of probabilities and strategy.
- It utilizes an advanced algorithm that takes into account the probability of winning and the risk of losing in each round.
- Bob aims to make decisions that maximize the expected value of gains, considering the current state of the game.
- Its goal is to adapt its strategy based on changing game conditions to achieve the most favorable outcomes.

#### Carol - Bot Trained with Reinforcement Learning:

- Bot Carol is an opponent based on a Deep Neural Network (DNN) trained using reinforcement learning (RL) techniques.
- Carol can adjust its strategy based on the current game state.

#### Dave - OpenAI ChatGPT:

- Bot Dave leverages GPT-powered chatbot technology to make decisions in the game.
- The game situation is described in text, and a prompt is generated, which is then passed to the OpenAI API.
- The API returns a response that is interpreted as Dave's decision in the game.

## Link to the Game on Azure Server:

https://heads-up-poker.azurewebsites.net/

## Usage:

- Clone the repository: `git clone https://github.com/jarczano/Sudoku-Solver-Web-App`
- Install the requirements: `pip install -r requirements.txt`
- Run `main.py`: `python main.py`

The application can be accessed on devices connected to the local network using the address displayed after running `main.py`.  

## Technologies:
- Keras
- Tensorflow
- Flask
- Flask-socketIO
- OpenAI

## Related Projects:
- Texas Holdem Poker Reinforcement Learning https://github.com/jarczano/Texas-Holdem-Poker-Reinforcement-Learning
- Texas Holdem Poker Pygame https://github.com/jarczano/Texas-Holdem-Poker-Pygame
  
## License:
- MIT

## Author:
- Jarosław Turczyn
