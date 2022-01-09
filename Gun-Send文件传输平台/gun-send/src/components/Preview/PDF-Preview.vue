<template>
  <div class="pdf" v-show="fileType === 'pdf'">
    <p class="arrow">
    <span @click="changePdfPage(0)" class="turn" :class="{grey: currentPage==1}">Preview</span>
    {{ currentPage }} / {{ pageCount }}
    <span @click="changePdfPage(1)" class="turn" :class="{grey: currentPage==pageCount}">Next</span>
    </p>
    <pdf :src="src" :page="currentPage"
      @num-pages="pageCount=$event"
      @page-loaded="currentPage=$event"
      @loaded="loadPdfHandler">
    </pdf>
    <p class="arrow">
    <span @click="changePdfPage(0)" class="turn" :class="{grey: currentPage==1}">Preview</span>
    {{ currentPage }} / {{ pageCount }}
    <span @click="changePdfPage(1)" class="turn" :class="{grey: currentPage==pageCount}">Next</span>
    </p>
  </div>
</template>

<script>
import pdf from 'vue-pdf'
export default {
  components: {
    pdf
  },
  data () {
    return {
      currentPage: 0,
      pageCount: 0,
      fileType: 'pdf',
      src: ''
    }
  },
  created () {
    this.$bus.on('startPdfPreview', (previewFileSrc) => {
      this.src = previewFileSrc
    })
  },
  methods: {
    changePdfPage (Page) {
      if (Page === 0 && this.currentPage > 1) {
        this.currentPage--
      }
      if (Page === 1 && this.currentPage < this.pageCount) {
        this.currentPage++
      }
    },
    loadPdfHandler () {
      this.currentPage = 1
    }
  }
}
</script>

<style>
span {
  color: white;
}
</style>
