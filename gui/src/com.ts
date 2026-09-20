export default class Communication{
    ws: WebSocket;
    queue: any[];
    idx: number;
    
    constructor(host: string){
        this.ws = new WebSocket(host)
        this.ws.onclose = this.Closed
        this.queue = new Array()
        this.idx = 0
        this.ws.onmessage = (e)=>{
            this.queue.push(e)
        }
    }
    
    Closed(){
        console.log("closed")
    }

    Send(data: string){
        if (this.ws.OPEN != this.ws.readyState){
            return false
        }
        this.ws.send(data)
        return true
    }

    Recive(){
        if (this.ws.OPEN != this.ws.readyState){
            return false
        }
        if(this.queue.length <= this.idx){
            return false
        }
        let data = this.queue.at(this.idx)
        this.idx += 1
        if (this.idx == 30){
            this.queue = this.queue.slice(this.idx)
            this.idx = 0
            console.log("limpiado",this.queue.length)
        }
        return data
    }

}