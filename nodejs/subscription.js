import {SubscriptionClient} from '@azure/arm-subscriptions';
import {all} from './format.js';

export default class Subscription {
	constructor(credential, subscriptionId, logger = console) {
		Object.assign(this, {logger, credential});
		this.client = new SubscriptionClient(this.credential);
		this.subscriptionId = subscriptionId;
	}

	async ping() {

		try {
			const list = this.client.subscriptions.list();
			const {value} = await list.next();
			if (!this.subscriptionId) {
				this.subscriptionId = value.subscriptionId;
			}

			return true;
		} catch (e) {
			this.logger.error(e);
			return false;
		}
	}

	async regions() {
		const iterator = this.client.subscriptions.listLocations(this.subscriptionId);
		return await all(iterator, ({name, displayName}) => ({name, displayName}));
	}

	async list() {
		const iterator = this.client.subscriptions.list();
		return await all(iterator);
	}
}