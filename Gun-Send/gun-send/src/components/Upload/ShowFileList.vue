<template>
  <div class="add-file-list">
    <el-scrollbar style="height:100%; width: 100%">
      <ul>
        <li v-for="(item, index) in addArr" :key="index">
          <div title="点击预览" id="file-list-item">
            <div id="file-icon"><i class="el-icon-document"></i></div>
            <div id="file-name" @click="clickToPreview(item)">{{ cutFileName(item.name) }}</div>
            <div id='close-icon' title="点击删除"><i class="el-icon-close" @click="deleteFile(index)"></i></div>
          </div>
        </li>
      </ul>
    </el-scrollbar>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      addArr: [],
      isDisable: false,
      tipText: ''
    }
  },
  methods: {
    deleteFile (certainIndex) {
      this.addArr.splice(certainIndex, 1)
    },
    clickToPreview (certainFile) {
      this.$bus.emit('PreviewFile', certainFile)
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
      if (strlen >= 40) {
        let count = 0
        for (let i = 0; i < 40; i++) {
          if (name.charCodeAt(i) <= 255) {
            count++
          }
        }
        name = name.substr(0, 20 + count * 0.5)
        if (name.length !== fileName.length) {
          name = name + '...'
        }
      }
      return name
    }
  },
  created () {
    this.$bus.on('getFiles', (fileData) => {
      this.addArr = fileData
    })
    this.$bus.on('ForbidModifyUploadSetting', () => {
      this.isDisable = true
    })
  }
}
</script>

<style>
.el-scrollbar {
  height: 100%;
}
div.el-scrollbar__wrap {
  overflow-x: hidden;
}
div.el-scrollbar__bar.is-horizontal {
  display: none;
}
#file-list-item:hover {
  cursor: pointer;
  transform: scale(1.2,1.1);
  -webkit-transform: scale(1.2,1.1);
  -moz-transform: scale(1.2,1.1);
  -o-transform: scale(1.2,1.1);
  -ms-transform: scale(1.2,1.1);
}
</style>

<style scoped>
ul {
  list-style-type: none;
  width: 100%;
  height: 100%;
}
li {
  margin-top: 10px;
}
.add-file-list {
  width: 100%;
  height: 70%;
}
.el-tag {
  width: 200px
}
#file-list-item {
  /* background-color: darkkhaki; */
  display: flex;
  align-items: flex-end;
  padding-right: 0;
  background-color: rgba(255,255,255,0.5);
  width: 400px;
  height: 30px;
  border-radius: 15px;
  line-height: 30px;
  color: #606266;
}
#close-icon {
  justify-self: flex-end;
  width: 15px;
}
#file-icon {
  margin-left: 10px;
  align-self: center;
  width: 25px;
}
#file-name {
  width: 320px;
}
</style>
