import {getConfigFileCredential, auth} from '../login.js';
import {all} from '../format.js';
import {SubscriptionClient} from '@azure/arm-subscriptions';

const credentials = getConfigFileCredential();
const client = new SubscriptionClient(credentials);
describe('auth', function () {
	this.timeout(0);
	it('subscriptions.list', async () => {

		const list = client.subscriptions.list();
		const values = await all(list);

		console.debug(values);

	});
	it('dry-run', async () => {
		const isAllowed = await auth(credentials);
		console.debug(isAllowed);
	});
});
