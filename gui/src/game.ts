import Communication from "./com";
import Drawler from "./grid";

export default class Game {
  selected = -1;
  paused = false;
  grid: Drawler | null = null;
  constructor(grid: Drawler) {
    this.grid = grid;
  }
  DrawGame(mapa: any, creatures: any) {
    if (this.grid == null) {
      return;
    }
    for (var i = 0; i < mapa.length; i++) {
      for (var j = 0; j < mapa[0].length; j++) {
        if (mapa[i][j].Char == "#") {
          this.grid.Fill(j, i, "white");
        } else if (mapa[i][j].Char == "*") {
          this.grid.Fill(j, i, "blue");
        } else if (mapa[i][j].Char == ".") {
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

  AddEntity(com: Communication, name: string) {
    const canvas = document.querySelector<HTMLCanvasElement>("canvas");
    if (canvas == null) {
      return;
    }

    canvas.addEventListener(
      "click",
      (event: MouseEvent) => {
        const sz = this.grid?.pix
        if (sz == undefined){
          return
        }
        const posx = Math.floor((event.offsetX) / sz);
        const posy = Math.floor((event.offsetY) / sz);
        com.AddEntity(name, posx, posy);
        console.log("aqui: ",posx, posy)
      },
      { once: true },
    );
  }

  Pause() {
    this.paused = true;
  }
  Continue() {
    this.paused = false;
  }

  Step(com: Communication) {
    com.Step();
  }
  Place(x: number, y: number, obj: any) {
    if (this.grid == null) {
      return;
    }
    this.grid.Fill(x, y);
  }
}
