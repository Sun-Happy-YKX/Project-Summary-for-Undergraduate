import { shallowMount, createLocalVue } from '@vue/test-utils'
import MaxAccountChooser from '@/components/Upload/MaxAccountChooser.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('MaxAccountChooser.vue', () => {
    const wrapper = shallowMount(MaxAccountChooser, {localVue})

    it('测试handleChange方法', () => {
        wrapper.setData({
            num1: 1
        })
        wrapper.vm.handleChange()
        expect(wrapper.vm.$bus.emit('getMaxNum'))
    })

    it('测试created方法', () => {
        wrapper.vm.isDisable = false
        wrapper.vm.$bus.emit('ForbidModifyUploadSetting')
        expect(wrapper.vm.isDisable).toBeTruthy()
    })
})
