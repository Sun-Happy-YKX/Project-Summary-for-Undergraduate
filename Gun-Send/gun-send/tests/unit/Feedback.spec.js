import { shallowMount, createLocalVue } from '@vue/test-utils'
import Feedback from '@/components/Home/Feedback.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('Feedback.vue', () => {
    const wrapper = shallowMount(Feedback, {localVue})
    wrapper.setData({
        textarea1: '这是输入的标题',
        textarea2: '这是输入的内容' 
    })
    const divtext = wrapper.findAll('.tips')

    it('测试p标签内的文本', () => {
        const p = wrapper.find('#name')
        expect(p.text()).toEqual('Gun-Send')
    })

    it('测试文本输入框传值的正确', () => {
        expect(wrapper.vm.textarea1).toEqual('这是输入的标题')
        expect(wrapper.vm.textarea2).toEqual('这是输入的内容')
    })

    it('测试sendTitle方法', () => {
        wrapper.vm.sendTitle(() => {
            expect(wrapper.vm.$bus.on('sendTitle'))
        })
    })

    it('测试sendContent方法', () => {
        wrapper.vm.sendContent(() => {
            expect(wrapper.vm.$bus.on('sendContent'))
        })
    })
})
