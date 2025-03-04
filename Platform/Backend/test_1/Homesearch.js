    window.onload = function() {
    var btn = document.getElementById('btn');
    
    btn.onclick = function() {
        // 获取用户输入的值
        var lng_L = document.getElementById('lng_L').value;
        var lng_R = document.getElementById('lng_R').value;
        var lat_L = document.getElementById('lat_L').value;
        var lat_R = document.getElementById('lat_R').value;

        // 创建 JSON 对象
        var data = {
            lng_L: lng_L,
            lng_R: lng_R,
            lat_L: lat_L,
            lat_R: lat_R
        };

        if (!lng_L || !lng_R || !lat_L || !lat_R) {
            alert("请填写所有经纬度信息"); // 当发现空字段时显示提示
            return; 
        }
        else{

        // 将 JSON 对象转换为字符串
        var jsonString = JSON.stringify(data);

        // 存储 JSON 字符串到 localStorage
        localStorage.setItem('userData', jsonString);
        //console.log(jsonString);
        window.location.href = 'DownloadPage.html';
         }
};
}