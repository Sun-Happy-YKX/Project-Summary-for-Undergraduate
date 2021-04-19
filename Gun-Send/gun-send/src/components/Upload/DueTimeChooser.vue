<template>
<div>
  <div class="block">
    <el-form-item label="生效时间">
    <el-date-picker @change="changeStartHandler" class="timeChooser"
      style="width:150px;margin-left:10px;"
      v-model="startTime" :disabled="isDisable"
      align="left" type="date" size="small"
      placeholder="选择生效日期">
    </el-date-picker>
    </el-form-item>
    <el-form-item label="失效时间">
    <el-date-picker @change="changeEndHandler" class="timeChooser"
      style="width:150px;margin-left:10px;"
      v-model="endTime" :disabled="isDisable"
      align="left" type="date" size="small"
      placeholder="选择失效日期">
    </el-date-picker>
    </el-form-item>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      startTime: new Date(),
      endTime: new Date(),
      isDisable: false
    }
  },
  methods: {
    changeStartHandler (event) {
      this.$bus.emit('getStartTime', this.startTime)
    },
    changeEndHandler (event) {
      this.$bus.emit('getEndTime', this.endTime)
    }
  },
  created () {
    this.$bus.on('ForbidModifyUploadSetting', () => {
      this.isDisable = true
    })
  }
}
</script>
<style lang="scss">
.el-picker-panel__content span {
  color: black;
}
</style>
