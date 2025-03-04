// 在当前页面发送请求并处理响应
window.onload = function() {
    var btn = document.getElementById('btn');
    btn.onclick = function() {
        const xhr = new XMLHttpRequest();

        var lng_L = document.getElementById('lng_L').value;
        var lng_R = document.getElementById('lng_R').value;
        var lat_L = document.getElementById('lat_L').value;
        var lat_R = document.getElementById('lat_R').value;

        var params = 'lng_L=' + lng_L + '&lng_R=' + lng_R + '&lat_L=' + lat_L + '&lat_R=' + lat_R;

        xhr.open('GET', 'url?' + params, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
            
                var responseData = JSON.parse(xhr.responseText);
                localStorage.setItem('responseData', JSON.stringify(responseData));

                window.location.href = 'SearchResultPage.html';
            }
        };
        xhr.send();
        
    };
};
