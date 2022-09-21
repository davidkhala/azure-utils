export async function all(list) {
	const values = [];
	for await (const value of list) {
		values.push(value);
	}
	return values;
}

export class Azure {
	constructor(credential, logger = console) {
		Object.assign(this, {logger, credential});
	}
}