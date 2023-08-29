var socket = io.connect(window.location.protocol + '//' + window.location.host);

var show_end_round = false;
const time_to_show_end_round = 7000;
const time_delay_hide_action_container = 1;
// Send start game to the serever
socket.emit('start_game');

const common_card1 = document.getElementById('common_card1');
const common_card2 = document.getElementById('common_card2');
const common_card3 = document.getElementById('common_card3');
const common_card4 = document.getElementById('common_card4');
const common_card5 = document.getElementById('common_card5');

const player_card1 = document.getElementById('player_card1');
const player_card2 = document.getElementById('player_card2');

const player_stack = document.getElementById('player_stack');

const opponent_card1 = document.getElementById('opponent_card1');
const opponent_card2 = document.getElementById('opponent_card2');

const opponent_stack = document.getElementById('opponent_stack');

const player_bet = document.getElementById('player_bet');
const opponent_bet = document.getElementById('opponent_bet');
const pot = document.getElementById('pot');



const button_call = document.getElementById('button_call');
const button_check = document.getElementById('button_check');
const button_All_in = document.getElementById('button_All-in');
const button_Fold = document.getElementById('button_Fold');

const raise_container = document.getElementById('raise_container');
const button_Raise = document.getElementById('button_Raise');
const slider_raise = document.getElementById('slider_raise');

const action_container = document.getElementById('action_container');

const raiseValue = document.getElementById('raiseValue');

const name_opponent = sessionStorage.getItem('name_opponent');



slider_raise.addEventListener('input', () => {
   // console.log("sliver val",slider_raise.value);
    button_Raise.textContent = "Raise " + String(slider_raise.value) + " $";
    //console.log("sliver val",slider_raise.value);
});



const game_info = document.getElementById('game_info');

socket.on('connect', function () {
  console.log("Connected...!", socket.connected);
});




// Player card
socket.on('deal_player_cards', function(deal_player_cards){
  console.log('Received response deal_player_card');
  var [text_player_card1, text_player_card2] = deal_player_cards;

  player_card1.src = '../static/image/' + text_player_card1 + '.png';
  player_card2.src = '../static/image/'+ text_player_card2 + '.png';
  player_card1.style.display = 'flex';
  player_card2.style.display = 'flex';
  // mozna dopisać zeby też rozdał przeciwnikowi ale to z jakas animacja zas
});


// Opponent card
socket.on('deal_opponent_cards', function(deal_opponent_cards){
    // to jest zeby potem najwyzej zrobic jakas animacje rozdawania

  opponent_card1.style.display = 'flex';
  opponent_card2.style.display = 'flex';
  opponent_card1.src = '../static/image/yellow_back.png';
  opponent_card2.src = '../static/image/yellow_back.png';

});


// Flop
socket.on('deal_flop_cards', function(deal_flop_cards){

  console.log('Received response deal_flop_cards');
  var [text_flop_card1, text_flop_card2, text_flop_card3] = deal_flop_cards;

  common_card1.src = '../static/image/' + text_flop_card1 + ".png";
  common_card2.src = '../static/image/' + text_flop_card2 + ".png";
  common_card3.src = '../static/image/' + text_flop_card3 + ".png";
  common_card1.style.opacity = 1;
  common_card2.style.opacity = 1;
  common_card3.style.opacity = 1;

  addMessage('Flop cards: ' + text_flop_card1 + ', ' + text_flop_card2 + ', ' + text_flop_card3)
});


// Turn
socket.on('deal_turn_card', function(deal_turn_card){
  console.log('Received response deal_turn_card');
  var [text_turn_card1] = deal_turn_card;
  common_card4.src = '../static/image/' + text_turn_card1 + ".png";
  common_card4.style.opacity = 1;

  addMessage('Turn card: ' + text_turn_card1)
});

// River
socket.on('deal_river_card', function(deal_river_card){
  console.log('Received response deal_river_card');
  var [text_river_card1] = deal_river_card;
  common_card5.src = '../static/image/' + text_river_card1 + ".png";
  common_card5.style.opacity = 1;

  addMessage('River card: ' + text_river_card1)
});

