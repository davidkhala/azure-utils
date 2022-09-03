
export async function all(list) {
	const values = [];
	for await (const value of list) {
		values.push(value);
	}
	return values;
}
