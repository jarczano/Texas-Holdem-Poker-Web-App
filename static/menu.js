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

/*
import socket from './start.js';
*/

//import { testFunction } from '../static/start.js';
//import { testFunction } from '../start.js'
//console.log('from menu');
//console.log(testFunction);
//console.log(window.sharedVariable);

//var socket = window.socket

//var socket = io();
/*export default socket;
*/

/*
socket.on('connect', function () {
  const sid = socket.id;
  console.log("Client menu. player id: ", sid);
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


//lock('landscape')


/*
var socket = io.connect(window.location.protocol + '//' + window.location.host);
*/

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

/*
socket.on('connect', function () {
      const sid = socket.id;
  console.log("Connected...!", socket.connected);
  console.log("SID", sid);
});
*/

var selectedOpponent = "bot";

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




/*
function play(){
    console.log("select_opponent...!", selectedOpponent);
    socket.emit('select_opponent', selectedOpponent);
    setTimeout(function() {
        window.location.href = "/play/";
    }, 10)
}*/

function play(){
    console.log("select_opponent...!", selectedOpponent);
    //text_href= "/play/bot" ;//+ selectedOpponent;
    text_href= "/play/" + selectedOpponent;
    console.log(text_href);
    //socket.emit('select_opponent', selectedOpponent);
    window.location.href = text_href;
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