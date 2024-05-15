import path from "path";
import fs from "fs/promises";

const __dirname = process.cwd();

(async () => {
	const files = ["console.py", "driver_std.py", "views.py"];
	let result = "";
	for(const file of files) {
		const moduleName = file.split(".")[0];
		const contents = await fs.readFile(path.join(__dirname, file));
		const regex = /^(?:(_[A-Z][^\s]*)|def\s*(_[^\s(]*))/gm;
		const exports = [];
		let matcher;
		while((matcher = regex.exec(contents)) != null)
			exports.push(matcher[1] || matcher[2]);
		result += `from .${moduleName} import ${exports.join(", ")}\n\n`;
		result += `${exports.map(e => `${e.slice(1)} = ${e}`).join("\n")}\n\n`
	}
	await fs.writeFile(path.join(__dirname, "__init__.py"), result.trim() + "\n");
	console.log(result);
})();
