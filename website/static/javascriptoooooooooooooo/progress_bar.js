var list = ["Matika","Fyzika","Informatika","Programování",]
for(let j=0;j<list.length;j++){
    var bar = document.querySelector('#'+list[j]+"bar");
    var a = document.querySelector('#'+list[j]);
    a = a.innerHTML;
    a = a.split('/');
    console.log(a);
    bar.style.width = a[0]/a[1]*100 +"%";
    if(a[0]==a[1]){
        bar.style.backgroundColor = 'lightGreen';
    };
};