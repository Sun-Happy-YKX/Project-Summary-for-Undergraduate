<template>
<div v-if="canComment == true">
  <el-rate v-model="value" show-text></el-rate>
  <el-tag type="info">点击提交后自动返回首页</el-tag><br>
  <el-button type="primary" @click="CommitComment">提交评论</el-button>
</div>
</template>

<script>
export default {
  data () {
    return {
      value: null,
      canComment: false
    }
  },
  methods: {
    CommitComment () {
      return this.$alert('感谢您的用心评论！', '致谢', {
        confirmButtonText: '确定',
        type: 'info',
        center: true
      }).then(() => {
        this.$router.push({ name: 'Home' })
      })
    }
  },
  created () {
    this.$bus.on('DisplayComment', () => {
      this.canComment = true
    })
  }
}
</script>

<style>

</style>
