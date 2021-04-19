import { hashcode } from './sha256'
// use sha256 to encrypt and check
export function encryptAndCheck (rawData, correctData) {
  const encryptData = hashcode(rawData)
  if (encryptData === correctData) {
    return true
  } else {
    return false
  }
}
