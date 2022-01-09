// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

// 云函数入口函数
exports.main = async (event, context) => {
  var fileData="我是存在的"
  const db = cloud.database()
  const todos = db.collection('files')
  const wxContext = cloud.getWXContext()

  return todos.doc(event.recordID).get({ //云数据库里获取文件数据
    
  })
}