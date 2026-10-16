(function(){
  var v=document.getElementById('video-hero');
  if(!v)return;
  // Respeta a quienes pidieron menos movimiento: sin autoplay.
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    v.removeAttribute('autoplay');v.pause();
  }
})();
