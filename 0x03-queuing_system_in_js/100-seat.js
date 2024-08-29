const express = require('express');
const { setAsync, getAsync } = require('./redisClient');
const queue = require('./queue');

const app = express();
const PORT = 1245;

let reservationEnabled = true;

setAsync('available_seats', '50').catch(console.error);

app.get('/available_seats', async (req, res) => {
  try {
    const availableSeats = await getAsync('available_seats');
    res.json({ numberOfAvailableSeats: availableSeats });
  } catch (error) {
    res.status(500).json({ status: 'Error retrieving available seats' });
  }
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (error) => {
    console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = parseInt(await getAsync('available_seats'), 10);
      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }
      await setAsync('available_seats', (availableSeats - 1).toString());
      done();
    } catch (error) {
      done(error);
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
