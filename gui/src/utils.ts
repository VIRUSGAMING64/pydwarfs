import Communication from "./com";



export function RawData(com :Communication, advance = false){
    let data = com.Recive();
    com.Frame(advance);
    if (data === false || data.data == undefined) {
        return "";
    }
    return data.data
}

export function GetCreatures(rawstr: string){
    let obj = JSON.parse(rawstr)
    return obj.creatures
}

export function GetRunningCreatures(rawstr: string){
    let obj = JSON.parse(rawstr)
    return obj.runningCreatures
}

export function GetMaps(rawstr: string){
    let obj = JSON.parse(rawstr);
    return obj.maps
}

export function GetLogs(rawstr: string){
    let obj = JSON.parse(rawstr);
    if (!Array.isArray(obj.logs)){
        return false
    }
    return obj.logs
}
