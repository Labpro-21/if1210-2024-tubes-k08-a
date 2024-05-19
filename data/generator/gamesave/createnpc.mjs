import fs from "fs/promises"
import fs0 from "fs"
import path from "path"
import url from "url"

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

// https://nintendo.fandom.com/wiki/Category:Pok%C3%A9mon_trainers
// [...document.querySelectorAll("#content .category-page__member-link")].map(v => v.innerText).filter(t => !t.includes("("))
const trainerNames = ["Aarune","Acerola","Adaman","Agatha","Madoka Akagi","Akari","Alder","Allister","Amarys","Amethio","Anabel","Archie","Ardos","Argenta","Ariana","Arlo","Arven","Ash Ketchum","Atticus","Avery","AZ","Bea","Bede","Benga","Beni","Bertha","Bettie","Blaine","Blanche","Bonnie","Brandon","Brassius","Brawly","Brycen","Buck","Bugsy","Burgh","Byron","Caitlin","Calaba","Calem","Candela","Candice","Carmine","Cheren","Chili","Chobin","Chuck","Cilan","Clavell","Clemont","Colress","Crasher Wake","Cress","Cyllene","Cyndy","Darach","Dendra","Diantha","Drasna","Drayden","Drayton","Eldes","Elesa","Elio","Emmet","Erbie","Eri","Erika","Eusine","Evelyn","Exol","Faba","Falkner","Fantina","Flannery","Florian","Friede","Gaeric","Gardenia","Gary Oak","Geeta","Ghetsis","Giacomo","Glacia","Gladion","Goh","Gordie","Gorigan","Grant","Greevil","Greta","Grimsley","Grusha","Guzma","Hala","Hapu","Hassel","Hau","Helena","Hexagon Brothers","Hop","Ilima","Iono","Irida","Iscan","Jacq","Janine","John","Juan","Juliana","Kahili","Kali","Kamado","Karen","Katherine","Katy","Kiawe","Klara","Kofu","Koga","Korrina","Lacey","Lear","Lenora","Lian","Liko","Looker","Lorelei","Lovrina","Lt. Surge","Lucian","Lysandre","Mai","Marley","Marlon","Marnie","Maxie","Maylene","Mela","Melli","Melony","Michael","Milo","Mina"]

const randString = () => {
	return Math.random().toString(36).substr(2, 5)
}

(async () => {
	const monsters = JSON.parse(await fs.readFile(path.join(__dirname, "../monsters/database_monster.json"), "utf-8"))
		.filter(m => fs0.existsSync(path.join(__dirname, "../../assets/", m.spriteDefault)));
	const trainerUsers = [];
	const idOffset = 6;
	for(let i = 0; i < 27; i++) {
		const trainerNameIndex = Math.floor(trainerNames.length * Math.random());
		const [trainerName] = trainerNames.splice(trainerNameIndex, 1);
		const trainerUser = {
			id: i + idOffset,
			name: trainerName,
			password: randString() + randString() + randString(),
			role: "npc",
			money: 150 + Math.round(Math.random() * 400)
		}
		trainerUsers.push(trainerUser);
	}

	const trainerMonsterInventory = [];
	const trainerMonsterIdOffset = 1;
	let j = 0;
	for(let i = 0; i < trainerUsers.length; i++) {
		const trainerUser = trainerUsers[i];
		const monsterCount = 1 + Math.floor(Math.random() * 5);
		for(let k = 0; k < monsterCount; k++) {
			const monsterType = monsters[Math.floor(Math.random() * monsters.length)];
			const trainerMonster = {
				id: trainerMonsterIdOffset + j++,
				ownerId: trainerUser.id,
				referenceId: monsterType.id,
				name: monsterType.name,
				experiencePoints: 30 + Math.round(Math.random() * 600),
				healthPoints: monsterType.healthPoints + Math.floor((Math.random() * 2 - 1) * 0.3 * monsterType.healthPoints),
				attackPower: monsterType.attackPower + Math.floor((Math.random() * 2 - 1) * 0.3 * monsterType.attackPower),
				defensePower: monsterType.defensePower + Math.floor((Math.random() * 2 - 1) * 0.3 * monsterType.defensePower),
				activePotions: []
			}
			trainerMonsterInventory.push(trainerMonster);
		}
	}
	await fs.writeFile(
		path.join(__dirname, "npc_users.csv"), 
		trainerUsers.map(t => [t.id, t.name, t.password, t.role, t.money].join(";")).join("\n"),
		"utf-8"
	);
	await fs.writeFile(
		path.join(__dirname, "npc_inventory_monsters.csv"),
		trainerMonsterInventory.map(m => [m.id, m.ownerId, m.referenceId, m.name, m.experiencePoints, m.healthPoints, m.attackPower, m.defensePower, m.activePotions.join("|")].join(";")).join("\n"),
		"utf-8"
	)
})()
