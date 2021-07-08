const {KeyClient} = require("@azure/keyvault-keys");

/**
 * @enum string
 */
const KeyType = {
    EC: 'EC',// Elliptic Curve
    'EC-HSM': 'EC-HSM',
    RSA: 'RSA',
    'RSA-HSM': 'RSA-HSM',
    oct: 'oct',// Octet sequence (used to represent symmetric keys)
    'oct-HSM': 'oct-HSM',
}


class Key {
    /**
     *
     * @param keyVaultName
     * @param credential
     */
    constructor(keyVaultName, credential, logger = console) {
        const KVUri = "https://" + keyVaultName + ".vault.azure.net";
        this.client = new KeyClient(KVUri, credential);
    }

    /**
     *
     * @param {string} keyName
     * @param {KeyType} keyType
     * @return {Promise<void>}
     */
    async create(keyName, keyType) {
        const {client} = this
        await client.createKey(keyName, keyType);
    }

    /**
     *
     * @param {string} keyName
     * @return {Promise<KeyVaultKey>}
     */
    async get(keyName) {
        const {client} = this
        return await client.getKey(keyName);
    }

    async delete(keyName, force, waitUtil) {
        const {client} = this

        try {
            const deletePoller = await client.beginDeleteKey(keyName);
            if (waitUtil) {
                await deletePoller.pollUntilDone();
            }
        } catch (e) {
            const {name, code, message} = e
            if (name !== 'RestError' || code !== 'KeyNotFound') {
                throw e
            }
            console.warn(message)
        }

        if (force) {
            await client.purgeDeletedKey(keyName);
        }
    }

}

module.exports = {
    Key,
    KeyType
}

