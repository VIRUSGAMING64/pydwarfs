export function RawData(com, advance = false) {
    let data = com.Recive();
    com.Frame(advance);
    if (data === false || data.data == undefined) {
        return "";
    }
    return data.data;
}
export function GetCreatures(rawstr) {
    let obj = JSON.parse(rawstr);
    return obj.creatures;
}
export function GetRunningCreatures(rawstr) {
    let obj = JSON.parse(rawstr);
    return obj.runningCreatures;
}
export function GetMaps(rawstr) {
    let obj = JSON.parse(rawstr);
    return obj.maps;
}
export function GetLogs(rawstr) {
    let obj = JSON.parse(rawstr);
    if (!Array.isArray(obj.logs)) {
        return false;
    }
    return obj.logs;
}
