$( document ).ready(function() {
  $(".ClickToSlide").click(function(){
    $(this).find( ".slideTo" ).slideToggle();
  });

  // حساب الحسم بجلبه وحسابه هنا
  (function(){
    var product = $( ".card-product-perant" ).length;
    console.log(product);
    var i;
    for (i = 1; i <= product; i++) {
      var discount = $('.card-product-perant:nth-of-type(' + i + ')').find('.new-price').text();
      var price = $('.card-product-perant:nth-of-type(' + i + ')').find('.price').text();
      var new_price = parseInt(price)-(parseInt(discount)/100*parseInt(price));
      $('.card-product-perant:nth-of-type(' + i + ')').find('.new-price').text(new_price.toFixed(0) + '.00ر.س')
      
    }

    // حساب الصفحة الفردية المنتج الفردي

    (function(){
      var singel_discount = $('#card-product-perant').find('.new-price').text();
      var singel_price = $('#card-product-perant').find('.price').text();
      var singel_new_price = parseInt(singel_price)-(parseInt(singel_discount)/100*parseInt(singel_price));
      $('#card-product-perant').find('.new-price').text(singel_new_price.toFixed(0) + '.00ر.س')
      
      

    })();
    // نهاية الحساب 



    //$('.new-price').text(my_discount/100*4);

    
  
   })();
    
});