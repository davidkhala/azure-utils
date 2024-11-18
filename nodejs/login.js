import {DefaultAzureCredential} from '@azure/identity';

export const getCredential = () => new DefaultAzureCredential();
