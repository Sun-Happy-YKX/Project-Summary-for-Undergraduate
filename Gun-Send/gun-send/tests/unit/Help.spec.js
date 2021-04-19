import { shallowMount, createLocalVue } from '@vue/test-utils'
import Help from '@/components/Home/Help.vue'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('Help.vue', () => {
    const wapper = shallowMount(Help, {localVue})

    it('测试p标签的渲染', () => {
        const p = wapper.find('p')
        expect(p.text()).toEqual('Gun-Send')
    })

    it('测试msg的传值正确', () => {
        expect(wapper.vm.msg).toBe('帮助')
    })

    it('测试goback-home组件的渲染是否成功', () => {
        const goback = wapper.find('#gobackhome')
        expect(goback.text()).toEqual('')
    })
})
