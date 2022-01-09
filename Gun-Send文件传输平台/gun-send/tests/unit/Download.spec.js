import { shallowMount, createLocalVue } from '@vue/test-utils'
import Download from '@/components/Download.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'
import pdf from 'vue-pdf'


const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)
localVue.use(pdf)


describe('Download.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(Download, {localVue})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试created', () => {
        wrapper.vm.isPreview = false
        wrapper.vm.$bus.emit('startPreview', 'send')
        expect(wrapper.vm.isPreview).toBeTruthy()
        wrapper.vm.isPreview = true
        wrapper.vm.$bus.emit('closePreview')
        expect(wrapper.vm.isPreview).toBeFalsy()
    })
})