// Change my mind, opponent decision will be dispaly only in message container
// Opponent decision
/*

const opponent_decision = document.getElementById('opponent_decision');

socket.on('opponent_decision', function(opponent_dec){
  console.log('Received response opponent_decision');
  console.log(opponent_dec);

  var [text_decision, raise_value] = opponent_dec;
  // tutaj jeszcze jakies animacje pewnie i jako funckje to odpalic
  if (text_decision == 'Raise'){
    text = text_decision + " " + String(raise_value) + " $"

  }
  else{text = text_decision}
  opponent_decision.innerText = text;
  opponent_decision.style.display = 'flex';

  // tutaj nie ma czym jest name_opponent
  //addMessage(name_opponent + ' ' + text)
});


// Hide opponent decision
socket.on('hide_opponent_decision', function(){
    opponent_decision.style.display = 'none';
});

*/


socket.on('message_decision', function(text_message){
    addMessage(text_message);
});


socket.on('finish_game', function(text_message){
    addMessage(text_message, 'end game');
});



// Player option
socket.on('player_option', function(player_option){
  console.log('Received response player_option');
  action_container.style.display = 'flex';

  var [option_check, option_call, option_raise_from, option_raise_to] = player_option;
  //[false/true     int/false  int/false    int/false]
  console.log(player_option)
  // tutaj jeszcze jakies animacje pewnie i jako funckje to odpalic
  if (String(option_check) == "true"){
    button_check.style.display = "flex";
  }
  else{button_check.style.display = "none";}

    console.log('test response player_option', 1)

  if (String(option_call) != "false"){
    button_call.style.display = "flex";
    button_call.textContent = "Call " + option_call + " $";
  }
   else{button_call.style.display = "none";
   }

console.log('test response player_option', 2)

  if (String(option_raise_from) != "false"){
    button_Raise.style.display = "flex"; // moze to tu nie jest potrzebme
    raise_container.style.display = "flex";
    button_Raise.textContent = "Raise " + option_raise_from + " $";
    slider_raise.min = option_raise_from;
    slider_raise.value = option_raise_from;
    slider_raise.max = option_raise_to;
    }
    else{
    raise_container.style.display = "none";
    }
   console.log('test response player_option', 3)
});



// update bet value
socket.on('update_bet', function(update_bet){
    console.log('Update bet', update_bet);
  var [player_name, new_player_bet] = update_bet;
  if (player_name == "Alice"){
    if (new_player_bet != 0){
        /*addMessage('Alice bet ' + new_player_bet + " $")*/
        player_bet.textContent = new_player_bet + " $";
        player_bet.style.display='flex'
    }
    else{player_bet.style.display='none';
    }
  }
  else{
    if (new_player_bet != 0){

        /*addMessage(player_name + ' bet ' + new_player_bet + " $")*/
        opponent_bet.textContent = new_player_bet + " $";
        opponent_bet.style.display='flex';
    }
    else{opponent_bet.style.display='none';}
    }
  }
);



// update stack value
socket.on('update_stack', function(update_stack){
  var [player_name, new_player_stack] = update_stack;
  console.log(player_name, new_player_stack);
  if (player_name == "Alice"){
    player_stack.textContent = new_player_stack + " $";
  }
  else{
    opponent_stack.textContent = new_player_stack + " $";
  }
});

// update pot
socket.on('update_pot', function(update_pot){
  var [new_pot] = update_pot;
   pot.textContent = "Pot: " + update_pot + " $";
   pot.style.display = 'flex';
});




function clean_table(){
    // reset view table, card, bet, pot
    player_card1.style.display = 'none';
    player_card2.style.display = 'none';
    opponent_card1.style.display = 'none';
    opponent_card2.style.display = 'none';
    common_card1.style.opacity = 0;
    common_card2.style.opacity = 0;
    common_card3.style.opacity = 0;
    common_card4.style.opacity = 0;
    common_card5.style.opacity = 0;
    player_bet.style.display = 'none';
    opponent_bet.style.display = 'none';
    pot.style.display = 'none';
}



