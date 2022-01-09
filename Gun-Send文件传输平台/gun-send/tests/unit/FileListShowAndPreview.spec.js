import { shallowMount, createLocalVue } from '@vue/test-utils'
import FileListShowAndPreview from '@/components/Download/FileListShowAndPreview.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('FileListShowAndPreview.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(FileListShowAndPreview, {localVue})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试方法clickToPreview的调用结果', () => {
        wrapper.vm.clickToPreview('file1')
        wrapper.vm.$bus.on('PreviewFile', (val) => {
            expect(val).toBe('file1')
        })
        wrapper.vm.$bus.on('startPreview', (msg) => {
            expect(msg).toBe('send')
        })
    })
})
