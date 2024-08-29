import kue from 'kue';
import { expect } from 'chai';
import sinon from 'sinon';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function () {
  let queue;

  beforeEach(function () {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(function () {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', function () {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and add them to the queue', function () {
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(list, queue);

    const jobs = queue.testMode.jobs;

    expect(jobs.length).to.equal(2);
    expect(jobs[0].type).to.equal('push_notification_code_3');
    expect(jobs[1].type).to.equal('push_notification_code_3');
  });

  it('should log the appropriate messages for job events', function () {
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      }
    ];

    const consoleLogSpy = sinon.spy(console, 'log');

    createPushNotificationsJobs(list, queue);

    const job = queue.testMode.jobs[0];
    job.emit('enqueue');
    job.emit('complete');
    job.emit('failed', 'An error occurred');
    job.emit('progress', 50);

    expect(consoleLogSpy.calledWith(`Notification job created: ${job.id}`)).to.be.true;
    expect(consoleLogSpy.calledWith(`Notification job ${job.id} completed`)).to.be.true;
    expect(consoleLogSpy.calledWith(`Notification job ${job.id} failed: An error occurred`)).to.be.true;
    expect(consoleLogSpy.calledWith(`Notification job ${job.id} 50% complete`)).to.be.true;

    consoleLogSpy.restore();
  });
});
