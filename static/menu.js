/*
document.getElementById('play_with_bot').addEventListener('click', function() {
    window.location.href = "{{ url_for('play', opponent='bot') }}";
});


document.getElementById('play_with_ai').addEventListener('click', function() {
    window.location.href = "{{ url_for('play', opponent='ai') }}";
});

*/
var socket = io.connect(window.location.protocol + '//' + window.location.host);



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
    const opponentDescription = document.getElementById("opponent-description");

    switch (selectedOpponent) {
      case "bot":
        opponentPhoto.src = "../static/image/logic_photo.jpg";
        opponentDescription.textContent = "Description of Alice.";
        break;
      case "ai":
        opponentPhoto.src = "../static/image/dnn_photo.png";
        opponentDescription.textContent = "Description of Bob.";
        break;
      case "gpt":
        opponentPhoto.src = "../static/image/gpt_photo.jpg";
        opponentDescription.textContent = "Description of Celia.";
        break;
      default:
        break;
    }
  }

updateOpponentInfo();

//selectOpponent('bot');