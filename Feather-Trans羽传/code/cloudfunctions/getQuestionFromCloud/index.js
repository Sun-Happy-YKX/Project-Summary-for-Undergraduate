// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

// 云函数入口函数
exports.main = async (event, context) => {
  const db = cloud.database()
  const question_num = parseInt(event.question_num)
  return db.collection('questions').aggregate().sample({
    size:question_num
  }).end()
}