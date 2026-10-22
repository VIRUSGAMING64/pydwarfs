/**
 
class CommunicationStatus:
    STEP = 1
    CLOSE = 2
    CONTINUE = 3
    SIGKILL = 4
    SHOW = 5

 */
const SHOW = 5, ADD = 6, STEP = 1;
export default class Communication {
    ws;
    queue;
    idx;
    constructor(host) {
        this.ws = new WebSocket(host);
        this.ws.onclose = this.Closed;
        this.queue = new Array();
        this.idx = 0;
        this.ws.onmessage = (e) => {
            this.queue.push(e);
        };
    }
    Closed() {
        console.log("closed");
    }
    Show(data = {}) {
        data = JSON.stringify(data);
        return this.Send(String(SHOW) + "__DATA__" + String(data));
    }
    Step(data = {}) {
        data = JSON.stringify(data);
        return this.Send(String(STEP) + "__DATA__" + String(data));
    }
    AddEntity(name, x, y) {
        let data = {
            "name": name,
            "x": x,
            "y": y
        };
        let sdata = JSON.stringify(data);
        this.Send(String(ADD) + "__DATA__" + sdata);
    }
    Send(data) {
        if (this.ws.OPEN != this.ws.readyState) {
            return false;
        }
        this.ws.send(data);
        return true;
    }
    Recive() {
        if (this.ws.OPEN != this.ws.readyState) {
            return false;
        }
        if (this.queue.length <= this.idx) {
            return false;
        }
        let data = this.queue.at(this.queue.length - 1);
        this.queue = new Array();
        return data;
    }
}
