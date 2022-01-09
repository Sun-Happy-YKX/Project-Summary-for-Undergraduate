import { shallowMount, createLocalVue } from '@vue/test-utils'
import DownloadOperation from '@/components/Download/DownloadOperation.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('DownloadOperation.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(DownloadOperation, {localVue})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试函数startDownload的触发', () => {
        wrapper.vm.canChooseDownloadMode = true
        expect(wrapper.vm.canChooseDownloadMode).toBeTruthy()
        wrapper.vm.startDownload = jest.fn()
        const btn = wrapper.find('#download')
        btn.trigger('click')
        expect(wrapper.vm.startDownload).toBeCalled()
        expect(wrapper.vm.startDownload).toHaveBeenCalledTimes(1)
    })

    it('测试created', () => {
        wrapper.vm.$bus.emit('canChooseDownloadMode', 'send')
        expect(wrapper.vm.canChooseDownloadMode).toBeTruthy()
        wrapper.vm.$bus.emit('SendFileMessage', ['file1', 'file2'], 'testFile', { url: 'abc123' })
        expect(wrapper.vm.fileList).toEqual(['file1', 'file2'])
        expect(wrapper.vm.fileName).toBe('testFile')
        expect(wrapper.vm.gunLink).toEqual({ url: 'abc123' })
    })
})
