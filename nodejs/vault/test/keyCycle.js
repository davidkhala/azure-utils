const {Key, KeyType} = require('../index')
const {getConfigFileCredential} = require('../../login')
const vaultName = 'davidkhala-vault'
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
