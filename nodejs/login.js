const {DefaultAzureCredential} = require("@azure/identity");
const getConfigFileCredential = () => new DefaultAzureCredential();
module.exports = {
    getConfigFileCredential
}