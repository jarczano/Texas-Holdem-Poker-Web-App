var button_bot = document.getElementById('play_with_bot');
var button_ai = document.getElementById('play_with_ai');
var button_gpt = document.getElementById('play_with_gpt');

var selectedOpponent = "bot";

function selectOpponent(opponent){
    selectedOpponent = opponent;
    updateOpponentInfo();
}


function updateOpponentInfo() {
    const opponentPhoto = document.getElementById("opponent-photo");
    const opponentName = document.getElementById("opponent-name")
    const opponentDescription = document.getElementById("opponent-description");

    const buttons = document.querySelectorAll('.button');
    buttons.forEach(button => {
        button.classList.remove('selected_button');
    });

    switch (selectedOpponent) {
      case "bot":
        opponentPhoto.src = "../static/image/bot_profile.jpg";
        opponentName.textContent = "The Mathematical Mind";
        opponentDescription.textContent = "a poker bot driven by pure math, logic, and probability. He calculates odds and strategies with mathematical precision. Challenge Bob for a battle of wits where every move is rooted in solid logic.";
        button_bot.classList.add('selected_button')

        break;
      case "ai":
        opponentName.textContent = "Artificial intelligence";
        opponentPhoto.src = "../static/image/ai_profile.jpg";
        opponentDescription.textContent = "an AI bot powered by neural networks and reinforcement learning. She evolves her game as you play, constantly adapting and improving her strategies. Can you stay ahead of an AI that learns from every hand?";
        button_ai.classList.add('selected_button')
        break;
      case "gpt":
        opponentName.textContent = "OpenAI ChatGPT";
        opponentPhoto.src = "../static/image/gpt_profile.jpg";
        opponentDescription.textContent = "your in-game poker companion powered by OpenAI's Chat GPT. In this unique gaming experience, you'll face off against Chat GPT, who receives prompts about the game situation and provides decisions based on a wealth of information. Can you outwit an AI that's constantly analyzing the game dynamics for the perfect move?";
        button_gpt.classList.add('selected_button')
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
