import {DefaultAzureCredential} from '@azure/identity';
import {SubscriptionClient} from '@azure/arm-subscriptions';

export const getConfigFileCredential = () => new DefaultAzureCredential();

export const auth = (credential) => {
	const client = new SubscriptionClient(credential);
	client.subscriptions.list();
};
