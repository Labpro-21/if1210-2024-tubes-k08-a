import fs from "fs/promises";

(async () => {
	const p = (...args) => new URL(String.raw(...args), "https://gracidea.lecoq.io");
	const worldTileset = await (await fetch(p`/textures/rse/tileset.json?sha=1dd0121`)).json();
	const npcsTileset = await (await fetch(p`/textures/rse/npcs.json?sha=1dd0121`)).json();
	const creaturesTileset = await (await fetch(p`/textures/rse/creatures.json?sha=1dd0121`)).json();
	const worldTilesetImage = Buffer.from(await (await fetch(p`/textures/rse/${worldTileset.meta.image}`)).arrayBuffer());
	const npcsTilesetImage = Buffer.from(await (await fetch(p`/textures/rse/${npcsTileset.meta.image}`)).arrayBuffer());
	const creaturesTilesetImage = Buffer.from(await (await fetch(p`/textures/rse/${creaturesTileset.meta.image}`)).arrayBuffer());
	const tileset = Object.fromEntries([
		...Object.entries(worldTileset.frames).map(([k, v]) => [k, { ...v, source: "world" }]),
		...Object.entries(npcsTileset.frames).map(([k, v]) => [k, { ...v, source: "npc" }]),
		...Object.entries(creaturesTileset.frames).map(([k, v]) => [k, { ...v, source: "creature" }])
	]);
	await fs.writeFile("tileset.json", JSON.stringify(tileset));
	await fs.writeFile("worldTilesetImage.webp", worldTilesetImage);
	await fs.writeFile("npcsTilesetImage.webp", npcsTilesetImage);
	await fs.writeFile("creaturesTilesetImage.webp", creaturesTilesetImage);

	const worldsheet = [{}, {}, {}, {}, {}];
	const regions = (await (await fetch(p`/data/maps.json`)).json()).regions;
	for(const region of regions) {
		const regionId = region.id;
		const sections = (await (await fetch(p`/data/maps/${regionId}.json`)).json()).sections;
		await Promise.all(sections.map(async section => {
			const sectionId = section.id;
			const sectionX = section.x;
			const sectionY = section.y;
			const sectionWidth = section.width;
			const sectionHeight = section.height;
			const chunksData = (await (await fetch(p`/data/maps/${sectionId}.json`)).json());
			for(const chunk of chunksData.chunks) {
				const chunkId = chunk.id;
				const chunkLayer = chunk.layer - 1;
				const chunkTiles = chunk.tiles;
				const chunkX = chunk.x;
				const chunkY = chunk.y;
				if(isNaN(chunkLayer))
					continue
				for(let i = 0; i < chunkTiles.length; i++) {
					const tile = chunkTiles[i];
					const worldX = `${(i % 16) + chunkX + sectionX}`
					const worldY = `${Math.floor(i / 16) + chunkY + sectionY}`
					if(worldsheet[chunkLayer][worldY] == null)
						worldsheet[chunkLayer][worldY] = {}
					worldsheet[chunkLayer][worldY][worldX] = { tile: tile, region: regionId, section: sectionId };
				}
			}
		}))
	}
	const layersBounds = worldsheet.map(l => {
		const ordinate = Object.keys(l).map(y => parseInt(y)).reduce(([a, b], c) => [Math.min(a, c), Math.max(b, c)], [Infinity, -Infinity]);
		const abscissa = Object.values(l).map(r => Object.keys(r).map(x => parseInt(x)).reduce(([a, b], c) => [Math.min(a, c), Math.max(b, c)], [Infinity, -Infinity])).reduce(([a, b], [c, d]) => [Math.min(a, c), Math.max(b, d)], [Infinity, -Infinity]);
		return [abscissa[0], ordinate[0], abscissa[1] - abscissa[0] + 1, ordinate[1] - ordinate[0] + 1]
	});
	const totalBounds = layersBounds.reduce(([x, y, w, h], [a, b, c, d]) => [Math.min(x, a), Math.min(y, b), Math.max(w, c), Math.max(h, d)], [Infinity, Infinity, -Infinity, -Infinity])
	const newLayerBounds = worldsheet.map(layer => {
		const newLayer = new Array(totalBounds[3]).fill(null).map(() => new Array(totalBounds[2]).fill(null));
		for(const ys of Object.keys(layer)) {
			const y = parseInt(ys) - totalBounds[1];
			for(const xs of Object.keys(layer[ys])) {
				const x = parseInt(xs) - totalBounds[0];
				newLayer[y][x] = layer[ys][xs];
			}
		}
		return newLayer;
	});
	await fs.writeFile("worldsheet.json", JSON.stringify({
		width: totalBounds[2],
		height: totalBounds[3],
		layers: JSON.stringify(newLayerBounds)
	}));
})();