// Finish round -> one player win
/*
socket.on('finish_round_one_player', function(finish_round_one_player){

  console.log('Received response finish_round');
  var [winner_name, pot_win] = finish_round_one_player;
  game_info.innerText = winner_name + " win " + pot_win;
  game_info.style.display = 'flex';

  addMessage(winner_name + " win " + pot_win);
   setTimeout(function(){
    game_info.style.display = 'none';
    clean_table();
  }, time_to_show_end_round);
});
*/

// Finish round -> one player win
socket.on('finish_round_one_player', function(finish_round_one_player){

  console.log('Received response finish_round');
  var [winner_name, pot_win] = finish_round_one_player;
  addMessage(winner_name + " win " + pot_win + "$");

   setTimeout(function(){
    clean_table();
  }, time_to_show_end_round);

});




/*
// finish round -> winners
socket.on('finish_round_split_pot', function(finish_round_split_pot){
  console.log('Received response finish_round');

  var [player_name, player_hand, player_pot_win] = finish_round_split_pot;

  game_info.innerText = player_name + ' with ' + player_hand + ' win ' + player_pot_win + " $"
  //game_info.innerText = "Alice with "+ hand_player +" win " + pot_win_player +'\n' + "Bob with " + hand_opponent + "  win " + pot_win_opponent;

  //player_stack.textContent = new_stack_player
  //opponent_stack.textContent = new_stack_opponent
  // tutaj jeszcze trzeba odslonic karty przeciwnika
  // show down
  opponent_card1.src = '../static/image/' + text_opponent_card1 + ".png";
  opponent_card2.src = '../static/image/' + text_opponent_card2 + ".png";
  // potem jeszcze w nowej rundzie pamietac zeby zaslonic karty przeciwnika
});
*/

// Finish round -> split pot
/*
socket.on('finish_round_split_pot', function(finish_round_split_pot){
  console.log('Received response finish_round');

  var [name_player1, hand_player1, pot_win_player1, name_player2, hand_player2, pot_win_player2] = finish_round_split_pot;
  game_info.innerText = name_player1 + ' with ' + hand_player1 + ' win ' + pot_win_player1 + '\n' + name_player2 + ' with ' + hand_player2 + ' win ' + pot_win_player2;
  game_info.style.display = 'flex';


  addMessage(name_player1 + ' with ' + hand_player1 + ' win ' + pot_win_player1);
  addMessage(name_player2 + ' with ' + hand_player2 + ' win ' + pot_win_player2);

   setTimeout(function(){
    game_info.style.display = 'none';
    clean_table();
  }, time_to_show_end_round);
});
*/

socket.on('finish_round_split_pot', function(finish_round_split_pot){
  console.log('Received response finish_round');

  var [name_player1, hand_player1, pot_win_player1, name_player2, hand_player2, pot_win_player2] = finish_round_split_pot;

  addMessage(name_player1 + ' with ' + hand_player1 + ' win ' + pot_win_player1 + "$");
  addMessage(name_player2 + ' with ' + hand_player2 + ' win ' + pot_win_player2 + "$");
  /*
  addMessage(name_player1 + ' has ' + hand_player1 + ' win ' + pot_win_player1);
  addMessage(name_player2 + ' has ' + hand_player2 + ' win ' + pot_win_player2);

  addMessage(name_player1 + ' win ' + pot_win_player1);
  addMessage(name_player2 + ' win ' + pot_win_player2);
*/

   setTimeout(function(){
    clean_table();
  }, time_to_show_end_round);

});




// show down
socket.on('show_down', function(show_down){
  console.log('Received response show_down');

  var [text_opponent_card1 ,text_opponent_card2] = show_down;

  // show down
  opponent_card1.src = '../static/image/' + text_opponent_card1 + ".png";
  opponent_card2.src = '../static/image/' + text_opponent_card2 + ".png";
  // potem jeszcze w nowej rundzie pamietac zeby zaslonic karty przeciwnika
});



