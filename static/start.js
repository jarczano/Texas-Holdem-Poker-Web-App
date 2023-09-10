
//var testFunction = function test() {alert('hello world')};

/*
var testFunction = "export test";
export default  testFunction ;
*/

//socket = io.connect(window.location.protocol + '//' + window.location.host);
//var socket = io({ query: { sid: sessionID } });
//var socket = io({ query: { sid: 'jCECT1gk360a4nCvAAAC' } });
//var socket = io()
/*export default socket;
*/
//socket.emit('transfer_socket', socket)

//console.log("how looks socker", socket);

/*
socket.on('connect', function () {
  const sid = socket.id;
  //console.log("Connected...!", socket.connected);
  console.log("Client start. player id: ", sid);
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
*/
function toggleFullScreen() {
    const button = document.getElementById('button_fsc');
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        button.setAttribute('data-fullscreen', 'on');
        button.querySelector('img').src = '../static/image/exit_fullscreen_icon.svg';
    } else if (document.exitFullscreen) {
        document.exitFullscreen();
        button.setAttribute('data-fullscreen', 'off');
        button.querySelector('img').src = '../static/image/fullscreen_icon.svg';
    }
}




const button_fullscreen = document.getElementById('button_fullscreen');
const menu_frame = document.getElementById('menu_frame');
const play_container = document.getElementById('play-container')


const button_fsc = document.getElementById('button_fsc');

button_fsc.addEventListener('click', function(){
  toggleFullScreen();
  console.log("click");
});

button_fullscreen.addEventListener('click', function(){
  toggleFullScreen();
  console.log("click");
  /*button_fullscreen.style.display = 'none';*/
  play_container.style.display = 'none';
  menu_frame.style.display = 'flex';
  /*lock('landscape')*/
});

