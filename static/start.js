var socket = io.connect(window.location.protocol + '//' + window.location.host);

socket.on('connect', function () {
  console.log("Connected...!", socket.connected);
});


function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else if (document.exitFullscreen) {
    document.exitFullscreen();
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

