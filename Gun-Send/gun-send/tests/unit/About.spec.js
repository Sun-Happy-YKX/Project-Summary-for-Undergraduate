import { shallowMount, createLocalVue } from '@vue/test-utils'
import About from '@/components/Home/About.vue'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('About.vue', () => {
    const wapper = shallowMount(About, {localVue})

    it('测试p标签的渲染', () => {
        const p = wapper.find('p')
        expect(p.text()).toEqual('Gun-Send')
    })

    it('测试msg的传值正确', () => {
        expect(wapper.vm.msg).toBe('关于产品')
    })

    it('测试goback-home组件的渲染是否成功', () => {
        const goback = wapper.find('#gobackhome')
        expect(goback.text()).toEqual('')
    })
})
