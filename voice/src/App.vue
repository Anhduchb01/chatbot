<template>
  <div>
    <button @click="startRecording">Start Recording</button>
    <button @click="stopRecording">Stop Recording</button>
    <br>
    <input type="file" ref="audioFileInput" @change="uploadFile"/>
    <br>
    <button @click="sendData">Send to API</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      stream: null,
      recorder: null,
      audioBlob: null,
      audioFile: null
    }
  },
  methods: {
    startRecording() {
      // Initialize the Web Audio API
       navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          this.stream = stream;
  
          // Create a MediaRecorder to record the audio
          this.recorder = new MediaRecorder(stream);
  
          // Start recording
          this.recorder.start();
  
          // Create a new Blob to hold the recorded audio
          this.recorder.ondataavailable = (e) => {
            this.audioBlob = new Blob([e.data], { type: 'audio/webm' });
          };
        })
        .catch(console.error);
    },
    stopRecording() {
      // Stop recording
      this.recorder.stop();
      console.log(this.audioBlob)
  
      // Stop the audio stream
      this.stream.getTracks().forEach((track) => track.stop());
    },
    uploadFile() {
      // get the selected file
      this.audioFile = this.$refs.audioFileInput.files[0];
    },
    sendData() {
      if (this.audioBlob === null && this.audioFile === null) {
        console.log("No audio to send")
        return;
      }
      let formData;
      if (this.audioBlob) {
        // Create a new FormData object to hold the audio file
        formData = new FormData();
        formData.append('audio_file', this.audioBlob);
      } else if (this.audioFile) {
        formData = new FormData();
        formData.append('audio_file', this.audioFile);
      }
      console.log(formData);
  
      // Send the audio file to the Flask API
      axios.post('http://127.0.0.1:5000/embed', formData)
        .then((response) => {
          console.log(response.data);
        })
        .catch(console.error);
    }
  }
}
</script>