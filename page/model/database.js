'use strict'

const { Pool } = require('pg')
const dbSecret = require('../secret_db')
const pool = new Pool({
  user: dbSecret.user,
  host: dbSecret.host,
  database: dbSecret.database,
  password: dbSecret.password
})

pool.on('error', (err, client) => {
  console.error('Error: ', err)
})

module.exports = pool
