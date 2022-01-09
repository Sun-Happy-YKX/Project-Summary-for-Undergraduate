import { shallowMount, createLocalVue } from '@vue/test-utils'
import EncryptionChooser from '@/components/Upload/EncryptionChooser.vue'
import ElementUI from 'element-ui'
import VueBus from 'vue-bus'

const localVue = createLocalVue()
localVue.use(ElementUI)
localVue.use(VueBus)

describe('EncryptionChooser.vue', () => {
    let wrapper
  
    beforeEach(() => {
        wrapper = shallowMount(EncryptionChooser, {localVue})
    })
  
    afterEach(() => {
        wrapper.destroy()
    })

    it('测试created', () => {
        wrapper.vm.isDisable = false
        wrapper.vm.$bus.emit('ForbidModifyUploadSetting')
        expect(wrapper.vm.isDisable).toBeTruthy()
    })

    it('测试passwordchange方法', () => {
        wrapper.vm.passwordChange(() => {
            expect(wrapper.vm.$bus.on('getPassword'))
        })
    })

    it('测试switchChange方法', () => {
        wrapper.vm.switchChange(() => {
            expect(wrapper.vm.$bus.on('getPassword'))
            expect(wrapper.vm.$bus.on('getEncryptChoice'))
        })
    })
})
