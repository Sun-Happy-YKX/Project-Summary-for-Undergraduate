import { shallowMount, createLocalVue } from '@vue/test-utils'
import Comment from '@/components/Download/Comment.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'


const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)


const $route = {
  name: 'Home'
}

const mockPush = jest.fn()
const $router = {
  push: mockPush
}

describe('Comment.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(Comment, {localVue,mocks: { $route, $router }})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试方法CommitComment的调用结果', () => {
        wrapper.vm.$alert = jest.fn()
        wrapper.vm.$alert.mockResolvedValue()
        return wrapper.vm.CommitComment().then(() => {
            expect(mockPush).toHaveBeenCalled()
            expect(mockPush).toHaveBeenCalledTimes(1)
        })
    })

    it('测试created', () => {
        wrapper.vm.canComment = false
        wrapper.vm.$bus.emit('DisplayComment')
        expect(wrapper.vm.canComment).toBeTruthy()
    })
})
