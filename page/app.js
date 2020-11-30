'use strict'

const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const logger = require('morgan')
const db = require('./model/database')
const session = require('express-session')
const secret = require('./secret')

const app = express()
const PORT = 8080

app.engine('hbs', hbs.express4({
  defaultLayout: path.join(__dirname, 'views', 'main')// ,
  // partialsDir: path.join(__dirname, 'views', 'partials') uncomment if used
}))

app.set('view engine', 'hbs')
app.set('views', path.join(__dirname, 'views'))

// additional middleware
app.use(logger('dev'))
app.use(express.urlencoded({ extended: false }))
app.use(express.static(path.join(__dirname, 'public')))

// session options
const sessOpt = {
  name: 'comment-label',
  secret: secret.secret_string,
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 12000 // 0.2 minute
  }
}

app.use(session(sessOpt))
// Dealing with comment id
app.use((req, res, next) => {
  if (!req.session.init) { // if first connection
    req.session.init = true
    req.session.commentid = ''
  }
})
app.use('/', require('./routes/mainRoute'))
// prevent browser from looking for favicon and throwing
// errors left and right
app.get('/favicon.ico', (req, res) => res.status(204))

app.use(function (req, res, next) {
  res.status(404).send({ error: 'Not found' })
})

app.listen(PORT, () => console.log('Server running on local host, port 8080'))
