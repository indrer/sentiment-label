'use strict'

const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const logger = require('morgan')
const db = require('./model/database')
const mainRoute = require('./routes/mainRoute')

const app = express()
const PORT = 8080

app.engine('hbs', hbs.express4({
  defaultLayout: path.join(__dirname, 'views', 'main'),
  partialsDir: path.join(__dirname, 'views', 'partials')
}))

app.use('/', mainRoute)

app.set('view engine', 'hbs')
app.set('views', path.join(__dirname, 'views'))

// additional middleware
app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(express.static(path.join(__dirname, 'public')))

app.use(function (req, res, next) {
  res.status(404).send({ error: 'Not found' })
})

app.listen(PORT, () => console.log('Server running on local host, port 8080'))
