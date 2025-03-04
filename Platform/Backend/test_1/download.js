window.onload = function () {
    var link = document.getElementById('Link');
    //更新搜索框中的值
    var Data = JSON.parse(localStorage.getItem('userData'));
    document.getElementById('lng_L').value = Data.lng_L;
    document.getElementById('lng_R').value = Data.lng_R;
    document.getElementById('lat_L').value = Data.lat_L;
    document.getElementById('lat_R').value = Data.lat_R;
    //获取用户的输入值
    var lng_L = document.getElementById('lng_L').value;
    var lng_R = document.getElementById('lng_R').value;
    var lat_L = document.getElementById('lat_L').value;
    var lat_R = document.getElementById('lat_R').value;

    const bbox = {
        "min_longitude": parseFloat(lng_L),
        "min_latitude": parseFloat(lat_L),
        "max_longitude": parseFloat(lng_R),
        "max_latitude": parseFloat(lat_R)
    };


    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Open the request (POST method, target URL)
    xhr.open('POST', 'http://10.91.108.210:8080/zircon/locations/bbox', true);

    // Set the request header to tell the server that we're sending JSON data
    //xhr.setRequestHeader('Content-Type', 'application/json');

    // Define the onload function (what happens after the request is successful)
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Convert response to blob
            var blob = xhr.response;

            // Create a URL for the blob
            var url = window.URL.createObjectURL(blob);

            // Create an anchor element for downloading
            var a = document.createElement('a');
            a.href = url;
            a.download = 'data.csv'; // Name of the downloaded CSV file

            // Trigger download by clicking the anchor
            document.body.appendChild(a);
            a.click();

            // Clean up the URL object after download
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            console.error('Request failed with status: ' + xhr.status);
        }
    };

    // Define the onerror function (in case there's a network error)
    xhr.onerror = function () {
        console.error('Request failed');
    };

    // Set the response type to 'blob' to handle binary data
    xhr.responseType = 'blob';

    // Send the POST request with the JSON body containing the bbox data
    xhr.send(JSON.stringify({ bbox }));

};