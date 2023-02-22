<template>
  <div>
    <vue-record-audio @result="onResult"  />
    <div v-for="file in audioFiles" :key="file.name">
      <label>
        <input type="checkbox" v-model="file.selected">
        <button @click="selectFile(file)">{{ file.name }}</button>
        <audio :src="file.url" controls></audio>
      </label>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data(){
    return{
      audioFiles: [],
    }
  },
  
  methods: {
    async onResult (data) {
      console.log('The blob data:', data);
      console.log('Downloadable audio', window.URL.createObjectURL(data));
      // const fileType =data.type;
      // console.log('fileType',fileType)
      const arrayBuffer = await data.arrayBuffer();
      console.log('arrayBuffer',arrayBuffer)
      // console.log('buffer',arrayBuffer)
      // const file = new File([arrayBuffer], 'audio.wav', { type: 'audio/wav' });
      // const wavBlob = await audioBlobToWav(data);
      // console.log('wavBlob',wavBlob)

      const file = new File([arrayBuffer], 'audio.wav', {type: 'audio/wav'});
      const fileUrl = URL.createObjectURL(file);
      const newFile = {
            name: "audio.wav",
            type: "audio/wav",
            url: fileUrl,
            blob: file,
            selected: false, // new property
          };
      this.audioFiles.push(newFile)
      const formData = new FormData();
      formData.append('audio', data,'audio.wav');
      
      // formData.append("file", blob, file.name);
      
      // const file = new File([this.arrayBuffer], 'audio.wav', { type: 'audio/wav' });
      // console.log(file)
      // formData.append('file', file);
      axios.post("http://localhost:3000/predictTest", formData
      // ,{headers:
      //   {'Content-Type': 'application/octet-stream'}
      // }
     
      )
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  }

}
</script>
