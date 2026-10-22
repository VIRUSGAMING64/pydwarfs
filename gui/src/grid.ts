export default class Drawler{
    pix: number
    ctx: CanvasRenderingContext2D|null
    sizex: number
    sizey: number
    
    constructor(ctx: CanvasRenderingContext2D|null, pixels: number, sizex: number,sizey: number){
        this.pix = pixels
        this.ctx = ctx
        
        this.sizex = sizex
        this.sizey = sizey
    }
    
    FillMatrix(){
        let color = "#00ff00"
        for(let i = 0; i < this.sizex; i++){
            for(let j = 0; j < this.sizey; j++){
                this.Fill(i,j, color)
            }   
        }
    }

    Fill(px :number,py :number, color = "black", border = "red"){
        if (this.ctx == null){
            return
        }
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