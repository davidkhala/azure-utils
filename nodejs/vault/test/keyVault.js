import assert from 'assert';
import fs from 'fs';
import {Key, KeyType} from '../index.js';
import {getConfigFileCredential} from '@davidkhala/azure/login.js';

const vaultName = 'davidkhala-vault';
const configFileCredential = getConfigFileCredential();

describe('key: EC', function () {
	this.timeout(0);

	const keyName = 'EC';
	const keyType = KeyType.EC;

	const keyOpt = new Key(vaultName, configFileCredential);
	it('create', async () => {

		await keyOpt.create(keyName, keyType);
	});
	it('get', async () => {
		const list = await keyOpt.list();
		console.info({list});
		const keyInfo = await keyOpt.get(keyName);
		console.log(keyInfo);
	});
	it('sign and verify', async () => {

		const keyCrypto = await keyOpt.asCrypto(keyName);
		const message = 'My data';

		const signature = await keyCrypto.sign(message);
		const isValid = await keyCrypto.verify(message, signature);
		assert.ok(isValid);
	});
	it('sign with oversize payload', async () => {
		const message = fs.readFileSync('vault/test/artifacts/payload1660145372021');
		console.log(message.length);
		const keyCrypto = await keyOpt.asCrypto(keyName);

		const signature = await keyCrypto.sign(message);
		console.info(signature);
		const isValid = await keyCrypto.verify(message, signature);
		assert.ok(isValid);
	});
	it('delete', async () => {

		await keyOpt.delete(keyName, {sync: true});
		await keyOpt.delete(keyName, {force: true});
	});

});
describe('key RSA', function () {
	this.timeout(0);
	const keyName = 'RSA';
	const keyType = KeyType.RSA;

	const keyOpt = new Key(vaultName, configFileCredential);
	it('create', async () => {
		await keyOpt.create(keyName, keyType);
	});
	it('get', async () => {
		const keyInfo = await keyOpt.get(keyName);
		console.log(keyInfo);
	});
	let cipherResult;
	it('encrypt', async () => {
		const cryptoOperator = await keyOpt.asCrypto(keyName);
		cipherResult = await cryptoOperator.encrypt('abc');

	});
	it('decrypt', async () => {
		const cryptoOperator = await keyOpt.asCrypto(keyName);
		const result = await cryptoOperator.decrypt(cipherResult);
		console.debug(result);
	});
	it('delete', async () => {

		await keyOpt.delete(keyName, {sync: true});
		await keyOpt.delete(keyName, {force: true});
	});
});
