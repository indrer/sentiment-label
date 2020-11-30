'use strict'

const express = require('express')
const router = express.Router()
const mainController = require('../controllers/mainController')
const db = require('../model/database')

router.get('/', async (req, res) => mainController.index(req, res, db))

router.post('/', async (req, res) => mainController.post(req, res, db))

module.exports = router
