import {DefaultAzureCredential} from '@azure/identity';
import {SubscriptionClient} from '@azure/arm-subscriptions';

export const getConfigFileCredential = () => new DefaultAzureCredential();

export const auth = async (credential) => {
	const client = new SubscriptionClient(credential);
	try {
		const list = client.subscriptions.list()
		await list.next()
		
		return true;
	} catch (e) {
		console.error(e);
		return false;
	}
};
