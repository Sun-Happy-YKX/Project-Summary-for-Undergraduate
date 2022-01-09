import { hashcode } from './sha256'
function salt () {
  const time = String(new Date().getTime())
  let str = ''
  for (let i = 0; i < 8; i++) {
    const base = Math.random() < 0.5 ? 65 : 97
    str += String.fromCharCode(base + Math.floor(Math.random() * 26))
  }
  return (time + str)
}

export function getUrl (data) {
  return hashcode(data + salt())
}
