var imgLogo = document.querySelector("#imgLogo");
var div = document.querySelector("#divTabletosondo");
var a = 0;
var c = 1;
var id = null;
var id2 = null;
id = setInterval(frame, 20);
function frame(){
    if(a==50+1){
        clearInterval(id);
        id2 = setInterval(all,20);
    }
    else{
        a++;
        imgLogo.style.top = a + "px";
    };
};
function all(){
    if(c<=0){
        clearInterval(id2);
        imgLogo.remove();
        div.style.height = "900px";
        div.style.width = "900px";
        divh();
    }
    else{
        c=c-0.1;
        imgLogo.style.opacity = c;
    };
};
function divh(){
    const divn = document.createElement("div");const table = document.createElement("table");
    var text = ["Login", "Register","Login","Login"];
    divn.className = "divnnn";
    table.className = "divnnn";
    div.append(divn);
    divn.append(table);
    //ffdfdfdfd
    const tr1 = document.createElement("tr");const tr2 = document.createElement("tr");const tr3 = document.createElement("tr");
    table.append(tr1);table.append(tr2);table.append(tr3);
    //rdfffdf
    

    for(j=0;j<text.length/2;j++){
        const tr = document.createElement("tr");
        table.append(tr);
    };
    for(var i = 0; i < text.length; i += 1) {
        const td = document.createElement("td");
        if(i>=2 && i<=3 ){
            td.className = "testd";
            td.innerHTML = text[i];
            tr2.appendChild(td);
        }
        else if(i>=4){
            td.className = "testd";
            td.innerHTML = text[i];
            tr3.appendChild(td);
        }
        else{
            td.className = "testd";
            td.innerHTML = text[i];
            tr1.appendChild(td);
        }
    }
};