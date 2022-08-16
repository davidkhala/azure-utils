import {getConfigFileCredential, auth} from '../login.js';
import {SubscriptionClient} from '@azure/arm-subscriptions';

const credentials = getConfigFileCredential();
const client = new SubscriptionClient(credentials);
describe('auth', function () {
	this.timeout(0);
	it('subscriptions.list', async () => {

		const list = client.subscriptions.list();
		const values = [];
		for await (const value of list) {
			values.push(value);
		}
		console.debug(values);

	});
	it('dry-run', async () => {
		const isAllowed = auth(credentials);
		console.debug(isAllowed);
	});
});
