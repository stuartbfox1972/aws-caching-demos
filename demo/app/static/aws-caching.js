
function triggerAWS() {
    
    const xhr = new XMLHttpRequest(),
        method = "GET",
        url="http://"+location.hostname+"/api/v1.0/elasticache/flush";

    xhr.open(method, url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            document.getElementById(responseID).innerHTML = xhr.responseText;
        }
    };
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}