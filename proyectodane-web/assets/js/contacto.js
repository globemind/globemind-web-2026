(function(){
  var f=document.getElementById('form-contacto');
  if(!f)return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var msg=document.getElementById('form-msg');
    if(f.website&&f.website.value)return; // honeypot
    if(!f.checkValidity()){f.reportValidity();return;}
    // TODO: conectar con el servicio de envío (pendiente de definir destino).
    msg.textContent='Gracias por escribirnos. (Envío aún no conectado: falta definir el destino del formulario).';
  });
})();
