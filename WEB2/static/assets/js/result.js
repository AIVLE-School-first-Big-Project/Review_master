$(document).ready(function(){
    $('.review_tr').each(function(){
        var content = $(this).children('.content');
        var content_txt = content.text();
        var content_txt_short = content_txt.substring(0,150)+"...";
        var btn_more = $('</tr><td colspan="2" style="text-align: right; font-size: 1.1rem;;"><a href="javascript:void(0)" class="more">더보기</a></td></rs>');

        
        $('.review_bth').append(btn_more);
        
        if(content_txt.length >= 150){
            content.html(content_txt_short)
            
        }else{
            btn_more.hide()
        }
        
        btn_more.click(toggle_content);
        // 아래 bind가 안 되는 이유는??
        // btn_more.bind('click',toggle_content);

        function toggle_content(){
            if($(this).hasClass('short')){
                // 접기 상태
                $(this).html('더보기');
                content.html(content_txt_short)
                $(this).removeClass('short');
            }else{
                // 더보기 상태
                $(this).html('접기');
                content.html(content_txt);
                $(this).addClass('short');

            }
        }
    });
});