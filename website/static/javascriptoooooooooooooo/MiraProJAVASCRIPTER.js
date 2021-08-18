var imgLogo = document.querySelector("#imgLogo");
var vcela = document.querySelector(".vcela");
var a = 0;
var id = null;
id = setInterval(frame, 10);
function frame(){
    if(a==50){
        clearInterval(id);
    }
    else{
        a++;
        imgLogo.style.top = a + "px";
    }
};