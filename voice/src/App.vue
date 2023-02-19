<template>
  <div>
    <div v-for="file in audioFiles" :key="file.name">
      <label>
        <input type="checkbox" v-model="file.selected">
        <button @click="selectFile(file)">{{ file.name }}</button>
        <audio :src="file.url" controls></audio>
      </label>
    </div>
    <button @click="startRecording">Record</button>
    <button @click="stopRecording">Stop</button>
    <audio ref="audioPlayer" controls></audio>
    <input type="file" @change="selectFile">
    <button @click="sendSelectedFiles">Send Selected Files</button>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  data() {
  return {
    recorder: null,
    recordedChunks: [],
    audioFile: null,
    audioFiles: [], // new data property
    arrayBuffer:null
    }
  },
  methods: {
    async startRecording() {
      const constraints = { audio: true };
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.recorder = new MediaRecorder(stream);
        this.recorder.start();
        this.recordedChunks = [];

        this.recorder.addEventListener("dataavailable", (event) => {
          if (event.data.size > 0) {
            this.recordedChunks.push(event.data);
          }
        });

        this.recorder.addEventListener("stop", async () => {
          const blob = new Blob(this.recordedChunks);
          
          const url = URL.createObjectURL(blob);
          const fileType = blob.type;
          const arrayBuffer =await  blob.arrayBuffer();
          this.arrayBuffer = arrayBuffer
          // console.log('arrayBuffer',arrayBuffer)
          const file = new File([arrayBuffer], "recording.wav", { type: fileType });
          const newFile = {
            name: "recording.wav",
            type: "audio/wav",
            url: url,
            blob: file,
          };
          console.log('newFile',newFile)
          const arr =await newFile.blob.arrayBuffer();
          console.log('bufferok',arr)
          this.audioFiles.push(newFile);
        });
      } catch (err) {
        console.error("Error starting recording: ", err);
      }
    },
    // selectFile(file) {
    //   this.audioFile = file.blob;
    //   this.$refs.audioPlayer.src = file.url;
    // },
    stopRecording() {
    this.recorder.stop();
    console.log('recordedChunks',this.recordedChunks)
  
    },
    selectFile(event) {
    const files = event.target.files;
    if (files.length > 0) {
      this.audioFile = files[0];
      this.$refs.audioPlayer.src = URL.createObjectURL(this.audioFile);
      const newFile = {
        name: this.audioFile.name,
        type: this.audioFile.type,
        url: URL.createObjectURL(this.audioFile),
        blob: this.audioFile,
        selected: false, // new property
      };
      console.log('newFile',newFile)
      this.audioFiles.push(newFile);
    }
  },
  async sendSelectedFiles() {
    console.log('this.arrayBuffer',this.arrayBuffer)
    const selectedFiles = this.audioFiles.filter((file) => file.selected);
    console.log('here',selectedFiles)
    if (selectedFiles.length > 0) {
      
        
          // const buffer = new Int16Array(reader.result);
        
        // const blob = new Blob([buffer], { type: "audio/wav" });
        // const formData = new FormData();

        const fileType =await selectedFiles[0].blob.type;
        console.log('fileType',fileType)
        const arrayBuffer =await  selectedFiles[0].blob.arrayBuffer();
        console.log('buffer',arrayBuffer)
        const file = new File([arrayBuffer], 'audio.wav', { type: 'audio/wav' });
        // formData.append("file", blob, file.name);
        const formData = new FormData();
        // const file = new File([this.arrayBuffer], 'audio.wav', { type: 'audio/wav' });
        // console.log(file)
        // formData.append('file', file);
        axios.post("http://localhost:3000/predictTest", formData,{
        headers: {
          "Content-Type": "multipart/form-data",
        }}
        )
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.error(error);
          });
     
    }
  },
  },
    // async sendFile() {
    //   console.log('ok')
    //   if (!this.audioFile) return;
    //   console.log(this.audioFile)
    //   const formData = new FormData();
    //   formData.append("file", this.audioFile);

    //   try {
    //     const response = await axios.post("http://localhost:3000/predictTest", formData);
    //     console.log(response.data);
    //   } catch (error) {
    //     console.error(error);
    //   }
    // },
  // },
};
</script>

<!-- 
<script>
import axios from 'axios';

export default {
  data() {
    return {
      stream: null,
      recorder: null,
      chunks: [],
      recordingStopped: false,
      fileSelected: false,
      file: null,
    };
  },
  methods: {
    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        this.stream = stream;
        this.recorder = new MediaRecorder(stream);
        this.recorder.start();

        this.recorder.addEventListener("dataavailable", event => {
          this.chunks.push(event.data);
        });

        this.recorder.addEventListener("stop", () => {
          this.recordingStopped = true;
        });
      });
    },
    stopRecording() {
      this.recorder.stop();
      this.stream.getTracks().forEach(track => track.stop());
    },
    sendAudio() {
      let formData;
      if (this.fileSelected) {
        formData = new FormData();
        formData.append("file", this.file);
      } else {
        const blob = new Blob(this.chunks, { type: "audio/wav" });
        const file = new File([blob], "audio.wav", { type: "audio/wav" });

        formData = new FormData();
        formData.append("file", file);
      }

      axios
        .post("http://localhost:3000/predictTest", formData)
        .then(response => console.log(response))
        .catch(error => console.error(error));
    },
    uploadFile() {
      this.file = this.$refs.fileInput.files[0];
      this.fileSelected = true;
    },
  },
};
</script> -->
