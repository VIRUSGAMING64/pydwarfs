import Communication from "./com.js";
import { GetMaps, RawData } from "./utils.js";

type GameMap = { Name?: string; Grid?: unknown[][] };
const com = new Communication("ws://127.0.0.1:9090");
const status = document.getElementById("map-status") as HTMLParagraphElement;
const list = document.getElementById("map-list") as HTMLUListElement;
let lastMapsSignature = "";

function renderMaps(maps: GameMap[]): void {
	list.replaceChildren();
	status.textContent = maps.length
		? `${maps.length} mapa${maps.length === 1 ? "" : "s"} disponible${maps.length === 1 ? "" : "s"}`
		: "No hay mapas cargados.";
	if (!maps.length) {
		const empty = document.createElement("li");
		empty.className = "col-span-full border-l-4 border-emerald-400 bg-slate-900/80 p-5 text-slate-400";
		empty.textContent = "El juego no tiene mapas disponibles en este momento.";
		list.appendChild(empty);
		return;
	}
	maps.forEach((map, index) => {
		const height = map.Grid?.length ?? 0;
		const width = height ? map.Grid?.[0]?.length ?? 0 : 0;
		const item = document.createElement("button");
		item.type = "button";
		item.className = "group w-full cursor-pointer border border-slate-700 bg-slate-900/90 p-5 text-left shadow-xl shadow-black/20 focus:outline-none focus:ring-2 focus:ring-emerald-400 active:scale-[0.98] active:bg-emerald-950";
		const name = document.createElement("span");
		name.className = "mb-3 block text-xl font-semibold text-emerald-100";
		name.textContent = map.Name?.trim() || `Mapa ${index + 1}`;
		const size = document.createElement("span");
		size.className = "m-0 block text-slate-400";
		size.textContent = `Tamaño: ${width} × ${height} casillas`;
		item.append(name, size);
		item.onclick = () => {
			com.LoadMap(map.Name);
			window.location.href = `${window.location.origin}${window.location.pathname}game`;
		};
		list.appendChild(item);
	});
}

function updateMaps(): void {
	const rawData = RawData(com);
	if (!rawData) return;
	try {
		const maps = GetMaps(rawData) as GameMap[];
		const signature = JSON.stringify(maps);
		if (signature === lastMapsSignature) return;
		lastMapsSignature = signature;
		renderMaps(maps);
	} catch {
		status.textContent = "No se pudieron leer los mapas.";
	}
}

setInterval(updateMaps, 150);
