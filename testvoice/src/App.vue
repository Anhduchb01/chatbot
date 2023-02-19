<template>
  <div>
    <button @click="startRecording">Start Recording</button>
    <button @click="stopRecording">Stop Recording</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      mediaRecorder: null,
      audioChunks: [],
      audioURL: null
    };
  },
  methods: {
    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          this.mediaRecorder = new MediaRecorder(stream);
          this.mediaRecorder.addEventListener("dataavailable", (event) => {
            this.audioChunks.push(event.data);
          });
          this.mediaRecorder.start();
        });
    },
    stopRecording() {
      this.mediaRecorder.stop();
      this.mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        this.audioURL = URL.createObjectURL(audioBlob);
        this.sendAudioFile(audioBlob);
      });
    },
    async sendAudioFile(audioBlob) {
      const formData = new FormData();
      formData.append('file', audioBlob);
      try {
        const response = await axios.post('http://localhost:3000/predictTest', formData);
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>
