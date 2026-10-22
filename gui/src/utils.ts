import Communication from "./com";



export function RawData(com :Communication){
    com.Show();
    let data = com.Recive();
    if (data.data == undefined) {
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
