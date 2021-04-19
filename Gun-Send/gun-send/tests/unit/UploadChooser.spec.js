import { shallowMount, createLocalVue } from '@vue/test-utils'
import UploadChooser from '@/components/Upload/UploadChooser.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

const mockGet = jest.fn()
const $event = mockGet

describe('UploadChooser.vue', () => {
    const wrapper = shallowMount(UploadChooser, {localVue, mocks: {$event}})

    it('测试created方法', () => {
        wrapper.vm.isDisable = false
        wrapper.vm.$bus.emit('ForbidModifyUploadSetting', () => {
            expect(wrapper.vm.isDisable).toBe(true)
        })
    })

    it('测试changeHandler方法', () => {
        wrapper.vm.changeHandler(() => {
            expect(wrapper.vm.$bus.emit('getFileName'))
        })
    })
})
