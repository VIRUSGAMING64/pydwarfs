import Communication from "./com.js";
class Drawler {
    pix;
    ctx;
    size;
    constructor(ctx, pixels, size) {
        this.pix = pixels;
        this.ctx = ctx;
        this.size = size;
    }
    FillMatrix() {
        let color = "black";
        for (let i = 0; i < this.size * 2; i++) {
            for (let j = 0; j < this.size; j++) {
                this.Fill(i, j, color);
            }
        }
    }
    Fill(px, py, color = "black", border = "red") {
        px = px * this.pix;
        py = py * this.pix;
        this.ctx.beginPath();
        this.ctx.rect(px, py, this.pix, this.pix);
        this.ctx.strokeStyle = border;
        this.ctx.fillStyle = color;
        this.ctx.fillRect(px, py, this.pix, this.pix);
        this.ctx.strokeRect(px, py, this.pix, this.pix);
    }
    GetPos(x, y) {
        let px = Math.floor(x / this.pix);
        let py = Math.floor(y / this.pix);
        this.Fill(px, py);
    }
}
let mapsize = 30;
let pixsz = Math.max(window.innerWidth, window.innerHeight) / mapsize;
let canvas = document.createElement("canvas");
canvas.width = Math.max(window.innerWidth, window.innerHeight);
canvas.height = Math.max(window.innerWidth, window.innerHeight);
document.body.appendChild(canvas);
let ctx = canvas.getContext("2d");
console.log("ready");
let com = new Communication("ws://127.0.0.1:9090");
setInterval(() => {
    console.log(com.Recive());
}, 1000 / 30);
if (ctx) {
    let conf = new Drawler(ctx, pixsz, mapsize);
    conf.FillMatrix();
    window.addEventListener("mousedown", (ev) => {
        let x = ev.pageX;
        let y = ev.pageY;
        conf.GetPos(x, y);
    });
}
else {
    alert("El context es null !!!");
}
