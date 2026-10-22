export function RawData(com) {
    com.Show();
    let data = com.Recive();
    if (data.data == undefined) {
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
