var text = ["Login","Register","SPS website"];
var href = ["login","register","https://sps-prerov.cz/"];
// Nahoře doplń tabulku
console.log("Please login/register!");
var divMain = document.querySelector("#divTabletosondo");
var imgLogo = document.createElement("img");
var a = 0;var c = 1;var id = null;var id2 = null;id3 = null;id4 = null;var k=0;var x=0;var g=0
imageprosim();
function imageprosim(){
    divMain.style.height = "599px";
    divMain.style.width = "369px";
    imgLogo.setAttribute('src','/static/images/MYLOGO.png');
    imgLogo.setAttribute('id', "imgLogo");
    divMain.append(imgLogo);
    stopId1 = setInterval(startId1, 20);
};
function startId1(){
    if(!(g==50+1)){
        g++;
        imgLogo.style.top = g + "px";}
    else{
        clearInterval(stopId1);
        stopId2 = setInterval(startId2,500);
        function startId2(){
            clearInterval(stopId2);
            stopId3 = setInterval(startId3,10);
        }
        function startId3(){
            if(!(c<=0)){
                c=c-0.01;
                imgLogo.style.opacity = c;
            }
            else{
                clearInterval(stopId3);
                imgLogo.remove();
                divMain.style.height = "700px";
                divMain.style.width = "900px";
                divh();
            };
        };
    };
};
function divh(){
    const element_div = document.createElement("div");
    const element_table = document.createElement("table");
    element_div.className = "element_class";
    element_table.className = "element_class";
    divMain.append(element_div);
    element_div.append(element_table);
    const div_table = document.querySelector(".element_class");
    div_table.style.opacity = 0;
    for(var j=0;j<text.length;j++){// vydělto length 2
        const element_tr = document.createElement("tr");
        element_table .append(element_tr);
        for(i=0;i<1;i++){// přidej i<1 na 2
            const element_td = document.createElement("td");
            element_td.className = "class_td";
            const element_p = document.createElement("p");
            element_p.className = "class_p";
            element_p.innerText = text[x];
            element_td.append(element_p);
            const element_a = document.createElement("a");
            element_a.setAttribute('href', href[x]);
            element_tr.append(element_a);
            element_a.append(element_td);
            x=x+1;
        };
    };
    stopId4 = setInterval(startId4,2);
    function startId4(){
        if(!(k>1)){
            k=k+0.01;
            div_table.style.opacity = k;
        }
        else{
            clearInterval(stopId4);

        };
    };
};