<template>
<div id="container">
  <goback-home id="gobackhome"></goback-home>
  <div id="card" v-show="isPreview === false">
    <div id="aside">
      <el-form label-width="80px" :label-position="'left'">
        <div v-show="isPreview === false" class="flex-layout">
          <div class="chooseFile">
            <uploader-chooser id="uploadfile"></uploader-chooser>
            <div class="innerBox">
              <div class="chooseDownloadAccount" id="com2">
                <max-account-chooser></max-account-chooser>
              </div>
              <div class="chooseDueTime" id="com3">
                <due-time-chooser></due-time-chooser>
              </div>
              <div class="chooseEncryption" id="com4">
                <encryption-chooser></encryption-chooser>
              </div>
              <div class="chooseConfirm" id="com5">
                <final-confirm></final-confirm>
              </div>
            </div>
          </div>
        </div>
      </el-form>
    </div>
    <div id="list" v-show="isPreview === false">
      <div class="tableHeader">已添加文件</div>
      <show-file-list></show-file-list>
    </div>
  </div>
  <div v-show="isPreview === true">
    <preview-page></preview-page>
  </div>
</div>
</template>

<script>
import PreviewPage from './Preview.vue'
import GobackHome from './GobackHome.vue'
import UploaderChooser from './Upload/UploadChooser.vue'
import MaxAccountChooser from './Upload/MaxAccountChooser.vue'
import DueTimeChooser from './Upload/DueTimeChooser.vue'
import FinalConfirm from './Upload/FinalConfirm.vue'
import EncryptionChooser from './Upload/EncryptionChooser'
import ShowFileList from './Upload/ShowFileList'
export default {
  data () {
    return {
      isPreview: false
    }
  },
  methods: {
  },
  components: {
    UploaderChooser,
    MaxAccountChooser,
    DueTimeChooser,
    FinalConfirm,
    EncryptionChooser,
    GobackHome,
    PreviewPage,
    ShowFileList
  },
  created () {
    this.$bus.on('startPreview', () => {
      this.isPreview = true
    })
    this.$bus.on('closePreview', () => {
      this.isPreview = false
    })
  }
}
</script>

<style lang="scss" scoped>
#card {
  display: flex;
  width: 60%;
  height: 70%;
  margin: 0 auto;
  margin-top: 40px;
  padding: 0;
  background-color: #D8BFD8;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
  border-radius: 10px;
}
#container{
  position: fixed;
  background-image: url("../assets/Upload.jpg");
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  overflow: auto;
}
#gobackhome{
  margin-left: 0;
  width: 200px;
}
.chooseFile{
  color: white;
  width: 100%;
  height: 450px;
  border-color: transparent;
  border-width: 2px;
  border-style: solid;
}
#uploadfile {
  width: 90%;
  margin: 0 auto;
}
.chooseDueTime,.chooseEncryption{
  margin-top: 5px;
}
.innerBox {
  width: 90%;
  margin: 0 auto;
  > * {
    margin-top: 5px;
  }
}
#aside {
  width: 40%;
}
#list {
  width: 60%;
}
.tableHeader {
  border-bottom: 1px solid white;
  color: white;
  font-size: 20px;
  width: 90%;
  height: 50px;
  text-align: center;
  margin-top: 20px;
}
</style>
