var apiBase = "http://"+location.hostname+"/api/v1.0"

function flushCache() { 
    const xhr = new XMLHttpRequest(),
        method = "GET",
        url=apiBase + "/elasticache/flush";

    xhr.open(method, url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            document.getElementById("responseID").innerHTML = xhr.responseText;
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}

function runQuery() {
    const xhr = new XMLHttpRequest(),
        method = "POST",
        url=apiBase + "/elasticache/query";

    xhr.open(method, url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            document.getElementById("responseID").innerHTML = JSON.stringify(xhr.responseText, undefined, 2);
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    qstr = document.getElementById("queryString").value
    xhr.send(JSON.stringify({"Query": qstr}));
}