import fs from "fs/promises"
import fs0 from "fs"
import path from "path"
import url from "url"

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

(async () => {
	const monsters = JSON.parse(await fs.readFile(path.join(__dirname, "../monsters/og-database_monster.json"), "utf-8"))
		.filter(m => fs0.existsSync(path.join(__dirname, "../../assets/", m.spriteDefault)));
	const families = [...new Set(monsters.map(m => m.family))];
	const upgradeOptions = [];
	for(const family of families) {
		let currentLevel = 1;
		let lastMonster = null;
		while(true) {
			const currentMonster = monsters.find(m => m.family == family && m.level == currentLevel);
			if(currentMonster == null)
				break;
			if(lastMonster == null) {
				currentLevel++;
				lastMonster = currentMonster;
				continue;
			}
			let cost = 0;
			cost += (currentMonster.healthPoints - lastMonster.healthPoints) * 2.2;
			cost += (currentMonster.attackPower - lastMonster.attackPower) * 14.2;
			cost += (currentMonster.defensePower - lastMonster.defensePower) * 11.7;
			cost = Math.round(cost / 75) * 75;
			cost = Math.max(300, cost);
			upgradeOptions.push({
				fromMonsterId: lastMonster.id,
				toMonsterId: currentMonster.id,
				cost: cost
			});
			currentLevel++;
			lastMonster = currentMonster;
		}
	}

	const csv = upgradeOptions.map((u, i) => [i, u.fromMonsterId, u.toMonsterId, u.cost].join(";")).join("\n");
	await fs.writeFile(path.join(__dirname, "laboratory.csv"), csv);
})();
