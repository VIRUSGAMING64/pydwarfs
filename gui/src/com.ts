/**
 
class CommunicationStatus:
    STEP = 1
    CLOSE = 2
    CONTINUE = 3
    SIGKILL = 4
    SHOW = 5

 */

const SHOW = 5,
    ADD = 6,
    LOAD_LOGS=7,
    LOAD_MAP=15,
    STEP = 1,
    FRAME = 8;
export default class Communication {
    ws: WebSocket;
    latest: string | null;
    pending: boolean;
    logCursor: number;

    constructor(host: string) {
        this.ws = new WebSocket(host);
        this.ws.onclose = this.Closed;
        this.latest = null;
        this.pending = false;
        this.logCursor = 0;
        this.ws.onmessage = (e) => {
            this.latest = e.data;
            try {
                const frame = JSON.parse(e.data);
                if (typeof frame.logCursor === "number") {
                    this.logCursor = frame.logCursor;
                }
            } catch (_) {
                // Non-frame responses use the legacy protocol.
            }
            this.pending = false;
        };
    }

    Closed() {
        console.log("closed");
    }
    
    GetLogs(data = {}) {
        data = JSON.stringify(data)
        return this.Send(String(LOAD_LOGS) + "__DATA__" + String(data));
    }
    
    LoadMap(data = {}){
        data = JSON.stringify(data)
        return this.Send(String(LOAD_MAP) + "__DATA__" + String(data));
    }
    Step(data = {}) {
        data = JSON.stringify(data)
        return this.Send(String(STEP) + "__DATA__" + String(data));
    }

    Frame(advance = false) {
        if (this.pending) {
            return false;
        }
        this.pending = true;
        return this.Send(String(FRAME) + "__DATA__" + JSON.stringify({ advance, logCursor: this.logCursor }));
    }
    AddEntity(name: string , x :number, y : number) {
        let data = {
            "name": name,
            "x" : x,
            "y": y
        }
        let sdata = JSON.stringify(data)
        this.Send(String(ADD) + "__DATA__" + sdata)
    }
    
    Send(data: string) {
        if (this.ws.OPEN != this.ws.readyState) {
            this.pending = false;
            return false;
        }
        this.ws.send(data);
        return true;
    }

    Recive() {
        if (this.ws.OPEN != this.ws.readyState) {
            return false;
        }
        if (this.latest == null) {
            return false;
        }
        const data = { data: this.latest };
        this.latest = null;
        return data;
    }
}
