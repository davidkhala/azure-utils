export async function all(list, callbackFn = (_) => _) {
	const values = [];
	for await (const value of list) {
		values.push(callbackFn(value));
	}
	return values;
}
