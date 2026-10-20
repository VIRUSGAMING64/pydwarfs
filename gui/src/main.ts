import Communication from "./com.js"
import Drawler from "./grid.js"
import Game from "./game.js";

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


function RawData(){
        console.log(com.Show());
    let data = com.Recive();
    if (data.data == undefined) {
        return "";
    }
    return data.data
}

function GetCreatures(rawstr: string){
    let obj = JSON.parse(rawstr)
    return obj.creatures
}

function GetMaps(rawstr: string){
    let obj = JSON.parse(rawstr);
    return obj.maps
}



function RenderizeScreen(forse = false){
    let creatures,data, mapa 
    if (BaseGame == null || !BaseGame.paused || forse){ //* Aqui se hace fetch desde el server
        data = RawData()
        if (data == ""){
            return
        }
        mapa = GetMaps(data)[0].Grid
        creatures = GetCreatures(data)
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
        console.log("juego pausado")
        return
    }
    BaseGame.DrawGame(mapa, creatures)
}

setInterval(() => {
    if(!BaseGame?.paused) {
        BaseGame?.Step(com)
        RenderizeScreen()
    }
}, 1000 / 60);











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
    console.log("haciendo un step manual")
    BaseGame.Step(com)
    RenderizeScreen(true)
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