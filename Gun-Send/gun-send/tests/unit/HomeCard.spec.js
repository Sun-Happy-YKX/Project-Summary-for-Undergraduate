import { shallowMount, createLocalVue } from '@vue/test-utils'
import HomeCard from '@/components/Home/HomeCard.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const mockPush = jest.fn()
const $router = {
  push: mockPush
}

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('HomeCard.vue', () => {
    const wrapper = shallowMount(HomeCard, {localVue, mocks: {$router}})

    it('测试jumptoupload方法', () => {
        wrapper.vm.jumptoupload(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试jumptodownload方法', () => {
        wrapper.vm.jumptodownload(() => {
            expect(mockPush).toHaveBeenCalled()
        })
    })
})
