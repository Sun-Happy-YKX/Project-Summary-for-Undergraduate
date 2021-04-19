<template>
<div v-show="canChooseDownloadMode === true" class="container">
  <div v-show="isDisplayFiles">
    <div class="card">
      <div id="filelist">
        <el-scrollbar class="scroll-bar">
          <ul>

            <li v-for="(item, index) in fileList" :key='index'>
              <p title="点击预览" id="item" @click="clickToPreview(item)"><i class="el-icon-document"></i> {{ cutFileName(item.name) }}</p>
            </li>
          </ul>
        </el-scrollbar>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      canChooseDownloadMode: false,
      isDisplayFiles: false,
      fileList: [],
      fileName: '',
      btnText: '显示文件列表'
    }
  },
  created () {
    this.$bus.on('canChooseDownloadMode', () => {
      this.canChooseDownloadMode = true
      this.isDisplayFiles = true
    })
    this.$bus.on('SendFileMessage', (fileList, fileName) => {
      this.fileList = fileList
      this.fileName = fileName
    })
  },
  methods: {
    clickToPreview (PreviewFile) {
      this.$bus.emit('PreviewFile', PreviewFile)
      this.$bus.emit('startPreview')
    },
    cutFileName (fileName) {
      let name = fileName
      let strlen = 0
      for (let i = 0; i < name.length; i++) {
        if (name.charCodeAt(i) > 255) {
          strlen += 2
        } else {
          strlen++
        }
      }
      if (strlen >= 30) {
        let count = 0
        for (let i = 0; i < 30; i++) {
          if (name.charCodeAt(i) <= 255) {
            count++
          }
        }
        name = name.substr(0, 15 + count * 0.5)
        if (name.length !== fileName.length) {
          name = name + '...'
        }
      }
      return name
    }
  }
}
</script>

<style scoped>
.card {
  width: 80%;
  height: 300px;
  margin: 0 auto;
  background-color: #F08080;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
  border-radius: 10px;
}
.container {
  width: 100%;
  height: 300px;
}
#test {
  color: black;
  height: 40px;
}
#filelist {
  height: 250px;
  width: 100%;
}
#item {
  background-color: rgba(255,255,255,0.5);
  width: 400px;
  height: 30px;
  border-radius: 15px;
  line-height: 30px;
  text-indent: 1em;
  color: #606266;
  margin-left: 70px;
}
ul {
  list-style: none;
}
#mytitle {
  position: absolute;
  color: #ffffff;
  max-width: 160px;
  font-size: 14px;
  padding: 4px;
  background: rgba(40, 40, 40, 0.8);
  border: solid 1px #e9f7f6;
  border-radius:5px;
}
</style>
<style>
.el-scrollbar {
  height: 100%;
}
.el-scrollbar__wrap {
  overflow-x: hidden;
}
#item:hover {
  cursor: pointer;
  transform: scale(1.2,1.1);
  -webkit-transform: scale(1.2,1.1);
  -moz-transform: scale(1.2,1.1);
  -o-transform: scale(1.2,1.1);
  -ms-transform: scale(1.2,1.1);
}
</style>
