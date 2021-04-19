import { shallowMount, createLocalVue } from '@vue/test-utils'
import HomeLayout from '@/components/Home/HomeLayout.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const mockPush = jest.fn()
const $router = {
  push: mockPush
}

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('HomeLayout.vue', () => {
    const wrapper = shallowMount(HomeLayout, {localVue, mocks: {$router}})

    it('测试jumptoabout方法', () => {
        wrapper.vm.jumptoabout(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试jumptoteam方法', () => {
        wrapper.vm.jumptoteam(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试jumptohelp方法', () => {
        wrapper.vm.jumptohelp(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试jumptofeedback方法', () => {
        wrapper.vm.jumptofeedback(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })
})