// Finish game
/*
socket.on('finish_game', function(finish_game){
  console.log('Received response finish_game');
  var [looser_name] = finish_game;
  if (looser_name == 'Alice'){
    winner_name = name_opponent
  }
  else{ winner_name = 'Alice'}
  game_info.style.display = 'flex';
  game_info.innerText = winner_name + ' win game';

});

function hide_action_container(){
  setTimeout(function(){
    action_container.style.display = 'none'
  }, time_delay_hide_action_container);
}*/




function hide_action_container(){
  setTimeout(function(){
    action_container.style.display = 'none'
  }, time_delay_hide_action_container);
}


// Send message to server -------------------------------------------------------------------------------------
// send call player decision to serwer
button_call.addEventListener('click', function(){
  socket.emit('player_decision', ['call', 0])
  hide_action_container()
});

// send check player decision to serwer
button_check.addEventListener('click', function(){
  socket.emit('player_decision', ['check', 0])
  hide_action_container()
});

// send fold player decision to serwer
button_Fold.addEventListener('click', function(){
  socket.emit('player_decision', ['fold', 0])
  hide_action_container()
});

// send all-in player decision to serwer
button_All_in.addEventListener('click', function(){
  socket.emit('player_decision', ['all-in', 0])
  hide_action_container()
});

// send raise player decision to serwer
button_Raise.addEventListener('click', function(){
  socket.emit('player_decision', ['raise', slider_raise.value])
  hide_action_container()
});
// Send message to server -------------------------------------------------------------------------------------

socket.on('redirect', function(data) {
    window.location.href = data.url;
});


// Message container ---------------------------------------------------------
function addMessage(message, special=null) {
    const messageContainer = document.getElementById('messageContainer');
    const messageElement = document.createElement('div');

    messageElement.className = 'message';
    messageElement.textContent = message;

    if (message === "New round") {
        messageElement.classList.add('new-round');
    }

    if (special == 'end game'){
        messageElement.classList.add('end-round');
    }

    messageContainer.appendChild(messageElement);

    // Scroll to the bottom to show the latest message
    messageContainer.scrollTop = messageContainer.scrollHeight;
}





/*
// update_stack_after_player_decision
socket.on('update_stack', function(update_stack){
  console.log('Received response update_stack');
  var [new_stack_player, new_bet_player, new_pot] = update_stack;
  player_stack.textContent = new_stack_player;
  player_bet.textContent = new_bet_player;
  pot.textContent = new_pot;
});
*/



/*

// Player card
socket.on('deal_player_cards', function(deal_player_cards){
  console.log('Received response deal_player_card');
  var [text_player_card1, text_player_card2] = deal_player_cards;
  show_player_cards(text_player_card1, text_player_card2)

  // mozna dopisać zeby też rozdał przeciwnikowi ale to z jakas animacja zas
});


function show_player_cards(text_player_card1, text_player_card2){
  if (show_end_round){
  console.log('not show_end_round');
    setTimeout(() => show_player_cards(text_player_card1, text_player_card2), 200);
  }
  else{
   console.log('show_end_round');
    player_card1.src = '../static/image/' + text_player_card1 + '.png';
    player_card2.src = '../static/image/'+ text_player_card2 + '.png';
  }

}
*/

/*
// update_stack
socket.on('update_stack', function(update_stack){
  console.log('Received response update_stack');
  var [new_stack_player, new_stack_opponent] = update_stack;
  player_stack.textContent = new_stack_player
  opponent_stack.textContent = new_stack_opponent
});
*/

/*
function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else if (document.exitFullscreen) {
    document.exitFullscreen();
  }
}



const button_fullscreen = document.getElementById('button_fullscreen');
button_fullscreen.addEventListener('click', function(){
    console.log('click');
  toggleFullScreen();
});

*/





