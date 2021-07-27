const {KeyClient, CryptographyClient} = require("@azure/keyvault-keys");
const {createHash} = require('crypto')
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

const KnownSignatureAlgorithms = {
    /** RSASSA-PSS using SHA-256 and MGF1 with SHA-256, as described in https://tools.ietf.org/html/rfc7518 */
    PS256: "PS256",
    /** RSASSA-PSS using SHA-384 and MGF1 with SHA-384, as described in https://tools.ietf.org/html/rfc7518 */
    PS384: "PS384",
    /** RSASSA-PSS using SHA-512 and MGF1 with SHA-512, as described in https://tools.ietf.org/html/rfc7518 */
    PS512: "PS512",
    /** RSASSA-PKCS1-v1_5 using SHA-256, as described in https://tools.ietf.org/html/rfc7518 */
    RS256: "RS256",
    /** RSASSA-PKCS1-v1_5 using SHA-384, as described in https://tools.ietf.org/html/rfc7518 */
    RS384: "RS384",
    /** RSASSA-PKCS1-v1_5 using SHA-512, as described in https://tools.ietf.org/html/rfc7518 */
    RS512: "RS512",
    /** ECDSA using P-256 and SHA-256, as described in https://tools.ietf.org/html/rfc7518. */
    ES256: "ES256",
    /** ECDSA using P-384 and SHA-384, as described in https://tools.ietf.org/html/rfc7518 */
    ES384: "ES384",
    /** ECDSA using P-521 and SHA-512, as described in https://tools.ietf.org/html/rfc7518 */
    ES512: "ES512",
    /** ECDSA using P-256K and SHA-256, as described in https://tools.ietf.org/html/rfc7518 */
    ES256K: "ES256K"
}
const SignDataAlgorithms = {
    PS256: KnownSignatureAlgorithms.PS256,
    RS256: KnownSignatureAlgorithms.RS256,
    PS384: KnownSignatureAlgorithms.PS384,
    RS384: KnownSignatureAlgorithms.RS384,
    PS512: KnownSignatureAlgorithms.PS512,
    RS512: KnownSignatureAlgorithms.RS512
}

/**
 *
 * @enum string
 */
const EncryptionAlgorithm = {
    'RSA-OAEP': 'RSA-OAEP',
    'RSA-OAEP-256': 'RSA-OAEP-256',
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
        const key = await this.client.getKey(keyName)
        return new Cryptography(key, this.credential)
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

const algorithmMap = {
    RSA: EncryptionAlgorithm["RSA-OAEP-256"],
    EC: KnownSignatureAlgorithms.ES256,
}

class Cryptography {
    /**
     *
     * @param {KeyVaultKey} key
     * @param credential
     */
    constructor(key, credential) {
        this.client = new CryptographyClient(key, credential)
        this.key = key
    }

    /**
     *
     * @param {string} plaintext
     * @param {EncryptionAlgorithm} [algorithm]
     * @return {Promise<Uint8Array>}
     */
    async encrypt(plaintext, algorithm) {
        if (!algorithm) {
            algorithm = algorithmMap[this.key.keyType]
        }
        const {result} = await this.client.encrypt({algorithm, plaintext: Buffer.from(plaintext)})
        return result
    }

    /**
     *
     * @param {Uint8Array} ciphertext
     * @param [algorithm]
     * @return {Promise<string>}
     */
    async decrypt(ciphertext, algorithm) {
        if (!algorithm) {
            algorithm = algorithmMap[this.key.keyType]
        }
        const {result} = await this.client.decrypt({algorithm, ciphertext})
        return result.toString()
    }

    async sign(message, algorithm) {


        if (!algorithm) {
            algorithm = algorithmMap[this.key.keyType]
            if (this.key.keyType === KeyType.EC) {
                const hash = createHash("sha256");

                const digest = hash.update(message).digest();
                const {result} = await this.client.sign(algorithm, digest)
                return result.toString()
            }

        }
        const {result} = await this.client.signData(algorithm, Buffer.from(message))
        return Buffer.from(result).toString('hex')
    }
}

module.exports = {
    Key,
    KeyType,
    EncryptionAlgorithm,
    Cryptography,
    KnownSignatureAlgorithms,
    SignDataAlgorithms,
}

