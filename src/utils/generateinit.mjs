import path from "path";
import fs from "fs/promises";
import fs0 from "fs";

const __dirname = process.cwd();

(async () => {
	const directories = (await fs.readdir(__dirname))
		.filter(f => fs0.statSync(path.join(__dirname, f)).isDirectory() && !f.startsWith("_"))
		.map(d => path.join(__dirname, d));
	for(const directory of directories) {
		const files = (await fs.readdir(directory))
			.filter(f => fs0.statSync(path.join(directory, f)).isFile() && f.endsWith(".py") && f != "__init__.py" && !f.startsWith("_"))
			.map(f => path.join(directory, f));
		let result = "";
		for(const file of files) {
			const moduleName = path.basename(file).split(".")[0];
			const contents = await fs.readFile(file);
			const regex = /^(?:(_{0,1}[a-zA-Z][^\.\s]*)\s*=|def\s*(_{0,1}[a-zA-Z][^\.\s(]*))/gm;
			const exports = [];
			let matcher;
			while((matcher = regex.exec(contents)) != null)
				exports.push(matcher[1] || matcher[2]);
			if(exports.length == 0) {
				// result += `__import__("${moduleName}", globals(), locals(), [], level=1)`;
				continue
			}
			result += `from .${moduleName} import ${exports.join(", ")}\n\n`;
			result += `${exports.map(e => `${e.startsWith("_") ? e.slice(1) : e} = ${e}`).join("\n")}\n\n`
		}
		await fs.writeFile(path.join(directory, "__init__.py"), result.trim() + "\n");
		console.log(result);
	}
})();
