var socket = io.connect('http://192.168.15.126:5000');
var x = document.querySelector("#messages")
socket.on('connect', function(){
  socket.send('User se připojil!!!!!!');
});
socket.on('message', function(msg){
  x.innerHTML('<p>'+msg+'</p>');
  console.log("něco se děje");
});/*
x.on("click", function(){
  socket.send(x.val());
  x.val('');
});*/