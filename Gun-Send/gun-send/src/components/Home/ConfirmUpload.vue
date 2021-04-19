<template>
    <div>
        <el-button class="button" type="text" @click.native="confirmSubmit">确认上传</el-button>
    </div>
</template>

<script>
export default {
  name: 'ConfirmUpload',
  data () {
    return {
      title: '',
      content: ''
    }
  },
  methods: {
    confirmSubmit () {
      if (this.title === '') {
        this.$message({
          type: 'warning',
          message: '请输入标题!'
        })
        return
      }
      if (this.content === '') {
        this.$message({
          type: 'warning',
          message: '请输入内容!'
        })
        return
      }
      this.$confirm('确定提交反馈?', '提示', {
        cancelButtonText: '取消',
        confirmButtonText: '确定',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '提交成功!'
        })
        const feedback = {
          title: this.title,
          content: this.content
        }
        this.$gun.get('feedback').set(feedback)
        this.$router.push({ name: 'Home' })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消提交 请您继续补充'
        })
      })
    }
  },
  created () {
    this.$bus.on('sendTitle', (title) => {
      this.title = title
    })
    this.$bus.on('sendContent', (content) => {
      this.content = content
    })
  }
}
</script>

<style lang="scss">
.button {
  color: #6acad1;
  border-color: #6acad1;
  border-width: 2px;
  border-style: solid;
  padding-top: 8px;
  padding-bottom: 8px;
  text-align: center;
  background-color: rgba(6,27,45,.6);
  width: 80px;
}
</style>
