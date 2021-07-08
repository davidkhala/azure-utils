const {Key, KeyType} = require('../index')
const {getConfigFileCredential} = require('../../login')

describe('key', () => {
    const vaultName = 'davidkhala-vault'
    const keyName = 'myKey'
    const keyType = KeyType.EC
    const configFileCredential = getConfigFileCredential()
    const keyOpt = new Key(vaultName, configFileCredential)
    it('create', async function () {
        this.timeout(40000)
        await keyOpt.create(keyName, keyType)
    })
    it('delete', async function () {
        this.timeout(400000)
        await keyOpt.delete(keyName, {sync: true})
        await keyOpt.delete(keyName, {force: true})
    })
})
