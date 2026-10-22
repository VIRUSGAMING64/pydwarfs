import Communication from "./com.js"
import Drawler from "./grid.js"
import Game from "./game.js";

import { GetCreatures, RawData, GetMaps, GetRunningCreatures} from "./utils.js"; "./utils"

let canvas = document.createElement("canvas");

let elem = document.getElementById("draw")
if (elem != null){
    elem.appendChild(canvas);
}

canvas.width = Math.max(window.innerWidth, window.innerHeight);
canvas.height = Math.max(window.innerWidth, window.innerHeight);
let ctx = canvas.getContext("2d");
let com = new Communication("ws://127.0.0.1:9090");

let BaseGame: Game|null=null
let conf :Drawler|null = null

function RenderizeScreen(forse = false){
    let creatures,data, mapa 
    if (BaseGame == null || !BaseGame.paused || forse){ //* Aqui se hace fetch desde el server
        data = RawData(com)
        if (data == ""){
            return false
        }
        mapa = GetMaps(data)[0].Grid
        creatures = GetCreatures(data)
        if (BaseGame == null){
            const menu = document.getElementById("menu")
            for(let i = 0; i < creatures.length; i+=1){
                let c = creatures[i]
                let button = document.createElement("button")
                const name = c.memory.creature.name
                button.innerText = name
                button.className="w-30 h-8 m-1 gap-1 text-white bg-gray-900"
                button.onclick = () => {
                    //Aqui quiero agregar un coso  
                    const LocalName = name
                    BaseGame?.AddEntity(com,name)
                }
                menu?.appendChild(button)
            }
        }
    }
        
    if (conf == null){
        let sizex =  mapa[0].length
        let sizey =  mapa.length
        let len = Math.max(sizex,sizey);
        let pixsz = Math.max(window.innerWidth, window.innerHeight) / len;
        canvas.width = pixsz * sizex;
        canvas.height = pixsz * sizey;    
        conf = new Drawler(ctx, pixsz,sizex, sizey);
    }

    if (BaseGame == null){
        BaseGame = new Game(conf)
    }else{
        BaseGame.grid = conf
    }
    if (BaseGame.paused && !forse){
        return false
    }
    creatures = GetRunningCreatures(data)
    BaseGame.DrawGame(mapa, creatures)
    return true
}

setInterval(() => {
    if (BaseGame == null){
        let val = RenderizeScreen(true)
        while(val) {
            val = RenderizeScreen(true)
        }
    }else if(!BaseGame?.paused) {
        BaseGame?.Step(com)
        let val = RenderizeScreen()
        while(val) {
            val = RenderizeScreen()
        }
    }
}, 100/6);

function Continue(){
    if (BaseGame == null){
        return
    }
    BaseGame.Continue()
}
function Pause(){
    if (BaseGame == null){
        return
    }
    BaseGame.Pause()
}
function Step(){
    if (BaseGame == null){
        return
    }
    BaseGame.Step(com)
    let val = RenderizeScreen(true)
    while(val) {
        val = RenderizeScreen(true)
    }
}

document.getElementById("btn-continue")?.addEventListener("click", Continue);
document.getElementById("btn-pause")?.addEventListener("click", Pause);
document.getElementById("btn-step")?.addEventListener("click", Step);
const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');

// Añadir evento de clic al botón
toggleBtn?.addEventListener('click', () => {
    sidebar?.classList.toggle('collapsed');
});