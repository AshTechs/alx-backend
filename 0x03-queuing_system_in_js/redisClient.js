const Redis = require('ioredis');
const { promisify } = require('util');

const redis = new Redis();

const setAsync = promisify(redis.set).bind(redis);
const getAsync = promisify(redis.get).bind(redis);

module.exports = { redis, setAsync, getAsync };
