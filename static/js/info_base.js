/**
 * Created by gaoyunchu on 18/12/25.
 */
// 获取用户前端输入的函数，便于发送GET请求
function split2list(text) {   //将字符串中的,分隔开，得到list
    //缺少类型的转换 eventcode
    list = text.split(',');
    return list;
}
function date_split(date) {
    //将DATE转换为8位字符串形式
    date_list = date.split('-');
    res = "";
    if (date_list.length == 3)
        res = date_list[0] + date_list[1] + date_list[2];
    return res;
}
function list2int(list) {
    //将EVENT中的字符串转换为INT
    res = [];
    l = list.length;
    for (var i = 0; i < l; i++) {
        res.push(parseInt(list[i]));
    }
    return res;
}