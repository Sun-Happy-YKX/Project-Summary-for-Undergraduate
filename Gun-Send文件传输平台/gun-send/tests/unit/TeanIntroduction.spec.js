import { shallowMount, createLocalVue } from '@vue/test-utils'
import TeamIntroduction from '@/components/Home/TeamIntroduction.vue'
import ElementUI from 'element-ui'

const localVue = createLocalVue()
localVue.use(ElementUI)

describe('TeamIntroduction.vue', () => {
    const wapper = shallowMount(TeamIntroduction, {localVue})

    it('测试p标签的渲染', () => {
        const p = wapper.find('p')
        expect(p.text()).toEqual('Gun-Send')
    })

    it('测试msg的传值正确', () => {
        expect(wapper.vm.msg).toBe('团队介绍')
    })

    it('测试goback-home组件的渲染是否成功', () => {
        const goback = wapper.find('#gobackhome')
        expect(goback.text()).toEqual('')
    })
})
