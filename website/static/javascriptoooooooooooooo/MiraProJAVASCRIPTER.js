var imgLogo = document.querySelector("#imgLogo");
var div = document.querySelector("#divTabletosondo");
var a = 0;var c = 1;var id = null;var id2 = null;
id = setInterval(frame, 20);
function frame(){
    if(a==50+1){
        clearInterval(id);
        id2 = setInterval(all,20);
    }
    else{a++;
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
function divh(){x=0;
    const divn = document.createElement("div");const table = document.createElement("table");
    divn.className = "divnnn";table.className = "divnnn";div.append(divn);divn.append(table);
    var text = ["Seznam"];
    var href = ["https://www.seznam.cz/"];
    for(var j=0;j<text.length/2;j++){
        const tr = document.createElement("tr");
        table.append(tr);
        for(i=0;i < 2;i++) {
            const td = document.createElement("td");
            td.className = "testd";
            tr.append(td);
            var elA = document.createElement("a");
            elA.setAttribute('href', href[x]);
            elA.className = "text2255"
            elA.innerText = text[x];
            td.append(elA)
            x=x+1;
        };
    };
};