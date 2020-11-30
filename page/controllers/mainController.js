'use strict'

const controller = {}

controller.index = async (req, res) => {
  console.log(req.session)
  res.render('index')
}

module.exports = controller
