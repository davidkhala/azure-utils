const {Key, KeyType} = require('../index')
const {getConfigFileCredential} = require('../../login')
const vaultName = 'davidkhala-vault'
const assert = require('assert')
const configFileCredential = getConfigFileCredential()

describe('key: EC', () => {

    const keyName = 'EC'
    const keyType = KeyType.EC

    const keyOpt = new Key(vaultName, configFileCredential)
    it('create', async function () {
        this.timeout(40000)
        await keyOpt.create(keyName, keyType)
    })
    it('get', async () => {
        const keyInfo = await keyOpt.get(keyName)
        console.log(keyInfo)
    })
    it('sign', async function () {
        this.timeout(0)

        const keyCrypto = await keyOpt.asCrypto(keyName)
        const message = 'My data'

        const signature = await keyCrypto.sign(message)
        const expected = 'efbfbd65efbfbd25efbfbdd683efbfbdefbfbd0a7665efbfbd41efbfbd0eefbfbd40efbfbdefbfbd35efbfbdefbfbd7fefbfbd6fefbfbd0fefbfbdefbfbd3defbfbdefbfbd4cefbfbdefbfbd14efbfbdefbfbd6b68efbfbd0f16efbfbd2501efbfbdefbfbd61efbfbd4f34efbfbdefbfbdefbfbdcb9d0cefbfbd0befbfbdefbfbd'
        // FIXME, why each time we have a different signature result?
        assert.strictEqual(signature, expected)
    })
    it('delete', async function () {
        this.timeout(400000)
        await keyOpt.delete(keyName, {sync: true})
        await keyOpt.delete(keyName, {force: true})
    })

})
describe('key RSA', () => {
    const keyName = 'RSA'
    const keyType = KeyType.RSA

    const keyOpt = new Key(vaultName, configFileCredential)
    it('create', async () => {
        await keyOpt.create(keyName, keyType)
    })
    it('get', async () => {
        const keyInfo = await keyOpt.get(keyName)
        console.log(keyInfo)
    })
    let cipherResult
    it('encrypt', async function () {
        this.timeout(40000)
        const cryptoOperator = await keyOpt.asCrypto(keyName)
        cipherResult = await cryptoOperator.encrypt('abc')

    })
    it('decrypt', async function () {
        this.timeout(40000)
        const cryptoOperator = await keyOpt.asCrypto(keyName)
        const result = await cryptoOperator.decrypt(cipherResult)
        console.debug(result)
    })
})
