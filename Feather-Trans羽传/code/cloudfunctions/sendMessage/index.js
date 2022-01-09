const cloud = require('wx-server-sdk')
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV,
})
exports.main = async (event, context) => {
  try {
    var accepterID = event.accepterID
    var messageContent = event.messageContent
    var senderName = event.senderName
    var sendTime = event.sendTime
    var fileID = event.fileID
    const result = await cloud.openapi.subscribeMessage.send({
        "touser": accepterID, // 发送人的ID
        "page": 'pages/fileAccessUsers/fileAccessUsers?fileID='+fileID+'&userInfo='+accepterID,
        "lang": 'zh_CN',
        "templateId": 'Al5lWrv7uFR1hQf1BBlNGOSmHivCeKkTUTCegisgn_k', // 模板ID
        "miniprogramState": 'developer',
        "data": {
          "thing3": {
            "value": messageContent
          },
          "thing7": {
            "value": senderName
          },
          "time2": {
            "value": sendTime
          }
        },
      })
    return result
  } catch (err) {
    return err
  }
}