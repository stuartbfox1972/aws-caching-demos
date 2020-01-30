var apiBase = "http://"+location.hostname+"/api/v1.0"

function flushCache() { 
    const xhr = new XMLHttpRequest(),
        url=apiBase + "/elasticache/flush";

    xhr.open("GET", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}

function runQuery() {
    const xhr = new XMLHttpRequest(),
        url=apiBase + "/elasticache/query";

    xhr.open("POST", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    qstr = document.getElementById("queryString").value
    xhr.send(JSON.stringify({"Query": qstr}));
}

function renderJSON(incoming) {
    document.getElementById("responseID").innerHTML = incoming;
}

function runCompare() {
    const xhr = new XMLHttpRequest(),
        url=apiBase + "/elasticache/compare";

    xhr.open("POST", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    qstr = document.getElementById("queryString").value
    xhr.send(JSON.stringify({"Query": qstr}));
}