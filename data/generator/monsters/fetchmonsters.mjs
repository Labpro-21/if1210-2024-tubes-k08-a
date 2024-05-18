import { parse } from 'node-html-parser';
import { decode } from 'html-entities';
import fs from "fs/promises";

(async () => {
	const origin = "https://pokemondb.net";
	const p = (...args) => new URL(String.raw(...args), origin);
	const pokedexPage = parse(await (await fetch(p`/pokedex/all`)).text());
	const pokedexRows = pokedexPage.querySelectorAll("#pokedex > tbody > tr");

	const monsters = [];
	for(const pokedexRow of pokedexRows) {
		const monsterId = parseInt(pokedexRow.querySelector("td:nth-child(1)").innerText) - 1;
		if(monsters.some(m => m.id == monsterId)) continue;
		const monsterStrId = pokedexRow.querySelector("td:nth-child(2) > a").getAttribute("href").slice(`/pokedex/`.length);
		const monsterName = pokedexRow.querySelector("td:nth-child(2) > a").innerText;
		const monsterElements = pokedexRow.querySelector("td:nth-child(3)").innerText.split("\n").map(e => e.trim()).filter(e => e.length > 0);
		const monsterHP = parseInt(pokedexRow.querySelector("td:nth-child(4)").innerText);
		const monsterAttack = parseInt(pokedexRow.querySelector("td:nth-child(5)").innerText);
		const monsterDefense = parseInt(pokedexRow.querySelector("td:nth-child(6)").innerText);
		monsters.push({
			id: monsterId,
			strId: monsterStrId,
			name: monsterName,
			elements: monsterElements,
			healthPoints: monsterHP,
			attackPower: monsterAttack,
			defensePower: monsterDefense,
			level: 1,
			familiy: monsterStrId,
			description: "",
			spriteDefault: `monsters/${monsterStrId}.png.txt`,
			spriteFront: `monsters/${monsterStrId}_normal.gif.txt`,
			spriteBack: `monsters/${monsterStrId}_back.gif.txt`
		});
	}

	const evolutionPage = parse(await (await fetch(p`/evolution`)).text());
	const evolutionRows = evolutionPage.querySelectorAll(".infocard-list-evo");
	for(const evolutionRow of evolutionRows) {
		const monsterEvolutionIds = [...evolutionRow.querySelectorAll(".ent-name")].map(e => e.getAttribute("href").slice(`/pokedex/`.length));
		let i = 0;
		for(const monsterEvolutionId of monsterEvolutionIds) {
			const monster = monsters.find(m => m.strId == monsterEvolutionId);
			if(monster.familiy != null) continue;
			monster.level = ++i;
			monster.familiy = monsterEvolutionIds[0];
		}
	}

	for(let i = 0; i < monsters.length; i += 10) {
		const monstersChunk = monsters.slice(i, i + 10);
		await Promise.all(monstersChunk.map(async monster => {
			console.log(`fetching ${p`/pokedex/${monster.strId}`}`);
			const monsterPage = parse(await (await fetch(p`/pokedex/${monster.strId}`)).text());
			const paragraphs = [...monsterPage.querySelectorAll("#main > p")].map(d => d.innerText).filter(d => d.includes(monster.name));
			const description = paragraphs.map(p => decode(p)).join("\n").replaceAll("\\", "\\\\").replaceAll("\"", "\\\"").replaceAll("\n", "\\n");
			monster.description = description;
		}));
		await new Promise(r => setTimeout(r, 500));
	}

	console.log(monsters);
	const csv = monsters.map(m => [
		m.id, 
		m.name, 
		`"${m.description}"`, 
		m.familiy, 
		m.level, 
		m.healthPoints, 
		m.attackPower, 
		m.defensePower,
		m.spriteDefault,
		m.spriteFront,
		m.spriteBack
	].join(";")).join("\n");
	await fs.writeFile("database_monster.csv", csv);
})();
