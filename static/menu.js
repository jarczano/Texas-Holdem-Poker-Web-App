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
     window.location.href = "/play/";
}

function playWithAI() {
     window.location.href = "/play/";
    }

