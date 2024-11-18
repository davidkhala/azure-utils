import {getCredential} from '../login.js';
import Subscription from '../subscription.js';

const credentials = getCredential();
describe('subscriptions', function () {
    this.timeout(0);
    const az = new Subscription(credentials);
    it('list', async () => {
        const values = await az.list();
        console.debug(values);

    });
    it('ping', async () => {

        const isAllowed = await az.ping();
        console.debug(isAllowed);
    });
    it('regions', async () => {
        await az.ping();
        const values = await az.regions();
        console.debug(values);
    });
});

