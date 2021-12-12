function doGenerate() { window.location = "./"+returnHash(); };


function returnHash(){
    abc = "abcdefghijklmnopqrstuvwxyz1234567890".split("");
    var token=""; 
    for(i=0;i<30;i++){
         token += abc[Math.floor(Math.random()*abc.length)];
    }
    return token; //Will return a 30 bit "hash"
}
