<template>
  <div id="home">
    <div class="box">
      <home-layout class="layout"></home-layout>
      <home-card class="card"></home-card>
    </div>
  </div>
</template>

<script>
import HomeLayout from './Home/HomeLayout'
import HomeCard from './Home/HomeCard'

export default {
  data () {
    return {
      feedbackContent: ''
    }
  },
  methods: {
  },
  updated () {
  },
  components: {
    HomeLayout,
    HomeCard
  }
}
</script>

<style lang="scss" scoped>
#home {
  position: fixed;
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  background-image: url("../assets/Home.jpg");
}
.layout {
  margin-top: 2px;
  margin-right: 20px;
  margin-left: 2px;
}
.box {
  display: flex;
  flex-direction: column;
}
.card {
  align-self: flex-end;
  margin-top: 100px;
}
.card:hover {
  background-color: #7FFFD4;
}
.footer {
  margin: 0 auto;
}
</style>
