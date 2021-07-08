const {Key, KeyType} = require('../index')
const {getConfigFileCredential} = require('../../login')

describe('key', () => {
    it('life cycle', async function () {
        this.timeout(40000)
        const vaultName = 'davidkhala-vault'
        const keyName = 'myKey'
        const keyType = KeyType.EC
        const configFileCredential = getConfigFileCredential()
        const keyOpt = new Key(vaultName, configFileCredential)

        await keyOpt.create(keyName, keyType)
        await keyOpt.delete(keyName, true)
    })
})
