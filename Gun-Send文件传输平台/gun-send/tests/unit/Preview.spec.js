import { shallowMount, createLocalVue } from '@vue/test-utils'
import Preview from '@/components/Preview.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'
import VideoPlayer from 'vue-video-player'
import 'vue-video-player/src/custom-theme.css'
import 'video.js/dist/video-js.css'


const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)
localVue.use(VideoPlayer)


describe('Preview.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(Preview, { localVue })
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试created', () => {
        URL.createObjectURL = jest.fn()
        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.pdf' })
        expect(wrapper.vm.PreviewName).toBe('test.pdf')
        expect(wrapper.vm.PreviewFile).toEqual({ name: 'test.pdf' })
        expect(wrapper.vm.PreviewType).toBe(1)
        wrapper.vm.$bus.on('startPdfPreview', (url) => {
            expect(url).not.toBe('')
        })
        expect(wrapper.vm.txtType).toBe('pdf')

        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.doc' })
        expect(wrapper.vm.txtType).toBe('pdf')


        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.txt' })
        expect(wrapper.vm.txtType).toBe('txt')

        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.jpg' })
        expect(wrapper.vm.PreviewType).toBe(2)
    
        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.avi' })
        expect(wrapper.vm.PreviewType).toBe(3)

        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.mp3' })
        expect(wrapper.vm.PreviewType).toBe(4)

        wrapper.vm.$bus.emit('PreviewFile', { name: 'test.e' })
        expect(wrapper.vm.PreviewType).toBe(5)

    })

    it('测试方法returnToFileUpload的调用结果', () => {
        document.getElementById = jest.fn()
        document.getElementById.mockReturnValue(VideoPlayer)
        document.getElementById().pause = jest.fn()
        wrapper.vm.returnToFileUpload()
        wrapper.vm.$bus.on('closePreview', (msg) => {
            expect(msg).toBe('send')
        })
    }) 
})
