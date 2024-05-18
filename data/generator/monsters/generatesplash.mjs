import fs from "fs/promises";
import fs0 from "fs";
import path from "path";
import sharp from "sharp";
import { spawn } from "child_process";

const artCharacters = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@".split("");
const artDarkness = [0, 0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037, 1];
const generateAsciiArt = (image, width, height, invert) => {
	let line;
	const result = [];
	for(let y = 0; y < height; y++) {
		let lastR = null;
		let lastG = null;
		let lastB = null;
		line = "";
		for(let x = 0; x < width; x++) {
			const index = (y * width + x) * 4;
			const r = image[index + 0] / 255;
			const g = image[index + 1] / 255;
			const b = image[index + 2] / 255;
			const a = image[index + 3] / 255;
			const brightness = Math.sqrt(0.299 * r * r + 0.587 * g * g + 0.114 * b * b);
			const darkness = a * (invert ? brightness : 1 - brightness);
			const darknessIndex = Math.max(1, artDarkness.findIndex(d => d >= darkness));
			const lighterValue = artDarkness[darknessIndex - 1];
			const darkerValue = artDarkness[darknessIndex];
			const darknessMiddle = (darkerValue - lighterValue) / 2 + lighterValue;
			const character = artCharacters[darkness > darknessMiddle ? darknessIndex : darknessIndex - 1];
			if(character == " ") {
				if(invert && (lastR != null || lastG != null || lastB != null)) {
					lastR = null;
					lastG = null;
					lastB = null;
					line += "§a|"
				}
				line += " ";
				continue;
			}
			const newAttributes = [];
			if(a != 0 && r != lastR && g != lastG && b != lastB) {
				lastR = r; lastG = g; lastB = b;
				const charR = String.fromCharCode(Math.floor(r * 255));
				const charG = String.fromCharCode(Math.floor(g * 255));
				const charB = String.fromCharCode(Math.floor(b * 255));
				newAttributes.push(`${invert ? "s" : "w"}${btoa(charR + charG + charB).replaceAll("=", "")}`)
			}
			if(a != 0 && r != lastR && g != lastG) {
				lastR = r; lastG = g;
				const charR = String.fromCharCode(Math.floor(r * 255));
				const charG = String.fromCharCode(Math.floor(g * 255));
				newAttributes.push(`${invert ? "d" : "e"}${btoa(charR + charG).replaceAll("=", "")}`);
			}
			if(a != 0 && g != lastG && b != lastB) {
				lastG = g; lastB = b;
				const charG = String.fromCharCode(Math.floor(g * 255));
				const charB = String.fromCharCode(Math.floor(b * 255));
				newAttributes.push(`${invert ? "f" : "r"}${btoa(charG + charB).replaceAll("=", "")}`);
			}
			if(a != 0 && b != lastB && r != lastR) {
				lastB = b; lastR = r;
				const charB = String.fromCharCode(Math.floor(b * 255));
				const charR = String.fromCharCode(Math.floor(r * 255));
				newAttributes.push(`${invert ? "g" : "t"}${btoa(charB + charR).replaceAll("=", "")}`);
			}
			if(a != 0 && r != lastR) {
				lastR = r;
				const charR = String.fromCharCode(Math.floor(r * 255));
				newAttributes.push(`${invert ? "h" : "y"}${btoa(charR).replaceAll("=", "")}`);
			}
			if(a != 0 && g != lastG) {
				lastG = g;
				const charG = String.fromCharCode(Math.floor(g * 255));
				newAttributes.push(`${invert ? "j" : "u"}${btoa(charG).replaceAll("=", "")}`);
			}
			if(a != 0 && b != lastB) {
				lastB = b;
				const charB = String.fromCharCode(Math.floor(b * 255));
				newAttributes.push(`${invert ? "k" : "i"}${btoa(charB).replaceAll("=", "")}`);
			}
			if(newAttributes.length > 0) line += `§${newAttributes.join(",")}|`
			line += character;
		}
		result.push(line);
	}
	return result.join("\n");
}

(async () => {
	const directories = await fs.readdir("sprites/");
	for(let i = 0; i < directories.length; i += 10) {
		const directoriesBatch = directories.slice(i, i + 10);
		await Promise.all(directoriesBatch.map(async directoryName => {
			const directory = path.join("sprites", directoryName);
			const files = (await fs.readdir(directory)).filter(f => !f.includes(".imconver.png") && f.endsWith(".gif") || f.endsWith(".png"));
			await Promise.all(files.map(async fileName => {
				const file = path.join(directory, fileName);
				try {
					if(file.endsWith(".png")) {
						console.log(`Converting & generating ${file}`);
						let buffer;
						for(let j = 0; j < 3; j++) {
							buffer = await fs.readFile(file);
							if(buffer.length > 0) break;
							console.log(`Retrying reading file ${file}`);
						}
						const image = sharp(buffer);
						const meta = await image.metadata();
						const sizeW = Math.floor(meta.width / 2);
						const sizeH = Math.floor(meta.height / 4);
						const imageBuffer = await image.ensureAlpha().resize({ width: sizeW, height: sizeH, fit: "contain" }).raw().toBuffer();
						const ascii = generateAsciiArt(imageBuffer, sizeW, sizeH, true);
						const asciiFile = path.join(directory, fileName + ".txt");
						await fs.writeFile(asciiFile, ascii);
					}
					if(file.endsWith(".gif")) {
						console.log(`Converting ${file}`);
						const imconvertProcess = spawn(`imconvert.bat`, ["-coalesce", file, `${directory}/${path.basename(file)}.%05d.imconvert.png`]);
						imconvertProcess.stdout.pipe(process.stdout);
						imconvertProcess.stderr.pipe(process.stderr);
						await new Promise(r => imconvertProcess.on("close", r));
						await new Promise(r => setTimeout(r, 500));
						if(imconvertProcess.exitCode != 0)
							throw new Error("Imconvert non zero exit");
						const convertedFiles = (await fs.readdir(directory)).filter(n => n.startsWith(path.basename(file) + ".") && n.endsWith(".imconvert.png")).sort();
						const asciis = [];
						await Promise.all(convertedFiles.map(async convertedFileName => {
							const convertedFile = path.join(directory, convertedFileName);
							console.log(`Generating ${convertedFile}`);
							let buffer;
							for(let j = 0; j < 3; j++) {
								buffer = await fs.readFile(convertedFile);
								if(buffer.length > 0) break;
								console.log(`Retrying reading file ${convertedFile}`);
							}
							const image = sharp(buffer);
							const meta = await image.metadata();
							const sizeW = Math.floor(meta.width / 2);
							const sizeH = Math.floor(meta.height / 4);
							const imageBuffer = await image.ensureAlpha().resize({ width: sizeW, height: sizeH, fit: "contain" }).raw().toBuffer();
							const ascii = generateAsciiArt(imageBuffer, sizeW, sizeH, true);
							asciis.push(ascii);
							await fs.unlink(convertedFile);
							const dumpFile = path.join(directory, `${convertedFileName}.txt`);
							if(fs0.existsSync(dumpFile))
								await fs.unlink(dumpFile);
						}));
						const combinedAsciiFile = path.join(directory, fileName + ".txt");
						const combinedAscii = asciis.map(a => a.split("\n").map(l => l.includes(";") ? `"${l}"` : l).join(";")).join("\n");
						await fs.writeFile(combinedAsciiFile, combinedAscii);
					}
				} catch(e) {
					throw new Error(`Error while generating ${file}, ${e.stack || e.message || e}`);
				}
			}))
		}));
	}
})();
