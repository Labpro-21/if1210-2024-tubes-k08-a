import { parse } from 'node-html-parser';
import fs from "fs/promises";
import fs0 from "fs";
import path from "path";

(async () => {
	const origin = "https://pokemondb.net";
	const p = (...args) => new URL(String.raw(...args), origin);
	const spritesPage = parse(await (await fetch(p`/sprites`)).text());
	const spriteLinks = [...spritesPage.querySelectorAll(".infocard")].map(s => s.getAttribute("href"));
	for(let i = 0; i < spriteLinks.length; i += 10) {
		const spriteLinksBatch = spriteLinks.slice(i, i + 10);
		await Promise.all(spriteLinksBatch.map(async spriteLink => {
			const monsterStrId = spriteLink.slice("/sprites/".length);
			const directory = path.join("sprites", monsterStrId);
			if(!fs0.existsSync(directory))
				await fs.mkdir(directory, { recursive: true });
			const spriteFile = path.join(directory, `${monsterStrId}.png`);
			if(fs0.existsSync(spriteFile)) return;
			const spritePage = parse(await (await fetch(p`${spriteLink}`)).text());
			const row = [...spritePage.querySelectorAll("tr")].filter(r => r.innerText.includes("Animated"))[0];
			if(row == null) return;
			const columnName = [...row.parentNode.parentNode.querySelectorAll("thead > tr > th")].map(c => c.innerText);
			const normalIndex = columnName.findIndex(c => c.toLowerCase().includes("normal"));
			const backIndex = columnName.findIndex(c => c.toLowerCase().includes("back"));
			const defaultImageSrc = `https://img.pokemondb.net/sprites/black-white/normal/${monsterStrId}.png`;
			const normalImageSrc = [...row.querySelectorAll("td")][normalIndex].querySelector("img").getAttribute("src");
			const backImageSrc = [...row.querySelectorAll("td")][backIndex].querySelector("img").getAttribute("src");
			console.log(`fetching ${p`${defaultImageSrc}`}`);
			console.log(`fetching ${p`${normalImageSrc}`}`);
			console.log(`fetching ${p`${backImageSrc}`}`);
			await Promise.all([
				(async () => await fs.writeFile(spriteFile, Buffer.from(await (await fetch(p`${defaultImageSrc}`)).arrayBuffer())))(),
				(async () => await fs.writeFile(path.join(directory, `${monsterStrId}_normal.gif`), Buffer.from(await (await fetch(p`${normalImageSrc}`)).arrayBuffer())))(),
				(async () => await fs.writeFile(path.join(directory, `${monsterStrId}_back.gif`), Buffer.from(await (await fetch(p`${backImageSrc}`)).arrayBuffer())))()
			])
		}));
	}
})();
