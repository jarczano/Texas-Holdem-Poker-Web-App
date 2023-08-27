/*
document.getElementById('play_with_bot').addEventListener('click', function() {
    window.location.href = "{{ url_for('play', opponent='bot') }}";
});


document.getElementById('play_with_ai').addEventListener('click', function() {
    window.location.href = "{{ url_for('play', opponent='ai') }}";
});

*/
/*
window.matchMedia('(orientation: portrait)').addEventListener('change', event => {
 const portrait = event.matches;
 if (portrait){
    alert('portait')
 }
 else{alert('landscape')}
});
*/

function lock (orientation) {
  // (A1) GO INTO FULL SCREEN FIRST
  let de = document.documentElement;
  if (de.requestFullscreen) { de.requestFullscreen(); }
  else if (de.mozRequestFullScreen) { de.mozRequestFullScreen(); }
  else if (de.webkitRequestFullscreen) { de.webkitRequestFullscreen(); }
  else if (de.msRequestFullscreen) { de.msRequestFullscreen(); }

  // (A2) THEN LOCK ORIENTATION
  screen.orientation.lock(orientation);
}


lock('landscape')



var socket = io.connect(window.location.protocol + '//' + window.location.host);

var button_bot = document.getElementById('play_with_bot');
var button_ai = document.getElementById('play_with_ai');
var button_gpt = document.getElementById('play_with_gpt');

/*
function playWithBot() {
    sessionStorage.setItem('name_opponent', 'Bob');
    socket.emit('select_opponent', 'bot');
    window.location.href = "/play/";
}

function playWithAI() {
    sessionStorage.setItem('name_opponent', 'Celia');
    socket.emit('select_opponent', 'AI');
    window.location.href = "/play/";
    }
*/


socket.on('connect', function () {
  console.log("Connected...!", socket.connected);
});


let selectedOpponent = "bot";

function selectOpponent(opponent){
    selectedOpponent = opponent;
    updateOpponentInfo();
}
//'../static/image/' + text_flop_card3 + ".png";

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
        opponentName.textContent = "Logical bot";
        opponentDescription.textContent = "Take on Bob, a cunning and analytical opponent driven by logic, statistics, and probability. With a sharp mind and calculated decisions, Alice will keep you on your toes as she leverages her deep understanding of the game's dynamics to make each move count. Can you outwit this strategic thinker and emerge as the ultimate poker champion?";
        button_bot.classList.add('selected_button')

        break;
      case "ai":
        opponentName.textContent = "Deep neural network bot";
        opponentPhoto.src = "../static/image/ai_profile.jpg";
        opponentDescription.textContent = "Meet Celia, a formidable adversary powered by cutting-edge technology. Bob has been trained through countless games using reinforcement learning, evolving his strategies to perfection. Armed with a neural network brain, Bob's decisions are based on a fusion of past experiences and predictive algorithms. Prepare to face a poker prodigy who's always ready to adapt and surprise you with his AI-driven finesse.";
        button_ai.classList.add('selected_button')
        break;
      case "gpt":
        opponentName.textContent = "OpenAI ChatGPT";
        opponentPhoto.src = "../static/image/gpt_profile.jpg";
        opponentDescription.textContent = "Ready for a unique challenge? Dylan is not your ordinary opponent; she's powered by the OpenAI ChatGPT API. Engage in witty banter and play poker with a virtual entity that can understand and generate human-like responses. Celia's gameplay combines strategic thinking with engaging conversations, making every hand an entertaining and intriguing experience. Can you outplay Celia in the game of cards and words?";
        button_gpt.classList.add('selected_button')
        break;
      default:
        break;
    }
  }





function play(){
    socket.emit('select_opponent', selectedOpponent);
    window.location.href = "/play/";
}
updateOpponentInfo();

//selectOpponent('bot');


function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else if (document.exitFullscreen) {
    document.exitFullscreen();
  }
}



const button_fullscreen = document.getElementById('button_fullscreen');
button_fullscreen.addEventListener('click', function(){
  toggleFullScreen();
  lock('landscape')
});