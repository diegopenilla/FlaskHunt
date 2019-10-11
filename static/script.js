(function( $ ) {
    $.fn.initDropdown = function (option) {
  
        //ACD v - 1.0.0                                                   //
        //this is a simple plugin ,that writen by ANOD. hope you enjoy it!//
        //also u can support me : https://www.donationalerts.com/r/anod   //
        //default config                                                  //
        var config = $.extend({
            default_value:'Select a DNA sequence', // Свое значение.
            default_first: false, //Выбрать первый элемент в качестве значения по умолчанию
        },option);


        var dd = this.find('.dropdown');
        var items = this.find('li');
        var input = this.find('input');
        var items_list = this.find('.dropdown-itemsWrapper');
      
        dd.html(config.default_value);
        input.attr('value','null');
      //there a fix for preveous version of script
        items_list.removeClass('d-none').addClass('inactive');
      
        if(config.default_first){
            dd.html(config.default_first);
            input.attr('value','1');
        }

        $.each(this,function (i,v) {
            var selected = $(this).find('.selected');
            selected.parents('.dropdownWrapper').find('.dropdown').html(selected.html());
            selected.parents('.dropdownWrapper').find('input').attr('value',selected.attr('data-option'));
        });

        dd.on('click',function () {
            var container = $(this).parents('.dropdownWrapper');
            var items_list = container.find('.dropdown-itemsWrapper');

            items_list.toggleClass('inactive');
            $(this).toggleClass('active');

        });

        items.on('mousedown',function () {
            var container = $(this).parents('.dropdownWrapper');
            var input = container.find('input');
            var dropdown = container.find('.dropdown');
            var items_list = container.find('.dropdown-itemsWrapper');

            $(this).attr('class','selected');
            items_list.toggleClass('inactive');
            dropdown.toggleClass('active').html($(this).html());
            input.attr('value',$(this).attr('data-option'));
        });

        $(document).on('mousedown',function (e) { // событие клика по веб-документу

            var dropdowns = $('.dropdown.active');
            var items_list = dropdowns.parents('.dropdownWrapper').find('.dropdown-itemsWrapper');

            if(!dropdowns.is(e.target)) {
                dropdowns.removeClass('active');
                items_list.addClass('inactive');
            }
        });
    }
})(jQuery);

$('.dropdownWrapper').initDropdown();