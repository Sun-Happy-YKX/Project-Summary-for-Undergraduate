import { shallowMount, createLocalVue } from '@vue/test-utils'
import PdfPreview from '@/components/Preview/PDF-Preview.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'


const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)


describe('PDF-Preview.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(PdfPreview, {localVue})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试created', () => {
        wrapper.vm.$bus.emit('startPdfPreview', 'testVal')
        expect(wrapper.vm.src).toBe('testVal')
    })

    it('测试方法changePdfPage的调用结果', () => {
        wrapper.vm.currentPage = 2
        wrapper.vm.changePdfPage(0)
        expect(wrapper.vm.currentPage).toBe(1)
        wrapper.vm.currentPage = 1
        wrapper.vm.pageCount = 2
        wrapper.vm.changePdfPage(1)
        expect(wrapper.vm.currentPage).toBe(2)
    })

    it('测试方法loadPdfHandler的调用结果', () => {
        wrapper.vm.loadPdfHandler()
        expect(wrapper.vm.currentPage).toBe(1)
    })
})
