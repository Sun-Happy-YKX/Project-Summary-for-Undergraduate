<template>
<div class="container">
  <div class="add-file-right">
    <el-form-item label="文件选择">
      <input type="file" name="file" id="fileElem" ref="clearFile" @change="getFile($event)" multiple="multiplt"
        class="add-file-right-input" :disabled="isDisable ? 'disabled' : false" style="width:150px;;margin-left:10px;"
        accept="CanUploadFileTypes">
        <label id="file-lable" for="fileElem">点击以添加文件</label>
    </el-form-item>
  </div>
  <el-form-item label="文件名称">
  <el-col :span="11">
    <el-input v-model="FileName" placeholder="请输入文件名称" id="filenameinput" style="width:150px;margin-left:10px;"
    @change="changeHandler" :disabled="isDisable ? 'disabled' : false" size="small"></el-input>
  </el-col>
  </el-form-item>
</div>
</template>

<script src="js/jquery.js"></script>
<script>
import DownloadButton from '../Download/DownloadOperation.vue'
export default {
  data () {
    return {
      tipText: '文本文件推荐上传.pdf格式；视频文件推荐上传.mp4格式；音频文件推荐上传.mp3格式；图片文件推荐上传.png,.png格式；',
      CanUploadFileTypes: [
        '.docx', '.doc', '.pdf', '.txt', '.html', '.css', '.js',
        '.vue', '.rtf', '.xls', '.ppt', '.xlsx', '.md',
        '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.psd', '.svg', '.pcx',
        '.mp3', '.wav', '.ogg', '.fla', '.wma',
        '.avi', '.mp4', '.wmv', '.mpg', '.mpeg', '.mov', '.rmvb', '.rm', '.ram', '.swf', '.flv'
      ],
      isDisable: false,
      formData: new FormData(),
      FileName: '',
      addArr: [],
      FileURL: ''
    }
  },
  components: {
    DownloadButton
  },
  methods: {
    getFile (event) {
      var file = event.target.files
      for(var i = 0;i<file.length;i++) {
        // 上传类型要判断
        this.addArr.push(file[i])
      }
      this.$bus.emit('getFiles', this.addArr)
    },
    changeHandler () {
      this.$bus.emit('getFileName', this.FileName)
    }
  },
  created () {
    this.$bus.on('ForbidModifyUploadSetting', () => {
      this.isDisable = true
    })
  }
}
</script>

<style lang="scss" scoped>
.container {
  font-size: 20px;
  > * {
    margin-top: 20px;
  }
}
.add-file-right {
  height:50px;
  margin-top:15px;
}
.add-file-right-more {
  font-size: 10px;
}
.dialog-footer {
  margin:auto auto 0 0;
}
.add-file-right-more {
  margin-left: 0;
}
.add-file-right-input {
  margin-left: 0;
  margin-top: 20px;
}
.add-file-right-input {
  position: absolute !important;
  height: 1px;
  width: 1px;
  overflow: hidden;
  clip: rect(1px, 1px, 1px, 1px);
}
input.add-file-right-input + label {
  cursor: pointer;
}
#file-lable {
  color: #fff;
  font-size: 15px;
  letter-spacing: 1.5px;
  margin-left: 13px;
}
</style>
