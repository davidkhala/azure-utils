import { DefaultAzureCredential } from "@azure/identity";
export const getConfigFileCredential = () => new DefaultAzureCredential();
