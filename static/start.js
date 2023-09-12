
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

