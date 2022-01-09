<template>
<div v-show="canChooseDownloadMode">
  <a><el-button id="download" type="primary" @click.native="startDownload" v-show="canChooseDownloadMode">下载</el-button></a>
</div>
</template>

<script type="text/javascript" src="jszip/jszip.min.js"></script>
<script type="text/javascript" src="js/jszip.js"></script>
<script type="text/javascript" src="jszip/FileSaver.js"></script>><!--用于文件下载-->
<script>
import JSZip from 'jszip'
export default {
  data () {
    return {
      canChooseDownloadMode: false,
      fileList: [],
      gunLink: {},
      fileName: ''
    }
  },
  methods: {
    async startDownload () {
      // 在这里相应点击下载按钮后的操作
      let currentDownloadAccount
      await this.gunLink.get('currentDownloadAccount').once(
        currentAccount => {
          currentDownloadAccount = currentAccount
        }
      )
      this.gunLink.get('currentDownloadAccount').put(
        currentDownloadAccount + 1
      )
      this.gunLink.get('currentDownloadAccount').once(
        currentAccount => {
          console.log(currentAccount)
        }
      )
      setTimeout(() => {
        this.$bus.emit('DisplayComment')
      }, 1500);
      let zip = new JSZip()
      this.fileList.forEach(function (obj) {
        zip.file(obj.name, obj)
      })
      let result = {}
      zip.generateAsync({
        type: 'blob'
      }).then((content) => {
        // 下载的文件名
        var filename = this.fileName
        result = content
        // 创建隐藏的可下载链接
        var eleLink = document.createElement('a')
        eleLink.download = filename
        eleLink.style.display = 'none'
        // 下载内容转变成blob地址
        eleLink.href = URL.createObjectURL(content)
        // 触发点击
        document.body.appendChild(eleLink)
        eleLink.click()
        // 然后移除
        document.body.removeChild(eleLink)
      })
    }
  },
  created () {
    this.$bus.on('canChooseDownloadMode', () => {
      this.canChooseDownloadMode = true
    })
    this.$bus.on('SendFileMessage', (fileList, fileName, gunLink) => {
      this.fileList = fileList
      this.fileName = fileName
      this.gunLink = gunLink
    })
  }
}
</script>

<style>
#download {
  display: block;
  width: 100px;
  margin: 0 auto;
}
</style>
