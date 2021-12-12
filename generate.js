function doGenerate() { window.location = "./"+returnHash(); };


function returnHash(){
    abc = "abcdefghijklmnopqrstuvwxyz1234567890".split("");
    var token=""; 
    for(i=0;i<32;i++){
         token += abc[Math.floor(Math.random()*abc.length)];
    }
    return token; //Will return a 32 bit "hash"
}
