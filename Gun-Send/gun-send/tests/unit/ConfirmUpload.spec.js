import { shallowMount, createLocalVue } from '@vue/test-utils'
import ConfirmUpload from '@/components/Home/ConfirmUpload.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const mockPush = jest.fn()
const $router = {
  push: mockPush
}

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('ConfirmUpload.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(ConfirmUpload, {localVue, mocks: {$router}})
    })
      
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试confirmSubmit函数点击确认按钮的运行结果', () => {
        wrapper.vm.$confirm = jest.fn()
        wrapper.vm.$confirm.mockResolvedValue()
        wrapper.vm.confirmSubmit(() => {
            wrapper.vm.$message = jest.fn()
            wrapper.vm.$message.mockResolvedValue()
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试confirmSubmit函数点击取消按钮的运行结果', () => {
        wrapper.vm.$confirm = jest.fn()
        wrapper.vm.$confirm.mockRejectedValue()
        wrapper.vm.confirmSubmit(() => {
            wrapper.vm.$message = jest.fn()
            wrapper.vm.$message.mockResolvedValue()
        })
    })

    it('测试el-button标签内的文本', () => {
        expect(wrapper.find('.button').text()).toEqual('确认上传')
    })

    it('测试confirmSubmit函数是否正常执行', () => {
        const btn = wrapper.find('.button')
        wrapper.vm.confirmSubmit = jest.fn()
        btn.trigger('click')
        expect(wrapper.vm.confirmSubmit).toHaveBeenCalled()
        expect(wrapper.vm.confirmSubmit).toHaveBeenCalledTimes(1)
    })

    it('测试created方法', () => {
        expect(wrapper.vm.$bus.emit('sendTitle', (title) => {
            wrapper.vm.title = title
        }))
        expect(wrapper.vm.$bus.emit('sendContent', (content) => {
            wrapper.vm.content = content
        }))
    })

    it('测试confirmSubmit方法', () => {
        wrapper.vm.title = ''
        wrapper.vm.content = '' 
        wrapper.vm.confirmSubmit(() => {
            expect(wrapper.vm.$message({
                type: 'warning',
                message: '请输入标题!'
              }))
            expect(wrapper.vm.$message({
                type: 'warning',
                message: '请输入内容!'
            }))
        })
    })

    it('测试confirmSubmit函数点击确认按钮的运行结果', () => {
        wrapper.vm.confirmSubmit(() => {
            wrapper.vm.$confirm = jest.fn()
            wrapper.vm.$confirm.mockResolvedValue()
            wrapper.vm.$message = jest.fn()
            wrapper.vm.$message.mockResolvedValue()
            expect(mockPush).toHaveBeenCalled()
        })
    })

    it('测试confirmSubmit函数点击确认按钮的运行结果', () => {
        wrapper.vm.confirmSubmit(() => {
            const btn = wrapper.find('#confirmButton')
            btn.trigger('click')
            expect(wrapper.vm.$message({
                type: 'success',
                message: '提交成功!'
            }))
        })
    })
})
