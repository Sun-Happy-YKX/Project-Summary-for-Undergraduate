<template>
    <el-row :gutter="20" id="elrow">
        <el-col :span="2"><el-button id="abutton" @click.native="jumptohome" class="go">返回首页</el-button></el-col>
    </el-row>
</template>

<script>
export default {
  name: 'GobackHome',
  methods: {
    jumptohome () {
      this.$router.push('/Home')
    }
  }
}
</script>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.el-col:hover .el-button {
  background-color: rgba(224, 224, 233, 0.4);
}
.go {
  background-color: #f16272;
  color: #fff;
  height: 30px;
  font-weight: bold;
  letter-spacing: 1.5px;
  border: 0;
  width: 100px;
  margin-left: 30px;
  margin-top: 20px;
  line-height: 8px;
}
</style>
