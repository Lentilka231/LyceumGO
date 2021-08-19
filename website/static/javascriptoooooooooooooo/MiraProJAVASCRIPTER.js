var element = document.querySelector("#ToKnow");
if(typeof(element) != 'undefined' && element != null){
    const imgLogo = document.querySelector("#imgLogo");
    imgLogo.remove
    console.log("Logged!");
} else{
    var div = document.querySelector("#divTabletosondo");
    var imgge = document.createElement("img")
    imgge.setAttribute('src','/static/images/MYLOGO.png');
    imgge.setAttribute('id', "imgLogo");
    div.append(imgge);
    console.log("Please login/register!");
    var a = 0;var c = 1;var id = null;var id2 = null;id3 = null;
    id = setInterval(frame, 20);
    function frame(){
        const imgLogo = document.querySelector("#imgLogo");
        if(!(a==50+1)){a++;
            imgLogo.style.top = a + "px";}
        else{
            clearInterval(id);
            id3 = setInterval(xddd,500)
            function xddd(){
                clearInterval(id3)
                id2 = setInterval(all,10);
            }
            function all(){
                if(!(c<=0)){
                    c=c-0.01;
                    imgLogo.style.opacity = c;
                }
                else{//endId2
                    clearInterval(id2);
                    imgLogo.remove();
                    div.style.height = "700px";
                    div.style.width = "900px";
                    divh();           
                };
            };
        };
    };
    function divh(){x=0;
        const divn = document.createElement("div");const table = document.createElement("table");
        divn.className = "divnnn";table.className = "divnnn";div.append(divn);divn.append(table);
        const divnnn = document.querySelector(".divnnn");
        divnnn.style.opacity = 0;
        divnnn.setAttribute("id", "divjaksvin");
        var text = ["Login","Register","About us"];
        var href = ["login","register","aboutus"];
        for(var j=0;j<text.length;j++){// vydělto length 2
            const tr = document.createElement("tr");
            table.append(tr);
            for(i=0;i<1;i++){// přidej i<1 na 2
                const td = document.createElement("td");
                const p = document.createElement("p");
                const elA = document.createElement("a");
                td.className = "testd";
                p.innerText = text[x];
                elA.setAttribute('href', href[x]);
                tr.append(elA);
                elA.append(td);
                td.append(p);
                p.className = "text2255";
                x=x+1;
            };
        };
        id4 = null;
        id4 = setInterval(aldsal,2)
    };
    var k=0;
    function aldsal(){
        const divnnn = document.querySelector(".divnnn");
        if(!(k>1)){
            k=k+0.01;
            divnnn.style.opacity = k;
        }
        else{
            clearInterval(id4);
        };
    };
};