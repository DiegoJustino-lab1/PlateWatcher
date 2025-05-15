const videoElement = document.getElementById('video');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const resultElement = document.getElementById('result');

let mediaStream = null;

async function startVideo() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = mediaStream;
        videoElement.play();
    } catch (error) {
        console.error('Error accessing the camera: ', error);
    }
}

function stopVideo() {
    if (mediaStream) {
        const tracks = mediaStream.getTracks();
        tracks.forEach(track => track.stop());
        videoElement.srcObject = null;
    }
}

async function captureImage() {
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    const response = await fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    });

    const result = await response.json();
    displayResult(result);
}

function displayResult(result) {
    if (result.success) {
        resultElement.textContent = `Texto detectado: ${result.text}`;
    } else {
        resultElement.textContent = 'Nenhuma placa detectada.';
    }
}

startButton.addEventListener('click', startVideo);
stopButton.addEventListener('click', stopVideo);
videoElement.addEventListener('click', captureImage);