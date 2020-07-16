var apiBase = location.protocol+"//"+location.hostname+"/api/v1.0";


function FlushCache() {
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

function runRDSQuery() {
    const xhr = new XMLHttpRequest(),
        url=apiBase + "/rds/query";

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

function runRDSCompare() {
    const xhr = new XMLHttpRequest(),
        url=apiBase + "/rds/compare";

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

function copyClip(q) {
    /* Get the text field */
    var copyText = document.getElementById(q);
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
    document.getElementById("queryString").innerHTML = copyText.value;
  
}

function runS3Prepare() {
    const xhr = new XMLHttpRequest(),
    url=apiBase + "/s3/prepare";

    xhr.open("GET", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}

function runS3Clean() {
    const xhr = new XMLHttpRequest(),
    url=apiBase + "/s3/clean";

    xhr.open("GET", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}

function runS3Query() {
    const xhr = new XMLHttpRequest(),
    url=apiBase + "/s3/query";

    xhr.open("GET", url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            renderJSON(xhr.responseText)
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}