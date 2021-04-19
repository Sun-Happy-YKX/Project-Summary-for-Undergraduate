import { shallowMount, createLocalVue } from '@vue/test-utils'
import DueTimeChooser from '@/components/Upload/DueTimeChooser.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

const mockPush = jest.fn()
const $event =  mockPush

describe('DueTimeChoose.vue', () => {
    const wrapper = shallowMount(DueTimeChooser, {localVue, mocks: {$event}})

    it('测试changeStartHandler函数被调用', () => {
        wrapper.vm.changeStartHandler(() => {
            expect(wrapper.vm.$bus.on('getStartTime'))
        })
    })

    it('测试changeEndHandler函数被调用', () => {
        wrapper.vm.changeEndHandler(() => {
            expect(wrapper.vm.$bus.on('getEndTime'))
        })
    })

    it('测试created方法', () => {
        wrapper.vm.isDisable = false
        wrapper.vm.$bus.emit('ForbidModifyUploadSetting')
        expect(wrapper.vm.isDisable).toBeTruthy()
    })
})
