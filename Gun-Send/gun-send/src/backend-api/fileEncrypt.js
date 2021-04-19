const CryptoJS = require('crypto-js')
const key = CryptoJS.enc.Utf8.parse('B8D3F62AB8C2EE5C')
const iv = CryptoJS.enc.Utf8.parse('526E667B8ACA29F1')

async function fileToBase64 (file) {
  const reader = new FileReader()
  const base64Text = await new Promise(resolve => {
    reader.readAsDataURL(file)
    reader.onload = function (event) {
      return resolve(event.target.result)
    }
  })
  return base64Text
}
export async function Encrypt (file) {
  const base64Text = fileToBase64(file)
  let encrypted
  await base64Text.then(word => {
    const srcs = CryptoJS.enc.Utf8.parse(word)
    encrypted = CryptoJS.AES.encrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 })
  }).catch(
    () => { }
  )
  return encrypted.ciphertext.toString().toUpperCase()
}
async function base64ToFile (base64Text, sliceSize) {
  const base64Data = base64Text.substr(base64Text.indexOf('base64,') + 7, base64Text.length)
  let contentType = /data:([^;]*);/i.exec(base64Text)[1]
  contentType = contentType || ''
  sliceSize = sliceSize || 512
  const byteCharacters = atob(base64Data)
  const byteArrays = []

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize)
    const byteNumbers = new Array(slice.length)
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    byteArrays.push(byteArray)
  }

  const blob = new Blob(byteArrays, { type: contentType })
  return blob
}
export async function Decrypt (word) {
  const encryptedHexStr = CryptoJS.enc.Hex.parse(word)
  const srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr)
  const decrypt = CryptoJS.AES.decrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 })
  const decryptedStr = decrypt.toString(CryptoJS.enc.Utf8)
  const base64Text = decryptedStr.toString()
  const blob = await base64ToFile(base64Text)
  return blob
}
