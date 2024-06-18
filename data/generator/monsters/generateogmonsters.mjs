// THIS IS A HACK TO CONFORM THE RULES.
import fs from "fs/promises";
import fs0 from "fs";
import url from 'url';
import path from "path";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

(async () => {
	const monsters = JSON.parse(await fs.readFile(path.join(__dirname, "database_monster.json")))
		.filter(m => fs0.existsSync(path.join(__dirname, "../../assets/", m.spriteDefault)));
	const families = [...new Set(monsters.map(m => m.family))].filter(f => monsters.filter(m => m.family == f).length >= 3);

	const newMonsters = [];
	for(const family of families) {
		const sameFamilies = monsters.filter(m => m.family == family).sort((a, b) => a.level - b.level);
		const baseMonster = sameFamilies[0]
		for(let i = 0; i < 5; i++) {
			const m = sameFamilies[i];
			if(i == 0) {
				m.defensePower = Math.round(m.defensePower / 200 * 100);
				newMonsters.push(m);
				continue;
			}
			if(m != null) {
				newMonsters.push({
					...m,
					healthPoints: Math.round(baseMonster.healthPoints * (1 + i * 0.1)),
					attackPower: Math.round(baseMonster.attackPower * (1 + i * 0.1)),
					defensePower: Math.min(50, Math.round(baseMonster.defensePower * (1 + i * 0.1))),
				});
				continue;
			}
			const lastMonster = sameFamilies[sameFamilies.length - 1];
			newMonsters.push({
				...lastMonster,
				strId: `${lastMonster.strId}-${i - sameFamilies.length}`,
				name: `${lastMonster.name}-${i - sameFamilies.length + 1}`,
				level: i + 1,
				healthPoints: Math.round(baseMonster.healthPoints * (1 + i * 0.1)),
				attackPower: Math.round(baseMonster.attackPower * (1 + i * 0.1)),
				defensePower: Math.min(50, Math.round(baseMonster.defensePower * (1 + i * 0.1))),
			});
		}
	}
	newMonsters.forEach((m, i) => m.id = i);
	monsters.splice(0, monsters.length, ...newMonsters);

	await fs.writeFile(path.join(__dirname, "og-database_monster.json"), JSON.stringify(monsters, null, 4));

	const csv = monsters.map(m => [
		m.id, 
		m.name, 
		`"${m.description}"`, 
		m.family, 
		m.level, 
		m.healthPoints, 
		m.attackPower, 
		m.defensePower,
		m.spriteDefault,
		m.spriteFront,
		m.spriteBack
	].join(";")).join("\n");
	await fs.writeFile(path.join(__dirname, "og-database_monster.csv"), csv);
})()

