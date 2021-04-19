<template>
<el-container id="background">
  <el-header>
    <goback-home id="gobackhome"></goback-home>
  </el-header>
  <el-main id="tempmain">
    <p id="name">Gun-Send</p>
    <div v-show="isPreview === false">
      <div class="InputDownloadLink">
        <input-download-link></input-download-link>
      </div>
      <div id="file">
        <file-list-show-and-preview></file-list-show-and-preview>
        <div class="DownloadOperation">
          <download-operation></download-operation>
        </div>
      </div>
    </div>
    <div v-show="isPreview === true">
      <preview-page></preview-page>
    </div>
  </el-main>
</el-container>
</template>

<script>
import PreviewPage from './Preview.vue'
import GobackHome from './GobackHome.vue'
import InputDownloadLink from './Download/InputDownloadLink'
import FileListShowAndPreview from './Download/FileListShowAndPreview'
import DownloadOperation from './Download/DownloadOperation'
export default {
  data () {
    return {
      isPreview: false
    }
  },
  components: {
    InputDownloadLink,
    FileListShowAndPreview,
    DownloadOperation,
    GobackHome,
    PreviewPage
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
#background {
  position: fixed;
  background-image: url("../assets/Download.jpg");
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  overflow:auto;
}
#gobackhome {
  margin: 0;
  margin-top: 2px;
  width: 200px;
}
#name {
  font-size: 5rem;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  color: white;
  text-align: center;
  margin: 0;
}
#file {
  color: white;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  width: 800px;
  height: 400px;
  margin: 0 auto;
}
.InputDownloadLink {
  margin: 0 auto;
  width: 400px;
}
.FileListShowAndPreView {
  width: 800px;
  height: 400px;
}
.DownloadOperation {
  width: 400px;
  margin: 0 auto;
  margin-top: 20px;
}
.el-header {
  padding: 0;
  padding-left: 2px;
}
</style>
