<template>
<div>
  <el-form-item :label="Label">
  <el-switch v-model="isEncrypt" :disabled="isDisable === true" @change="switchChange"
   active-text="使用密码" style="width:300px;margin-left:10px;">
  </el-switch><br>
  <el-input v-model="password" placeholder="请设置密码" v-if="isEncrypt == true" @change="passwordChange"
    style="width:150px;margin-left:10px;" size="small" :disabled="isDisable === true"></el-input>
  </el-form-item>
</div>
</template>

<script>
export default {
  data () {
    return {
      isDisable: false,
      isEncrypt: false,
      password: ''
    }
  },
  computed: {
    Label () {
      return '加密传输'
    }
  },
  methods: {
    passwordChange () {
      this.$bus.emit('getPassword', this.password)
    },
    switchChange () {
      this.password = ''
      this.$bus.emit('getPassword', this.password)
      this.$bus.emit('getEncryptChoice', this.password)
    }
  },
  created () {
    this.$bus.on('ForbidModifyUploadSetting', () => {
      this.isDisable = true
    })
  }
}
</script>

<style>
.el-message-box__btns .el-button:first-child {
  background: rgb(20, 160, 130);
}
.usePwd {
  margin-right: 98px;
}
</style>
