function doStyle(num) {
    var introArray = new Array("首页", "测试标准", "测试流程", "测试介绍");
    var s = document.getElementsByClassName("sb_menu")[0];
    if (num == 0) {
        document.getElementById("childindex").style.display = "";
        document.getElementById("content").style.display = "none";
    } else {
        document.getElementById("childindex").style.display = "none";
        document.getElementById("content").style.display = "";
    }
    for (var i = 0; i <= 4; i++) {
        if (i == num) {
            s.getElementsByTagName("a")[i].innerHTML = "<font size='2' color='#21a6ff'><< " + introArray[i] + "</font>";
        } else {
            s.getElementsByTagName("a")[i].innerHTML = introArray[i];
        }
    }
}

function readFile(fileName) {
    $.post("test_File_doFile", {
        fileName : fileName
    }, function(data, textStatus) {this;
        document.getElementById("content").innerHTML = data;
    });
}

function choose(num) {

    switch(num) {
        case 0:

            doStyle(0);

            break;
        case 1:

      
            readFile("test.txt");
            doStyle(1);
            break;
        case 2:
            ;

          

         
           readFile("test1.txt");
            doStyle(2);
            break;
        case 3:

           

           readFile("test2");
          
            doStyle(3);
            break;
    }

}
