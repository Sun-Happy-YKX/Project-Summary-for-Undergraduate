export function destroy (url) {
  this.$gun.get('fileShare-gunSend').get(url).put(null)
}
export function formatDate (date) {
  return (date.getFullYear().toString() + '-' +
  (date.getMonth() + 1).toString() + '-' +
  date.getDate().toString() + ' ' +
  date.getHours().toString() + ':' +
  date.getMinutes().toString() + ':' +
  date.getSeconds().toString())
}
export async function checkIfRetained (gunLink) {
  const retained = await (async () => {
    const current = new Date()
    let startTime
    let endTime
    await gunLink.get('startTime').once(
      function (start) {
        startTime = start
      }
    )
    if (startTime === undefined) {
      return '该文件不存在'
    } else {
      startTime = new Date(startTime)
      if (startTime > current) {
        return '该文件将于' + formatDate(startTime) + '开放下载'
      }
    }
    await gunLink.get('endTime').once(
      function (end) {
        endTime = end
      }
    )
    if (endTime === undefined) {
      return '该文件不存在'
    } else {
      endTime = new Date(endTime)
      if (endTime < current) {
        return '文件已于' + formatDate(endTime) + '过期'
      }
    }
    let currentDownload
    await gunLink.get('currentDownloadAccount').once(
      function (account) {
        currentDownload = account
      }
    )
    let maxDownload
    await gunLink.get('MaxDownloadAccount').once(
      function (account) {
        maxDownload = account
      }
    )
    if (currentDownload < maxDownload) {
      return ''
    } else {
      return '文件接收次数已达上限'
    }
  })()
  return retained
}
