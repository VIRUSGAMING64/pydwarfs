import Communication from "./com.js"
class Drawler{
    pix: number
    ctx: CanvasRenderingContext2D
    sizex: number
    sizey: number
    
    constructor(ctx: CanvasRenderingContext2D, pixels: number, sizex: number,sizey: number){
        this.pix = pixels
        this.ctx = ctx
        this.sizex = sizex
        this.sizey = sizey
    }
    
    FillMatrix(){
        let color = "green"
        for(let i = 0; i < this.sizex; i++){
            for(let j = 0; j < this.sizey; j++){
                this.Fill(i,j, color)
            }   
        }
    }

    Fill(px :number,py :number, color = "black", border = "red"){
        px = px * this.pix
        py = py * this.pix
        this.ctx.beginPath()
        this.ctx.rect(px, py, this.pix, this.pix)
        this.ctx.strokeStyle = border
        this.ctx.fillStyle = color
        this.ctx.fillRect(px,py, this.pix, this.pix)
        this.ctx.strokeRect(px,py, this.pix, this.pix)
    }

    SetPos(x :number,y :number, color = "black", border = "red") {
        let px = Math.floor(x / this.pix) 
        let py = Math.floor(y / this.pix)
        this.Fill(px,py,color, border)
    }

}

let canvas = document.createElement("canvas");

let elem = document.getElementById("draw")
if (elem != null){
    elem.appendChild(canvas);
}

canvas.width = Math.max(window.innerWidth, window.innerHeight);
canvas.height = Math.max(window.innerWidth, window.innerHeight);
let ctx = canvas.getContext("2d");
let com = new Communication("ws://127.0.0.1:9090");


if (ctx) {
    setInterval(() => {
        console.log(com.Send("SHOW"));
        let data = com.Recive();
        if (data.data == undefined) {
            return;
        }
        let obj = JSON.parse(data.data);
        let mapa = obj.maps[0].Grid;

        let sizex =  mapa[0].length
        let sizey =  mapa.length
        let len = Math.max(sizex,sizey);
        let pixsz = Math.max(window.innerWidth, window.innerHeight) / len;

        canvas.width = pixsz * sizex;
        canvas.height = pixsz * sizey;

        let conf = new Drawler(ctx, pixsz,sizex, sizey);
        conf.FillMatrix();
        canvas.addEventListener("mousedown", (ev) => {
            let x = ev.offsetX;
            let y = ev.offsetY;
            console.log(x, y);
            conf.SetPos(x, y, "blue");
        });
        for (var i = 0; i < mapa.length; i++) {
            for (var j = 0; j < mapa[0].length; j++) {
                if (mapa[i][j].Char == "#") {
                    conf.Fill(j, i, "white");
                }
                else if (mapa[i][j].Char == "*") {
                    conf.Fill(j, i, "blue");
                }
            }
        }
    }, 1000 / 5);
}
