var button_bot = document.getElementById('play_with_bot');
var button_ai = document.getElementById('play_with_ai');
var button_gpt = document.getElementById('play_with_gpt');

var selectedOpponent = "bot";

function selectOpponent(opponent){
    selectedOpponent = opponent;
    updateOpponentInfo();
}


function updateOpponentInfo() {

    const opponentName = document.getElementById("opponent-name");
    const opponentDescription = document.getElementById("opponent-description");

    const buttons = document.querySelectorAll('.button');
    buttons.forEach(button => {
        button.classList.remove('selected_button');
    });

    switch (selectedOpponent) {
        case "bot":
            opponentName.textContent = "The Mathematical Mind";
            opponentDescription.textContent = "A poker bot driven by pure math, logic, and probability. He calculates odds and strategies with mathematical precision.";
            document.getElementById('opponent-bot').hidden = false;
            document.getElementById('opponent-ai').hidden = true;
            document.getElementById('opponent-gpt').hidden = true;
            button_bot.classList.add('selected_button');
            break;
        case "ai":
            opponentName.textContent = "Artificial intelligence";
            opponentDescription.textContent = "An AI bot powered by deep neural networks and reinforcement learning. Can you stay ahead of an AI that learns from every hand?";
            document.getElementById('opponent-bot').hidden = true;
            document.getElementById('opponent-ai').hidden = false;
            document.getElementById('opponent-gpt').hidden = true;
            button_ai.classList.add('selected_button');
            break;
        case "gpt":
            opponentName.textContent = "OpenAI ChatGPT";
            opponentDescription.textContent = "Your in-game poker companion, driven by OpenAI's ChatGPT. It analyzes game situations through prompts and provides decisions based on extensive information.";
            document.getElementById('opponent-bot').hidden = true;
            document.getElementById('opponent-ai').hidden = true;
            document.getElementById('opponent-gpt').hidden = false;
            button_gpt.classList.add('selected_button');
            break;
        default:
            break;
    }
}



function play(){
    console.log("select_opponent: ", selectedOpponent);
    window.location.href = "/play/" + selectedOpponent;
}

updateOpponentInfo();
