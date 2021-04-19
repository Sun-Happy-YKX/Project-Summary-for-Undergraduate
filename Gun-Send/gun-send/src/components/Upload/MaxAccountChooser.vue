<template>
<div>
  <el-form-item label="下载次数" id="featurename" size="small">
  <el-input-number id="inputnum" v-model="num1" @change="handleChange" style="width:150px;margin-left:10px;"
   :disabled="isDisable" :min="1" :max="100" label="描述文字"></el-input-number>
  </el-form-item>
</div>
</template>
<script>
export default {
  data () {
    return {
      num1: 1,
      isDisable: false
    }
  },
  methods: {
    handleChange () {
      this.$bus.emit('getMaxNum', this.num1)
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
#inputnum {
  width: 200px;
  display: inline-block;
}
</style>
