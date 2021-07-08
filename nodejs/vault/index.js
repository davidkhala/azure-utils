const {KeyClient, CryptographyClient} = require("@azure/keyvault-keys");

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
/**
 *
 * @enum string
 */
const EncryptionAlgorithm = {
    'RSA-OAEP': 'RSA-OAEP',
    "RSA-OAEP-256": 'RSA-OAEP-256',
    RSA1_5: 'RSA1_5',
    A128GCM: 'A128GCM',
    A192GCM: 'A192GCM',
    A256GCM: 'A256GCM',
    A128KW: 'A128KW',
    A192KW: 'A192KW',
    A256KW: 'A256KW',
    A128CBC: 'A128CBC',
    A192CBC: 'A192CBC',
    A256CBC: 'A256CBC',
    A128CBCPAD: 'A128CBCPAD',
    A192CBCPAD: 'A192CBCPAD',
    A256CBCPAD: 'A256CBCPAD',
}

class Key {
    /**
     *
     * @param keyVaultName
     * @param credential
     * @param [logger]
     */
    constructor(keyVaultName, credential, logger = console) {
        const KVUri = "https://" + keyVaultName + ".vault.azure.net";
        const client = new KeyClient(KVUri, credential);
        Object.assign(this, {client, logger, credential})
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

    async asCrypto(keyName) {
        const {id} = await this.client.getKey(keyName)
        const cryptoClient = new CryptographyClient(id, this.credential)

        return cryptoClient
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

    async delete(keyName, {sync, force}) {
        const {client} = this
        let key
        const throwOthers = (e) => {
            const {name, code, message} = e
            if (name !== 'RestError' || code !== 'KeyNotFound') {
                throw e
            }
            this.logger.warn(message)
        }
        try {
            const result = await client.getKey(keyName)
            key = result.key
            this.logger.info(key)
        } catch (e) {
            throwOthers(e)
        }

        if (key) {
            const deletePoller = await client.beginDeleteKey(keyName);
            if (sync) {
                await deletePoller.pollUntilDone();
            }
        }

        if (force) {
            await client.purgeDeletedKey(keyName);
        }
    }

}

module.exports = {
    Key,
    KeyType,
    EncryptionAlgorithm,
}

