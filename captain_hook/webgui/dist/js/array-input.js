
$(document).ready(function () {
   $('.array-input').each(function () {
       var input_container = $(this);

       $(input_container).on('click', '.delete', function () {
           console.log('click');
           $(this).parent().parent().parent().remove();
       });

       $(input_container).find('.add').click(function () {
           var input = $(this).parent().parent().find('input');
           var field = input.data('field');
           var prefix = input.data('prefix');
           var value = input.val();
           if(!value){
               return;
           }
           var html = '<li> <div class="input-group"> <input name="['+ prefix +'['+ field +'][]" value="'+ value +'" class="form-control"/> <div class="input-group-addon delete"> <i class="fa fa-times"></i> </div></div></li>'
           $(input_container).find('.addItem').before(html);
           input.val('');
       });
   })
});