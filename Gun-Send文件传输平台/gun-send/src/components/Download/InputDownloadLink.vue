<template>
<div class="inputLink" v-show="BeforeRightPassword">
  <div class="downloadinput" v-show="(isConfirmAnalysis === false || isEncrypt === false) && BeforeRightPassword">
    <el-input placeholder="请输入您的种子链接" v-model="BTlink"></el-input>
    <el-button id="analysbutton" size="mini" type="primary" @click.native="startAnalysis">确定</el-button><br>
  </div>
  <div class="downloadinput">
    <el-input v-model="inputPassword" v-show="isConfirmAnalysis === true && isEncrypt === true" placeholder="请输入您的密码"></el-input>
    <el-button id="passwordbutton" size="mini" type="primary" @click.native="passwordConfirm" v-show="isConfirmAnalysis === true && isEncrypt === true">确定</el-button>
    <el-progress class="downloadBar" v-if="currentPercent !== 0" :percentage="currentPercent" :status="barStatus" />
  </div>
</div>
</template>

<script>
import { hashcode } from '@/backend-api/sha256'
import { checkIfRetained } from '@/backend-api/fileDestroy'
import { encryptAndCheck } from '@/backend-api/encryptAndCheck'
import { Decrypt } from '@/backend-api/fileEncrypt'
import {
  errorMax,
  roundingError
} from '@/config'
export default {
  data () {
    return {
      BeforeRightPassword: true,
      BTlink: '',
      isConfirmAnalysis: false,
      isEncrypt: false,
      password: '',
      inputPassword: '',
      errorCount: 0,
      fileList: [],
      fileNumber: 0,
      fileName: '',
      currentPercent: 0,
      barStatus: 'exception',
      analysisLinkError: ''
    }
  },
  mounted () {
    this.$gun.get('fileShare-gunSend').once().map().once(
      oneShare => { }
    )
  },
  methods: {
    async startAnalysis () {
      this.isConfirmAnalysis = await this.BTConfirm()
      if (!this.isEncrypt) {
        this.passwordConfirm()
      }
    },
    async BTConfirm () {
      const resultSearchAndCheckBT = await this.SearchAndCheckBT()
      if (resultSearchAndCheckBT === true) {
        return true
      } else {
        this.BTlink = ''
        this.$alert(this.analysisLinkError, '提示', {
          confirmButtonText: '确定',
          type: 'warning',
          center: true
        })
        return false
      }
    },
    async SearchAndCheckBT () {
      this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink)).get('password').once(
        password => {
          this.password = password
        }
      )
      this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink)).get('fileNumber').once(
        number => {
          this.fileNumber = number
        }
      )
      this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink)).get('fileName').once(
        name => {
          this.fileName = name
        }
      )
      let checkResult
      if (!this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink))) {
        this.analysisLinkError = '该链接地址无效'
        return false
      } else {
        checkResult = await (async () => {
          this.analysisLinkError = await checkIfRetained(this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink)))
          if (this.analysisLinkError === '') {
            if (this.password === hashcode('')) {
              this.isEncrypt = false
            } else {
              this.isEncrypt = true
            }
            return true
          } else {
            return false
          }
        })()
        return checkResult
      }
    },
    async passwordConfirm () {
      if (encryptAndCheck(this.inputPassword, this.password)) {
        const gunLink = this.$gun.get('fileShare-gunSend').get(hashcode(this.BTlink))
        await (async () => {
          for (let i = 0; i < this.fileNumber; i++) {
            await (async () => {
              const pieceList = []
              const myFileIndex = 'myfile' + i
              let pieceNumber
              gunLink.get(myFileIndex + 'pieceNumber').once(
                number => {
                  pieceNumber = number
                }
              )
              let fileType
              gunLink.get(myFileIndex + 'type').once(
                type => {
                  fileType = type
                }
              )
              let fileName
              gunLink.get(myFileIndex + 'name').once(
                name => {
                  fileName = name
                }
              )
              for (let j = 0; j < pieceNumber; j++) {
                const fileIndex = 'file' + j
                let pieceCode
                gunLink.get(myFileIndex + fileIndex).once(
                  code => {
                    pieceCode = code
                  }
                )
                const piece = await Decrypt(pieceCode)
                const percentIndex = 'percent' + j
                let piecePercent
                gunLink.get(myFileIndex + percentIndex).once(
                  percent => {
                    piecePercent = percent
                  }
                )
                this.currentPercent = this.currentPercent + piecePercent
                pieceList[j] = piece
                if (parseInt(this.currentPercent) === 100 ||
                  (Math.abs(this.currentPercent - 100) < roundingError)) {
                  this.currentPercent = 100
                  this.barStatus = 'success'
                  setTimeout(() => {
                    this.BeforeRightPassword = false
                    this.$bus.emit('SendFileMessage', this.fileList, this.fileName, gunLink)
                    this.$bus.emit('canChooseDownloadMode', 'send')
                  }, 1500)
                }
              }
              this.fileList[i] = new File(pieceList, fileName, { type: fileType })
            })()
          }
        })()
        if (this.isEncrypt) {
          this.$message({
            message: '密码输入正确！',
            type: 'success'
          })
        }
      } else {
        this.errorCount++
        this.inputPassword = ''
        if (this.errorCount >= errorMax) {
          this.$alert('您的输入错误次数已达上限', '警告', {
            confirmButtonText: '确定',
            type: 'warning',
            center: true
          }).then(() => {
            this.$router.push({ name: 'Home' })
          })
          return
        }
        if (this.isEncrypt) {
          this.$alert('密码错误，请您重新输入密码', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            center: true
          })
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.inputLink {
  margin: 50px auto;
  background-color: #F08080;
  width: 400px;
  border-color: transparent;
  border-width: 2px;
  border-style: solid;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
  border-radius: 10px;
}
.downloadinput {
  margin: 20px auto 20px;
  width: 300px;
}
.downloadBar {
  margin: 0 auto;
}
#analysbutton,#passwordbutton {
  margin: 8px auto 0;
}
</style>
