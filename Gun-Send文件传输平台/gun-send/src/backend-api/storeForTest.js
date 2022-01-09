export function store (gun, url, password, storeStartTime, storeEndTime, MaxDownloadNumber, dirName) {
    const fileShare = gun.get('fileShare-gunSend')
    fileShare.get(url).put({
      startTime: storeStartTime.toString(),
      endTime: storeEndTime.toString(),
      password: password,
      MaxDownloadAccount: MaxDownloadNumber,
      currentDownloadAccount: 0,
      fileName: dirName
    })
  }