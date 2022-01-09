<template>
<div class="container">
  <div id="pdfPreview" v-show="PreviewType === 1">
    <pdf-preview class="pdf" v-show="txtType === 'pdf'"></pdf-preview>
    <iframe :src="txtSrc" v-show="txtType === 'txt'">
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=gb2312"/>
      </head>
    </iframe>
  </div>
  <img class="img" :src="ImgSrc" alt="图片预览" v-show="PreviewType === 2" height="400vh"/>
  <video :src="VideoSrc" preload="auto" controls="controls" id="myVideo"
    height="100%" width="600px" v-show="PreviewType === 3"></video>
  <audio :src="AudioSrc" preload="auto" controls="controls" id="myAudio"
    height="100%" width="600px" v-show="PreviewType === 4"></audio>
  <div v-show="PreviewType == 5">抱歉，不支持此类文件的预览！</div>
  <div>
    <el-button class="returnBtn" type="primary" @click.native="returnToFileUpload">返回</el-button>
  </div>
</div>
</template>

<script>
import PdfPreview from './Preview/PDF-Preview.vue'
export default {
  data () {
    return {
      PreviewFile: {},
      PreviewName: '',
      txtSrc: '',
      ImgSrc: '',
      VideoSrc: '',
      AudioSrc: '',
      PreviewType: 0,
      txtType: ''
    }
  },
  methods: {
    returnToFileUpload () {
      this.$bus.emit('closePreview', 'send')
      const video = document.getElementById('myVideo')
      video.pause()
      const audio = document.getElementById('myAudio')
      audio.pause()
    }
  },
  created () {
    this.$bus.on('PreviewFile', (PreviewFile) => {
      this.PreviewName = PreviewFile.name
      this.PreviewFile = PreviewFile
      const Fname = this.PreviewName
      const Ftype = Fname.substring(Fname.lastIndexOf('.')).toLowerCase()
      if (Ftype === '.txt' || Ftype === '.pdf' || Ftype === '.md' ||
      Ftype === '.html' || Ftype === '.js' || Ftype === '.css' || Ftype === '.vue') {
        this.txtSrc = URL.createObjectURL(this.PreviewFile)
        this.PreviewType = 1
        if (Ftype === '.pdf') {
          this.$bus.emit('startPdfPreview', this.txtSrc)
          this.txtType = 'pdf'
        } else {
          this.txtType = 'txt'
        }
      } else if (Ftype === '.jpg' || Ftype === '.jpeg' || Ftype === '.png' || Ftype === '.bmp' ||
      Ftype === '.gif' || Ftype === '.tiff' || Ftype === '.psd' || Ftype === '.svg' || Ftype === '.pcx') {
        this.ImgSrc = URL.createObjectURL(this.PreviewFile)
        this.PreviewType = 2
      } else if (Ftype === '.avi' || Ftype === '.wmv' || Ftype === '.mpg' || Ftype === '.mpeg' || Ftype === '.mp4' ||
      Ftype === '.mov' || Ftype === '.rmvb' || Ftype === '.rm' || Ftype === '.ram' || Ftype === '.swf' || Ftype === '.flv') {
        this.VideoSrc = URL.createObjectURL(this.PreviewFile)
        this.PreviewType = 3
      } else if (Ftype === '.mp3' || Ftype === '.wav' || Ftype === '.ogg' || Ftype === '.fla' || Ftype === 'wma') {
        this.AudioSrc = URL.createObjectURL(this.PreviewFile)
        this.PreviewType = 4
      } else {
        this.PreviewType = 5
      }
    })
  },
  components: {
    PdfPreview
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.container > * {
  display: block;
  margin: 0 auto;
}
.el-button {
  display: block;
}
.returnBtn {
  margin-top: 20px;
}
#pdfPreview {
  margin: 0 auto;
  width: 100%;
}
iframe {
  background-color: white;
  height: 60vh;
  width: 60%;
  display: block;
  margin: 0 auto;
}
.pdf {
  width: 60%;
  display: block;
  margin: 0 auto;
}
</style>
