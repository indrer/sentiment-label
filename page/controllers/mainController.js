'use strict'

const controller = {}

/*
 * comment_id
 * video_id
 * body
 * title
 */

controller.index = async (req, res, db) => {
  try {
    var row = await db.query(`SELECT sentiment_anls.comment.comment_id, sentiment_anls.comment.video_id, sentiment_anls.comment.body, sentiment_anls.video.title from sentiment_anls.comment
    inner join sentiment_anls.video on comment.video_id=video.url
    WHERE rated=0
    ORDER BY RANDOM()
    LIMIT 1;`)
    req.session.commentid = row.rows[0].comment_id
    res.locals.commentinfo = {
      body: row.rows[0].body,
      videoid: row.rows[0].video_id,
      title: row.rows[0].title
    }
    res.render('index')
  } catch (err) {
    console.log(err.stack)
  }
}

controller.post = async (req, res, db) => {
  // let commentid = [req.session.commentid]
  let commentid = ['test'] // DO NOT UNCOMMENT THIS WHILE TESTING
  let sentiment = parseInt(req.body.sentiment)
  let query = ''
  switch (sentiment) {
    case 1:
      query = `update sentiment_anls.comment
      set positive = positive + 1, rated = rated + 1
      where comment_id = $1;`
      break
    case -1:
      query = `update sentiment_anls.comment
      set negative = negative + 1, rated = rated + 1
      where comment_id = $1;`
      break
    case 0:
      query = `update sentiment_anls.comment
      set neutral = neutral + 1, rated = rated + 1
      where comment_id = $1;`
      break
  }
  try {
    console.log(query)
    await db.query(query, commentid)
  } catch (err) {
    console.log(err)
  }
  res.redirect('/')
}
module.exports = controller
