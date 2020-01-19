const ClearCache = async () => {
    var h = location.hostname;
    const response = await fetch('http://' + location.host + '/api/v1.0/elasticache/flush');
    const myJson = await response.json(); //extract JSON from the http response
    // do something with myJson
  }