export default class Game {
    selected = -1;
    paused = false;
    grid = null;
    constructor(grid) {
        this.grid = grid;
    }
    DrawGame(mapa, creatures) {
        if (this.grid == null) {
            return;
        }
        for (var i = 0; i < mapa.length; i++) {
            for (var j = 0; j < mapa[0].length; j++) {
                if (mapa[i][j].Char == "#") {
                    this.grid.Fill(j, i, "white");
                }
                else if (mapa[i][j].Char == "*") {
                    this.grid.Fill(j, i, "blue");
                }
                else if (mapa[i][j].Char == ".") {
                    this.grid.Fill(j, i, "green");
                }
            }
        }
        for (let i = 0; i < creatures.length; i++) {
            const cr = creatures[i];
            let x = cr.memory.x.value;
            let y = cr.memory.y.value;
            this.grid.Fill(x, y, "black");
        }
    }
    AddEntity(com, name) {
        const canvas = document.querySelector("canvas");
        if (canvas == null) {
            return;
        }
        canvas.addEventListener("click", (event) => {
            const sz = this.grid?.pix;
            if (sz == undefined) {
                return;
            }
            const posx = Math.floor((event.offsetX) / sz);
            const posy = Math.floor((event.offsetY) / sz);
            com.AddEntity(name, posx, posy);
            console.log("aqui: ", posx, posy);
        }, { once: true });
    }
    Pause() {
        this.paused = true;
    }
    Continue() {
        this.paused = false;
    }
    Step(com) {
        com.Step();
    }
    Place(x, y, obj) {
        if (this.grid == null) {
            return;
        }
        this.grid.Fill(x, y);
    }
}
