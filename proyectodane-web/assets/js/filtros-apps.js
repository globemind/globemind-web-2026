(function(){
  var chips=document.querySelectorAll('.chip[data-cat]'),cards=document.querySelectorAll('.app');
  var count=document.getElementById('apps-count');
  chips.forEach(function(chip){
    chip.addEventListener('click',function(){
      var cat=chip.dataset.cat,n=0;
      chips.forEach(function(c){c.setAttribute('aria-pressed',c===chip);});
      cards.forEach(function(card){
        var show=!cat||card.dataset.categorias.split('|').indexOf(cat)>-1;
        card.hidden=!show;if(show)n++;
      });
      if(count)count.textContent=n+(n===1?' aplicación':' aplicaciones');
    });
  });
})();
