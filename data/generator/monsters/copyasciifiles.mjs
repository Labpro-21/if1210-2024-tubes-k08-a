import fs from "fs/promises";
import fs0 from "fs";
import path from "path";
import url from 'url';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

(async () => {
	const directories = await fs.readdir(path.join(__dirname, "sprites/"));
	for(let i = 0; i < directories.length; i += 10) {
		const directoriesBatch = directories.slice(i, i + 10);
		await Promise.all(directoriesBatch.map(async directoryName => {
			const directory = path.join(__dirname, "sprites/", directoryName);
			const files = (await fs.readdir(directory))
				.filter(f => f.endsWith(".png.txt") || f.endsWith(".gif.txt"));
			await Promise.all(files.map(async fileName => {
				const file = path.join(directory, fileName);
				const destination = path.join(__dirname, "../../assets/monsters", fileName);
				console.log(`copying ${file} to ${destination}`)
				await fs.copyFile(file, destination);
			}));
		}));
	}
})();
