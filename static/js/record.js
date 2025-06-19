// static/js/record.js
let mediaRecorder;
let recordedChunks = [];

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
  .then(stream => {
    document.getElementById("preview").srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const formData = new FormData();
      formData.append('video', blob, 'recording.webm');

      fetch('/save-video', {
        method: 'POST',
        body: formData
      })
        .then(response => response.text())
        .then(data => alert(data))
        .catch(error => console.error('Error:', error));
    };

    document.getElementById("startBtn").onclick = () => {
      recordedChunks = [];
      mediaRecorder.start();
    };

    document.getElementById("stopBtn").onclick = () => {
      mediaRecorder.stop();
    };
  })
  .catch(error => console.error('getUserMedia error:', error));
