// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const db = cloud.database()
  const _=db.command
  const todos = db.collection('question_files')

  return todos.doc(event.recordID).update({
    data:{ //！注意不要忘记这个地方 一开始忘了加data
      downloadNums:_.inc(1) //下载次数+1
    }
  })
}