
for(let i=1;i<=5;i++){
    var x = document.querySelector("#circle"+i);
    x.onclick = function(){
        for(let j=1;j<=5;j++){
            var z = document.querySelector("#circle"+j);
            z.style.border = "black solid 4px";
        };
        this.style.border = "green solid 4px";
    };
};
