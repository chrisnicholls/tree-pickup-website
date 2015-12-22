function salt(x){
    var s = "";
    while(s.length<x&&x>0){
        var r = Math.random();
        s+= (r<0.1?Math.floor(r*100):String.fromCharCode(Math.floor(r*26) + (r>0.5?97:65)));
    }
    return s;
}

$(document).ready(function() {


    $("#loginForm").on("submit", function(event) {
        var s = salt(20);
        $("#inputS").val(s);

        var raw = $("#inputPassword").val();
        var salted = raw + s;
        /*alert("salted=" + salted);
        alert($.md5(salted));*/

        var hashed = $.md5(salted);

        $("#password").val(hashed);

    });
});