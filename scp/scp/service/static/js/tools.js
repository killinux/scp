function doStyle(num) {
    var introArray = new Array("首页", "JMeter", "WebBench", "ApachBench");
    var s = document.getElementsByClassName("sb_menu")[0];
   
    for (var i = 0; i <= 3; i++) {
        if (i == num) {
            s.getElementsByTagName("a")[i].innerHTML = "<font size='2' color='#21a6ff'><< " + introArray[i] + "</font>";
             document.getElementById(i).style.display = "";
            
        } else {
            s.getElementsByTagName("a")[i].innerHTML = introArray[i];
             document.getElementById(i).style.display = "none";
        }
    }
}

