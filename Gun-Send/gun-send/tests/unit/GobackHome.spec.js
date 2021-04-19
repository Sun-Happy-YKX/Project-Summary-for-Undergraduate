import { shallowMount, createLocalVue } from '@vue/test-utils'
import GobackHome from '@/components/GobackHome.vue'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

const mockPush = jest.fn()
const $router = {
  push: mockPush
}

describe('GobackHome.vue', () => {
    const wrapper = shallowMount(GobackHome, {localVue, mocks: {$router}})

    it('测试文本显示正确', () => {
        expect(wrapper.find('#abutton').text()).toEqual('返回首页')
    })

    it('测试jumptohome函数执行结果', () => {
        return wrapper.vm.jumptohome(() => {
            expect(mockPush).toHaveBeenCalled()
            expect(mockPush).toHaveBeenCalledTimes(1)
        })
    })

    it('测试jumptohome函数是否被执行', () => {
        wrapper.vm.jumptohome = jest.fn()
        const btn = wrapper.find('#abutton')
        btn.trigger('click')
        expect(wrapper.vm.jumptohome).toHaveBeenCalled()
        expect(wrapper.vm.jumptohome).toHaveBeenCalledTimes(1)
    })
})
