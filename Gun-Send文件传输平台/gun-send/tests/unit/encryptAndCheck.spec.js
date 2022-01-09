// import { shallowMount } from '@vue/test-utils'
import { encryptAndCheck } from '@/backend-api/encryptAndCheck'
import { hashcode } from '@/backend-api/sha256'

describe('test encryptAndCheck.js', () => {
    it('test the output of function encryptAndCheck', () => {
        const rawData = 'abcdefghijklmn'
        const correctData = hashcode(rawData)
        expect(encryptAndCheck(rawData, correctData)).toBeTruthy
        const raw = 'abc'
        expect(encryptAndCheck(raw,correctData)).toBeFalsy
    })
})
