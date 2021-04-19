<template>
<div>
  <el-button class="button" type="primary" @click="confirmUploadFile" :loading="false" :disabled="isDisable">确认上传</el-button>
  <el-button class="button copyBtn" type="primary" :loading="false" @click="copyLink" :disabled="disableCopy">复制BT链接</el-button>
  <el-progress v-if="percent !== 0" :percentage="percent" :status="barStatus" />
  <span v-if="isDisplayBT === true" type="success">您生成的下载链接为:{{ cutURL }}</span>
</div>
</template>

<script>
import Clipboard from 'clipboard'
import { Encrypt } from '@/backend-api/fileEncrypt'
import { getUrl } from '@/backend-api/getFileUrl'
import { hashcode } from '@/backend-api/sha256'
import { roundingError } from '@/config'
export default {
  data () {
    return {
      MaxDownloadAccount: 1,
      startTime: {},
      endTime: {},
      password: '',
      fileList: [],
      percent: 0,
      fileURL: '',
      fileName: '',
      barStatus: 'exception',
      isDisplayBT: false,
      isDisable: false,
      disableCopy: true,
      isEncrypt: false
    }
  },
  computed: {
    cutURL: function () {
      return this.fileURL.split('').slice(0, 13).join('') + '...'
    }
  },
  mounted () {
    this.startTime = new Date()
    this.endTime = new Date()
  },
  methods: {
    async store () {
      let nameData = ''
      for (let i = 0; i < this.fileList.length; i++) {
        nameData = nameData + this.fileList[i].name
      }
      this.fileURL = getUrl(nameData)
      const url = hashcode(this.fileURL)
      const filePassword = hashcode(this.password)
      const fileShare = this.$gun.get('fileShare-gunSend')
      const shareContent = {
        startTime: this.startTime.toString(),
        endTime: this.endTime.toString(),
        password: filePassword,
        MaxDownloadAccount: this.MaxDownloadAccount,
        currentDownloadAccount: 0,
        fileName: this.fileName,
        fileNumber: this.fileList.length
      }
      const bytesPerPiece = 1024 * 1024
      let totalSize = 0
      for (let i = 0; i < this.fileList.length; i++) {
        totalSize = totalSize + this.fileList[i].size
      }
      let currentSize = 0
      await (async () => {
        for (let i = 0; i < this.fileList.length; i++) {
          await (async () => {
            const myFileIndex = 'myfile' + i
            let start = 0
            let end
            let index = 0
            const filesize = this.fileList[i].size
            shareContent[myFileIndex + 'name'] = this.fileList[i].name
            shareContent[myFileIndex + 'percent'] = this.fileList[i].size / totalSize * 100
            shareContent[myFileIndex + 'type'] = this.fileList[i].type
            while (start < filesize) {
              end = start + bytesPerPiece
              if (end > filesize) {
                end = filesize
              }
              const piece = this.fileList[i].slice(start, end)
              const encryptFile = Encrypt(piece)
              currentSize = currentSize + piece.size
              const currentPercent = currentSize / totalSize * 100
              await encryptFile.then(result => {
                const fileIndex = 'file' + index
                shareContent[myFileIndex + fileIndex] = result
                const percentIndex = 'percent' + index
                shareContent[myFileIndex + percentIndex] = piece.size / totalSize * 100
                this.percent = parseInt(currentPercent)
                if ((this.percent === 100) || (Math.abs(currentPercent - 100) < roundingError)) {
                  this.percent = 100
                }
                index++
                start = end
              })
            }
            shareContent[myFileIndex + 'pieceNumber'] = index
          })()
        }
      })()
      fileShare.get(url).put(shareContent)
      fileShare.get(url).once(
        et => {
          this.barStatus = 'success'
          this.isDisplayBT = true
          this.disableCopy = false
        }
      )
      fileShare.get(url).on(
        (data) => { }
      )
      this.$gun.get('fileShare-gunSend').get(url).once(
        oneShare => { }
      )
    },
    async confirmUploadFile () {
      if (this.fileList.length === 0) {
        this.$message({
          type: 'warning',
          message: '请选择您需要上传的文件'
        })
        return
      }
      if (this.fileName === '') {
        this.$message({
          type: 'warning',
          message: '请为您这次上传的文件集命名'
        })
        return
      }
      if (this.password === '' && this.isEncrypt === true) {
        this.$message({
          type: 'warning',
          message: '请设置您的密码'
        })
        return
      }
      if (this.startTime === {} || this.endTime === {} || this.startTime >= this.endTime) {
        this.$message({
          type: 'warning',
          message: '请您输入正确的时间格式'
        })
        return
      }
      const todayTime = new Date(new Date().setHours(0, 0, 0, 0))
      if (this.startTime < todayTime || this.endTime <= new Date().getTime()) {
        this.$message({
          type: 'warning',
          message: '生失效时间应至少久于当前'
        })
        return
      }
      this.$confirm('此操作将上传该文件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(async () => {
        this.$message({
          type: 'success',
          message: '上传开始!'
        })
        this.$bus.emit('ForbidModifyUploadSetting')
        await this.store()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消上传'
        })
      })
    },
    copyLink () {
      const displayFileURL = this.fileURL
      const clipboard = new Clipboard('.copyBtn', {
        text: function () {
          return displayFileURL
        }
      })
      clipboard.on('success', e => {
        this.$message({ message: '复制成功', showClose: true, type: 'success' })
        clipboard.destroy()
      })
      clipboard.on('error', e => {
        this.$message({ message: '复制失败,', showClose: true, type: 'error' })
        clipboard.destroy()
      })
    }
  },
  created () {
    this.$bus.on('getPassword', (password) => {
      this.password = password
    })
    this.$bus.on('getFiles', (fileList) => {
      this.fileList = fileList
    })
    this.$bus.on('getMaxNum', (maxNumber) => {
      this.MaxDownloadAccount = maxNumber
    })
    this.$bus.on('getStartTime', (startTime) => {
      this.startTime = startTime
    })
    this.$bus.on('getEndTime', (endTime) => {
      this.endTime = endTime
    })
    this.$bus.on('getFileName', (fileName) => {
      this.fileName = fileName
    })
    this.$bus.on('ForbidModifyUploadSetting', () => {
      this.isDisable = true
    })
    this.$bus.on('getEncryptChoice', (isEncrypt) => {
      this.isEncrypt = isEncrypt
    })
  }
}
</script>

<style lang="scss" scoped>
.button {
  width: 120px;
}
span {
  font-size: 15px;
}
</style>
