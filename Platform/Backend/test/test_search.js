window.onload = function() {
    // 获取按钮和结果容器
    var btn = document.getElementById('btn');
    btn.onclick = function() {
        //console.log('正在清除 testData');
        localStorage.removeItem('testData');
        //console.log('testData 是否已清除？', !localStorage.getItem('testData'));


        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'test.txt', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) { 
            if (xhr.status >= 200 && xhr.status < 300) {
                    var jsonString = xhr.responseText;
                    //console.log(jsonString);
                    var data = JSON.parse(jsonString);
                    //console.log(typeof data);
                   localStorage.setItem('testData', JSON.stringify(data));
                   // console.log(JSON.stringify(data));
                    window.location.href = 'SearchResultPage.html';
                    
                } else {
                    console.error('Request failed with status:', xhr.status);
                }
            }
        };
        xhr.send();
    };

    
};