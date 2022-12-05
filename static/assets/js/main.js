setTimeout(function(){
    $('.message').fadeOut('slow');
},4000);

$(document).ready(function(){
    $('.spinner_on_off').hide();
    setTimeout(function(){
        var class_name = $('.icon-badge-container');
        class_name.children('.icon-badge-icon').attr('style','color:dimgray;');    
    $(class_name).click(function(e){
        e.preventDefault();
        var atr = class_name.attr('aria-expanded');
        
        if (atr.includes('false')){
            class_name.children('.icon-badge-icon').attr('style','color:white;');
        }
        else{
            class_name.children('.icon-badge-icon').attr('style','color:dimgray;');
        }
    })
},3000);
});


function hover_func(val, reply){
    if (reply == 'r'){
        var val = reply + val;
    }
    var this_ = $('.comment-hover-func-' + val);
    $.ajax({
        type:'GET',
        url: this_.attr('data-href'),
        data: {},
        success: function(user){
            this_.removeAttr('onmouseover');
            var svg_img = $('.svg_img_path').attr('path');
            var c_hov = "";
            c_hov += "<div class='card bg-dark' style='width: 18rem;'><div class='col-md-10 ml-md-3'>";
            if (user.profile_photo){
                c_hov += "<img  src='/media/"  + user.profile_photo + "' class='img-fluid card-img-top rounded-circle' width='30px' width='30px' alt='photo'>";
            }
            else{
                c_hov += "<img src='" + svg_img + "' class='img-fluid card-img-top rounded-circle' width='30px' width='30px' alt='photo'>";
            }
                c_hov += "</div><div class='card-body'><a href='/account/" + user.hover_username + "/dashboard/' class='card-title text-capitalize text-white'>";
            if (user.First_name){
                c_hov += user.First_name + " " +  user.Last_name;
            }
            else{
                c_hov += "";
            }
            c_hov += "</a><p class='card-text d-block'>";
            if (user.interests){
                c_hov += user.interests;
            }
            c_hov += "</p><p class='card-text'>followed by " + user.follower_count + " people</p><ul class='list-inline'><li class='list-inline-item'><a class='text-white' href='";
            if (user.youtube_url){
                c_hov += user.youtube_url;
            } 
            c_hov += "'><i class='fa fa-youtube-play'></i></a></li><li class='list-inline-item'><a class='text-white' href='";
            if (user.facebook_url){
                c_hov += user.facebook_url;
            }
            c_hov += "'><i class='fa fa-facebook-official'></i></a></li><li class='list-inline-item'><a class='text-white' href='";
            if (user.github_url) {
                c_hov += user.github_url;
            }
            c_hov += "'><i class='fa fa-github'></i></a></li><li class='list-inline-item'><a class='text-white' href='";
            if (user.youtube_url) {
                c_hov += user.youtube_url;
            }
            c_hov += "'><i class='fa fa-instagram'></i></a></li><li class='list-inline-item'><a class='text-white' href='";
            if (user.linkedin_url) {
                c_hov += user.linkedin_url;
            }
            c_hov += "'><i class='fa fa-linkedin'></i></a></li></ul></div></div>";
            this_.attr('data-original-title', c_hov)
            }
        })
            $("[data-toggle='tooltip_" + val + "']").tooltip('toggle');
            
        return false;
        };


function notification_engine(event,val){
        event.preventDefault();
        var this_ = $('.' + val);
           $.ajax({
               type : 'GET',
               url :  this_.attr('data-href'),
               data : {},
               success: function(data){
                   this_.removeAttr('onclick');
                   var nt = $('.remove-badge-click');
                   nt.remove();
                   var lst_grp = $('.list-group-change')
                   var count = lst_grp.attr('count');
                   var nav_count = lst_grp.attr('nav-count');
                   for(clr=1; nav_count >= clr; clr++){
                    var clr_chng = $('.list-group-clr-' + clr.toString());
                    clr_chng.attr('class','list-group-item list-group-item-action list-group-item-dark');
                   }                
                   if (count <= 8 && count >= 1) {
                       count = count * 55;
                       lst_grp.attr('style',('height:' + count + 'px; overflow:auto;'));
                   }
                  
               }
           });
           return false;
};

function editable_comment(val, comm_id, extra){
    var this_ = $(val + comm_id);
    var z = this_.html();
    if (extra == ''){
        this_.remove();
        $('.dropbutton' + comm_id).hide();
        $('#commbox' + comm_id).append("<textarea class='form-control' id='commtext" + comm_id + "' name='message' rows='5' cols='50' placeholder='reply' required>" + z + "</textarea>");
        $('#editabletext' + comm_id + 'button').attr('class','btn btn-sm btn-light').html('save');
        $('#canceltext' + comm_id + 'button').attr('class','btn btn-sm btn-success').html('cancel');
    }
    else if (extra == 'cancel'){
        this_.remove();
        $('.dropbutton' + comm_id).show();
        $('#commbox' + comm_id).append("<small class='p-0 m-0' id='commtext" + comm_id + "'>" + z + "</small>");
        $('#editabletext' + comm_id + 'button').removeAttr('class').html('');
        $('#canceltext' + comm_id + 'button').removeAttr('class').html('');
    }
    else if (extra == 'sbmit'){
            $('#editabletext' + comm_id + 'button').attr('class','btn btn-sm btn-light disabled').html("save <span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
            event.preventDefault();
            var this_ = $('#commbox' + comm_id);
            var serializedData = $(this_).serialize();
            $.ajax({
                type : 'POST',
                url : this_.attr('data-href'),
                data : serializedData,
                success : function(data){
                    var this_ = $('#commtext' + comm_id);
                    this_.remove();
                    $('.dropbutton' + comm_id).show();
                    $('#commbox' + comm_id).append("<small class='p-0 m-0' id='commtext" + comm_id + "'>" + data['text'] + "</small>");
                    $('#editabletext' + comm_id + 'button').removeAttr('class').html('');
                    $('#canceltext' + comm_id + 'button').removeAttr('class').html('');

                },
                error : function(data){
                    location.reload();
                }
            })
        }
    else if (extra == 'dlt'){
        event.preventDefault();
        var this_ = $(val + 'href');
        $.ajax({
            type : 'GET',
            url : this_.attr('data-href'),
            data : {},
            success : function(data){
                // console.log(data['text']);
                $('#replycommentDelete1' + comm_id).modal('hide');
                $('#maincommentDelete20' + comm_id).modal('hide');
                var com_cnt = parseInt($('.comments-count').html()) - 1;
                $('.comments-count').html(com_cnt.toString());
                $(val).html("<div class='media-body border border-danger'><p>" + data['text'] + "</p></div><div class='mb-2 pb-2'></div>");

            },
            error : function(data){
                location.reload();
            }
        })
    }
    return false;
    };

// Logout the user.
function IdleTimeout() {
    var this_ = $('#logout_page');
    if(this_[0]){
        $.ajax({
            type : 'POST',
            url :  this_.attr('data-href'),
            data : this_.serialize(),
            success: function(data){
                location.reload();
        }
    })
}
};

$(document).ready(function(){
    
    $('.show-ntf').click(function(e){
        e.preventDefault();
        var this_ = $(this);
        // console.log('here');
        $.ajax({
            type:'GET',
            url: this_.attr('data-href'),
            data:{},
            success:function(context){
                var ntf = "";
                    ntf += "<div class='icon-badge-container icon-badge-click mt-2' onclick=notification_engine(event,'icon-badge-click');return  data-href='/" + context.nav_username + "/notifications/' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'><i class='far fa-bell icon-badge-icon' style='color:dimgray;'></i>";
                    if (context.unread_notification > 0){
                        ntf += "<div class='icon-badge'><a class='icon-badge remove-badge-click' style='background-color: #ff0000;'>" + context.unread_notification + "</a></div>";
                    
                    }
                    ntf += "</div><div class='dropdown-menu dropdown-menu-left dropdown-menu-lg-right mb-0 pb-0'><div class='list-group list-group-change' nav-count='" + context.unread_notification + "' count='" + context.total_notification_count + "' style = '";
                    if (context.total_notification_count > 9){
                        ntf += "height:500px;";
                    }
                    else{
                        ntf += "height:50px;";
                    } 
                    ntf += "overflow:auto;'><ul class='list-group list-group-flush' style='width:400px;'>";
                    if (context.total_notification_count > 0){
                        for(var x=0; x < context.total_notification_count; x++){
                            var y = x + 1;
                            ntf += "<a type='button' href='" + context.notification[x].text_url + "' target='_blank' class='list-group-item list-group-item-action list-group-clr-" + y.toString() + "'><small class='d-inline-block'>" + context.notification[x].text + " </small></a>";
                        
                        } 
                    }                       
                    else{
                        ntf += "<a type='button' class='list-group-item list-group-item-action'><small class='text-muted d-inline-block'> ******** notification is empty ********</small></a>";
                    }
                    ntf += "</ul></div><p class='list-group-item text-center list-group-item-dark mb-0'><a href='/activity/' class='d-inline-block'> See all </a></p></div>";
                    $('.ntf_dropdown').append(ntf);
                    $('.nav-bar-img').attr('src', context.profile_photo);
                    $('.show-ntf').attr('class',' ').attr('data-href',' ');
                }
            }
        )
    })
});

$(document).ready(function(){
    $(".show-ntf").click();
    $(".get_comment").click();
    setTimeout(function(){
        var url_link = (window.location.href).split('#')[1];
        // console.log('link get');
    var x = 0;
    if (url_link){
        var select_course = url_link.includes('button');
        var select_comment = url_link.includes('comment_1008');
        if (!select_comment){
            select_comment = url_link.includes('comment_5008');
        }
        if (select_course){
            document.getElementById(url_link + '-tab').click();

        }
        else if(select_comment){
            // console.log(url_link);
                var cmnt = $('#' + url_link);
                // cmnt.click();
                // console.log(cmnt);
                cmnt.attr('style','background-color:lemonchiffon;');
                // $(window).scrollTop($('#' + url_link).offset().top - 200); // doesn't give you smooth scroll
                
                $('html, body').animate({ 
                    scrollTop: $('#' + url_link).offset().top - 200
                }, 500);
                setTimeout(function(){
                    // console.log('style comment');
                    cmnt.attr('style','');
                },3000);
                // window.addEventListener('scroll',()=>{
                // if (x == 0){
                //     const scrolled = window.scrollY;
                //     cmnt.attr('style','background-color:lemonchiffon;');
                //     var z = scrolled - 200;
                //     console.log(z);
                //     window.onload = scrolldown(val=z,cmnt=cmnt);
                //     x = 500;
                // }});
                // function scrolldown(val,cmnt){
                //     window.scroll({
                //       top: val,
                //       behavior: 'smooth'
                //     });
                //     setTimeout(function(){
                //         console.log('style comment');
                //         cmnt.attr('style','');
                //     },3000);
                
                // }

            }
    }

    }, 3200)
});

function reply_Public_comment(event,val,extra){
        event.preventDefault();
        var this_ = $("#Public_comment_" + val.toString());
        var this_btn = $('#Public_comment_submit_btn' + val.toString() + extra);
        // $('#accordian').fadeIn(300,function(){
        //     this_btn.attr('class','btn btn-sm bg-light shadow disabled').html("wait.. <span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
        // }).fadeOut(200);
        this_btn.attr('class','btn btn-sm bg-light shadow disabled').html("wait.. <span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
        
        if (extra == 'reply'){
            this_ = $("#Public_comment_r" + val.toString());
        }
        var serializedData = $(this_).serialize();
        if (serializedData.endsWith('message=')){
            var message = $("#" + extra + "_message_" + val).val();
            serializedData = serializedData + message;
        }
        $.ajax({
            type : 'POST',
            url :  this_.attr('data-href'),
            data : serializedData,
            success: function(data){
                    // $('#accordian').fadeOut(100,function(){
                    //         $('.get_comment').html("");
                    //     }).load(location.href + ' #accordian').fadeIn(10, function(){
                    //         $('.get_comment').click();
                    //     });
                        $('.get_comment').click();
                // location.reload();
                // $('#accordian').fadeOut('slow').load(location.href + ' #accordian').fadeIn('slow');

            },
            error : function(data){
                location.href=data['responseJSON']['path'];
            }
       },)
       return false;
};

function refresh(data){
    var prevstate = "";
    var img_path = $('.svg_img_path').attr('path');
    $('.all-followers').html('');
    for (people=0;people<data.count;people++){
        prevstate = "";
        var uname=data['useracc'][people]['user_email'].replace('@gmail.com','');
        if (data['useracc'][people]['First_name']){
            var first_name = data['useracc'][people]['First_name'];
            var last_name = data['useracc'][people]['Last_name'];
        };
        var cnt = data['follower_count_' + people.toString()];
        var uid = data['useracc'][people]['id']
        prevstate = prevstate + "<div class='card mb-0 mt-0 pt-0 pb-0 border-0' style='max-width: 500px;'><div class='row no-gutters mb-0 mt-0 pt-0 pb-0'><div class='col-sm-1 py-3'>"
         var pto = 'follower_profile_' + people.toString();
         if (data['useracc'][people]['profile_photo']){
             prevstate = prevstate + "<img src='" + data[pto] + "' class='img-fluid rounded-circle' height='50' width='50' alt='photo'></div>"
         }
         else{
             prevstate = prevstate + "<img src='" + img_path + "' class='img-fluid rounded-circle' height='50' width='50' alt='photo';></div>"
         }
         prevstate = prevstate + "<div class='col-sm-8'><div class='card-body'><h5><a class='card-title' href='/account/" + uname + "/dashboard/'" + ">"; 
         if(first_name){
             prevstate += String(first_name + ' ' + last_name);
            }
        else{
            prevstate += uname;
        }
         prevstate = prevstate + "</a></h5><p class='card-text m-0 p-0'>";
             if (data['useracc'][people]['interests']){
                 prevstate = prevstate + data['useracc'][people]['interests']
             }
         prevstate = prevstate + "</p><small class='text-muted'>followed by </small><small data-value='pop-followers-number" + data['useracc'][people]['id'] + "' class='text-muted pop-followers-number" + uname + "'>"
         prevstate = prevstate + cnt;
         prevstate = prevstate + "</small><small class='text-muted'> people</small></div></div><div class='col-sm-2'><div class='card-body'>";
             if (data['username'] != uname){

                 prevstate = prevstate + "<button type='button' onclick='follow_and_comment_like(event," + uid + ")' data-href=" + "/account/" + uname + "/follow/" + " class='btn btn-sm btn-outline-dark' id=" + "followbtn2" + uid + ">";
                     // console.log(data['follower_inside_' + people.toString()])
                     if (data['follower_inside_' + people.toString()]=="unfollow"){
                         prevstate = prevstate + "unfollow";
                         // console.log(data['follower_inside_' + people.toString()])
                     }
                     else{
                         prevstate = prevstate + "follow";
                     }
             };
             prevstate = prevstate + "</button></div></div></div></div>";
        
        $('.all-followers').append(prevstate);
    };
    $('.spiner_on_off').hide();

};
function follow_and_comment_like(event,val){
    var this_ = $('#followbtn2' + val);
    if (this_.length == 0) {
        this_ = $('#comment_likes_' + val);
    }
    event.preventDefault();
    var this_ = $(this_);
    this_.html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");

    $.ajax({
        type : 'GET',
        url :  this_.attr('data-href'),
        data : {},
        success: function(data){
            if (this_.hasClass('comment_like')){
                this_.text(data.condition);
                this_count = $('.comment_like_count_' + val);
                if (data.count > 0) {
                    this_count.text('' + data.count);
                }
                else{
                    this_count.text('');
                }
            }
            else{
                this_.text(data.condition);
                this_part_pop = $('.pop-followers-number' + data.slug);
                this_part_pop.text(" " + data.count);
            }
       },
       error: function(data){
           location.href=data['responseJSON']['path']
       }
   })
    return false;
   };
function get_comment_func(event){
   $(document).ready(function(){
    var this_ = $('.get_comment');
    // console.log('before');
        // console.log('heree');
        event.preventDefault();
        // this_.html("fetching...<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
        // console.log('ajax comming');
        $.ajax({
        type : 'GET',
        url :  this_.attr('data-href'),
        data : {},
        success: function(data){
            // console.log('inside');
            var com_cnt_var = 1;
            var comm_state = "";
            var token = $('#token').attr('csrf-value');
            var svg_img = $('.svg_img_path').attr('path');
            var req_username = data.req_username;
            var post_id = data.post_id;
            var post_slug_name = data.post_slug_name;
            var post_author_username = data.post_author_username;
            var comm_r = 1;
            this_.html("");
            if (com_cnt_var > 1){
                var com_cnt = parseInt($('.comments-count').html()) + 1;

                $('.comments-count').html(com_cnt.toString());
            }
            com_cnt_var += 1;
            for(comm=0;comm <= data.c_count;comm++){
                // get comment-reply variable
                var com = comm.toString();
                var c_id= data['c_id_' + com];
                var cr_count = data['cr_count_' + com];
                var c_username= data['c_username_' + com];
                var post_author_username = data['post_author_username'];
                var c_first_name = data['c_First_name_' + com];
                var c_last_name = data['c_Last_name_' + com];
                var c_profile_photo = data['c_profile_photo_' + com];
                var c_text = data['c_text_' + com];
                var c_date_created = data['c_date_created_' + com];
                var c_like_count = data['c_like_count_' + com];
                var c_like_unlike_btn = data['c_like_unlike_btn_' + com];


            if(req_username == post_author_username || req_username == c_username){
                comm_state += "<div class='modal m-0 p-0' id='maincommentDelete20" + c_id + "' tabindex='-1' role='dialog' aria-labelledby='maincommentDelete20" + c_id + "' aria-hidden='true'><div class='modal-dialog modal-dialog-centered' role='document'><div class='modal-content'><div class='modal-header text-white bg-dark'>";
                comm_state += "<h5 class='modal-title' id='maincommentDelete20" + c_id + "'>Alone-Blogger</h5><button type='button' class='close' data-dismiss='modal' aria-label='Close'><span style='color:white;' aria-hidden='true'>&times;</span></button></div><div class='modal-body'><h5 class='float-left'>Are You sure ? </h5>";
                comm_state += "<button type='button' id='main_comment_media_5008" + c_id + "href' data-href='/main_comment/" + c_id + "/comment_delete/' onclick=editable_comment('#main_comment_media_5008" + c_id + "','" + c_id + "','dlt') class='badge badge-dark float-right'>Delete</button>";
                comm_state += "</div></div></div></div>";
            }

    comm_state += "<div class='media col-md-12' id='main_comment_media_5008" + c_id + "'><a href='#reply_comment_5008"+ c_id + "'></a><img class='img-fluid rounded-circle mr-2' width='30' height='30' src='" ;
    if (c_profile_photo != undefined){
        comm_state += c_profile_photo + "' alt='pt'>";
    
    }
    else{
        comm_state += svg_img + "'alt='photo'>";
    }
    comm_state += "<div class='media-body'><div id='reply_comment_5008" + c_id + "'><p class='p-0 m-0'><a class='c-hover comment-hover-func-" + c_id + "' href='mailto:" + c_username + "' data-href='/account/" + c_username + "/comment_hover_user/' onmouseover='hover_func(" + c_id + ")' data-toggle='tooltip_" + c_id + "' data-html='true' title='" + c_username + "'>";
    if (c_first_name != undefined){
        comm_state += String(c_first_name + " " + c_last_name) + " <small class='text-muted'>@" + c_username + "</small>";
    }
    else{
        comm_state += String(c_username);
    }
    comm_state += "</a><small class='text-muted'>"; 
    if(c_username == post_author_username){ 
        comm_state += "<small style='background-color: #d9d8d7; border-radius: 10%;'>author</small>";
    } 
    comm_state += "(" + c_date_created + ")"; 
                    if (req_username == post_author_username || req_username == c_username){
                        comm_state += "<strong class='dropdown'><strong class='text-black dropbutton" + c_id + "main' type='button' id='dropdownMenuButton' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'> . . .</strong><small class='dropdown-menu' aria-labelledby='dropdownMenuButton'>";
                                            
                                if(req_username == c_username){
                                    comm_state += "<small type='button' onclick=editable_comment('#commtext','" + c_id + "main','') class='dropdown-item'>Edit</small>";
                                
                                }
                                comm_state += "<small type='button' data-toggle='modal' class='dropdown-item' data-target='#maincommentDelete20" + c_id + "'>Delete</small></small></strong>";
                    }
        comm_state += "</small></p><form id='commbox" + c_id + "main' data-href='/main_comment/" + c_id + "/edit_comment/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'> <small class='p-0 m-0' id='commtext" + c_id + "main'>" + c_text + "</small></form><small id='editabletext" + c_id + "mainbutton' onclick=editable_comment('#commbox','" + c_id + "main','sbmit')></small><small id='canceltext" + c_id + "mainbutton' onclick=editable_comment('#commtext','" + c_id + "main','cancel')></small></div>";
    if(data.user_authenticated){
        comm_state += "<ul class='list-inline pt-0'><li class='list-inline-item'><small class='comment_like_count_" + c_id + "-main text-muted' disabled>" + c_like_count + "</small> <a href='#'><small id='comment_likes_" + c_id + "-main' class='comment_like' onclick=follow_and_comment_like(event,'" + c_id + "-main') data-href='/main_comment/" + c_id + "/toggle_like/'>" + c_like_unlike_btn + " </small></a></li>";
        comm_state += "<li class='list-inline-item'><a data-toggle='collapse' href='#collapse" + c_id + "' aria-expanded='false' aria-controls='collapse" + c_id + "'><small id='editable-text-" + c_id + "-reply'><i class='fa fa-share'></i> reply</small></a></li></ul><div class='collapse' id='collapse" + c_id + "' data-parent='#accordian'><div class='card card-body mt-0 pt-0 border-0' style='background-color:rgb(244,244,244)'>";
        comm_state += "<form id='Public_comment_" + c_id + "' data-href='/" + post_author_username + "/comment/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'> <div class='form-group row'><input type='hidden' name='post' value='" + post_id + "'><input type='hidden' name='path' value='" + post_slug_name + "'><input type='hidden' name='reply_to' value='" + c_username + "'><input type='hidden' name='comment_id' value='" + c_id + "'><label class='border-info' for='message'>Type message</label>";
        comm_state += "<textarea class='form-control' name='message' id='main_message_" + c_id + "' rows='5' cols='50' placeholder='reply' required></textarea><button id='Public_comment_submit_btn" + c_id + "main' class='btn btn-sm bg-light shadow' type='submit' name='button' onclick=reply_Public_comment(event,'" + c_id + "','main') >reply</button></div></form></div></div>";
    }
    else{
        comm_state += "<a class='border-0 mb-3' id='editable-text-" + c_id + "-reply' type='button' data-toggle='modal' data-target='#exampleModalCenter'><small><i class='fa fa-share'></i>  reply</small></a>";   
    }
        for(comm_r=1;comm_r <= cr_count;comm_r += 1){
                var com_r = comm_r.toString();
                var cr_id= data['cr_id_' + com + '_' + com_r];
                var cr_username= data['cr_username_' + com + '_' + com_r];
                var cr_first_name = data['cr_First_name_' + com + '_' + com_r];
                var cr_last_name = data['cr_Last_name_' + com + '_' + com_r];
                var cr_profile_photo = data['cr_profile_photo_' + com + '_' + com_r];
                var cr_text = data['cr_text_' + com + '_' + com_r];
                var cr_reply_to = data['cr_reply_to_' + com + '_' + com_r];
                var cr_date_created = data['cr_date_created_' + com + '_' + com_r];
                var cr_like_count = data['cr_like_count_' + com + '_' + com_r];
                var cr_like_unlike_btn = data['cr_like_unlike_btn_' + com + '_' + com_r];
        //  Replied comments 
        comm_state += "<div class='media reply_comment_media_1008" + cr_id + "' id='reply_comment_1008" + cr_id + "'><a href='#reply_comment_1008" + cr_id + "'></a><img class='img-fluid rounded-circle mr-2' width='30' height='30' src='";
            if(cr_profile_photo){
                comm_state += cr_profile_photo;
            }
            else{
                comm_state += svg_img;
            }
            comm_state += "' alt='pt'><div class='media-body'><p class='p-0 m-0'><a class='c-hover comment-hover-func-r" + cr_id + "' href='mailto:" + cr_username + "' data-href='/account/" + cr_username + "/comment_hover_user/' onmouseover=hover_func(" + cr_id + ",'r') data-toggle='tooltip_r" + cr_id + "' data-html='true' title='" + cr_username + "'>";
                    if(cr_first_name != undefined){
                        comm_state += String(cr_first_name + " " + cr_last_name) + "<small class='text-muted'> @" + cr_username + "</small>";
                    }
                    else {
                        comm_state += cr_username;
                    }
                    comm_state += "</a><small class='text-muted'>";
                        if (cr_username == post_author_username) {
                            comm_state += "<small style='background-color: #d9d8d7; border-radius: 10%;'>author</small>";
                        }
                        comm_state += " (" + cr_date_created + ") <a href='/account/" + cr_username + "/dashboard/' class='badge badge-pill badge-dark'><i class='fa fa-share'> </i> " + cr_reply_to + "</a>";
                        if (req_username == post_author_username || req_username == cr_username){
                            comm_state += "<strong class='dropdown'><strong class='text-black dropbutton" + cr_id + "reply' type='button' id='dropdownMenuButton' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'> . . .</strong><small class='dropdown-menu' aria-labelledby='dropdownMenuButton'>";
                                if (req_username == cr_username){
                                    comm_state += "<small type='button' onclick=editable_comment('#commtext','" + cr_id + "reply','') class='dropdown-item'>Edit</small>";
                                }    
                                
                                comm_state += "<small type='button' data-toggle='modal' data-target='#replycommentDelete1" + cr_id + "' class='dropdown-item'>Delete</small></small></strong>";
                            }
                    comm_state += "</small></p><form id='commbox" + cr_id + "reply' data-href='/reply_comment/" + cr_id + "/edit_comment/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'> <small class='p-0 m-0' id='commtext" + cr_id + "reply'>" + cr_text + "</small></form>";
                comm_state += "<small id='editabletext" + cr_id + "replybutton' onclick=editable_comment('#commbox','" + cr_id + "reply','sbmit')></small><small id='canceltext" + cr_id + "replybutton' onclick=editable_comment('#commtext','" + cr_id + "reply','cancel')></small>";
                if (data.user_authenticated){
                    comm_state += "<ul class='list-inline pt-0'><li class='list-inline-item'><small class='comment_like_count_" + cr_id + "-reply text-muted' disabled>" + cr_like_count + "</small> <a href='#'><small id='comment_likes_" + cr_id + "-reply' class='comment_like' onclick=follow_and_comment_like(event,'" + cr_id + "-reply') data-href='/reply_comment/" + cr_id + "/toggle_like/'>" + cr_like_unlike_btn + "</small></a></li>";
                    comm_state += "<li class='list-inline-item'><a class='collapsed' data-toggle='collapse' href='#collapseExample1" + cr_id + "' aria-expanded='false' aria-controls='collapseExample" + cr_id + "'><small><i class='fa fa-share'></i> reply</small></a></li></ul><div class='collapse' id='collapseExample1" + cr_id + "' data-parent='#accordian'><div class='card card-body mt-0 pt-0 border-0' style='background-color:rgb(244,244,244)'>";
                    //   Reply comment Form
                    comm_state += "<form id='Public_comment_r" + cr_id + "' data-href='/" + post_author_username + "/comment/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'> <div class='form-group row'><input type='hidden' name='post' value='" + post_id + "'><input type='hidden' name='comment_id' value='" + c_id + "'><input type='hidden' name='path' value='" + post_slug_name + "'><input type='hidden' name='reply_to' value='"+ cr_username + "'><label class='border-info' for='message'>Type message</label>";
                    comm_state += "<textarea class='form-control' name='message' id='reply_message_" + cr_id + "' rows='5' cols='50' placeholder='reply' required></textarea><button id='Public_comment_submit_btn" + cr_id + "reply' class='btn btn-sm bg-light shadow' type='submit' name='button' onclick=reply_Public_comment(event,'" + cr_id + "','reply')>reply</button></div></form></div></div>";
                }
                else{
                    comm_state += "<a class='border-0 mb-3' type='button' data-toggle='modal' data-target='#exampleModalCenter'><small><i class='fa fa-share'></i> reply </small></a>"
                }
            comm_state += "</div></div>";
        if (req_username == cr_username || req_username == post_author_username){
            comm_state += "<div class='modal m-0 p-0' id='replycommentDelete1" + cr_id + "' tabindex='-1' role='dialog' aria-labelledby='replycommentDelete1" + cr_id + "' aria-hidden='true'><div class='modal-dialog modal-dialog-centered' role='document'><div class='modal-content'><div class='modal-header text-white bg-dark'><h5 class='modal-title' id='replycommentDelete1" + cr_id + " replycommentDelete1" + cr_id + "'>Alone-Blogger</h5>";
            comm_state += "<button type='button' class='close' data-dismiss='modal' aria-label='Close'><span style='color:white;' aria-hidden='true'>&times;</span></button></div><div class='modal-body'><h5 class='float-left'>Are You sure ? </h5>";
            comm_state += "<button type='button' id='reply_comment_1008" + cr_id + "href' data-href='/reply_comment/" + cr_id + "/comment_delete/' onclick=editable_comment('#reply_comment_1008" + cr_id + "','" + cr_id + "','dlt') class='badge badge-dark float-right'>Delete</button></div></div></div></div>";

        }
    }
        comm_state += "</div></div>";
        
    }
    comm_state += "<div class='media'><div class='media-body'><ul class='list-inline pt-0'><li class='list-inline-item'><a class='collapsed' data-toggle='collapse' href='#collapseExample2' aria-expanded='false' aria-controls='collapseExample2'><h4>comment: <i class='fa fa-comments'></i> </h4></a></li></ul><div class='collapse' id='collapseExample2' data-parent='#accordian'><div class='card card-body mt-0 pt-0 border-0' style='background-color:rgb(244,244,244)'>";
    comm_state += "<form id='Public_comment_main_comment' data-href='/" + post_author_username + "/comment/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'><div class='form-group row'><input type='hidden' name='post' value='" + post_id + "'><input type='hidden' name='path' value='" + post_slug_name + "'><label class='border-info' for='message'>Type message</label><textarea class='form-control' name='message' id='main_message_main_comment' rows='8' cols='80' placeholder='reply' required></textarea><button class='btn btn-sm bg-light shadow' id='Public_comment_submit_btnmain_commentmain' type='submit' name='button' onclick=reply_Public_comment(event,'main_comment','main') >Submit</button>";
    comm_state += "</div></form></div></div></div></div><hr></hr>";

    $('#accordian').html("").append(comm_state);
    var ts_ = $('.c-hover');
    ts_.attr('title',"<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
                
 },
 error:function(){

 }
})}
)};
    $(document).ready(function(){
        var class_name = ".followbtn,.followers-numberid,#unregister-user";
        var id_name="#linkgenerate,#logout_page,#subscribe,#registerForm,#loginForm";
        $(class_name).click(function(e){
            e.preventDefault();
            var this_ = $(this);
            if (!this_.hasClass('followers-numberid')){
                this_.html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> wait...");
            }
            $.ajax({
                type : 'GET',
                url :  this_.attr('data-href'),
                data : {},
                success: function(data){
                    this_.text(data.condition);
                    if(data.refresh==true){
                        refresh(data);
                    }
                    else{
                        this_part = $('.followers-numberid');
                        this_part.text(" " + data.count);
                        this_part_pop = $('.pop-followers-number' + data.slug);
                        this_part_pop.text(" " + data.count);
                    }
               },
               error: function(data){
                   location.href=data['responseJSON']['path'];
               }
           })
       });
        function on_error(data){
           if (data["responseJSON"]["pop_login"] == true){
               $("#loginForm")[0].reset();
               alert(data["responseJSON"]["false_message"]);
               // code
           }
           else if (data["responseJSON"]["pop_register"] == true){
               if (data["responseJSON"]["false_message"]["username"]=='** username already exists'){
                   setTimeout(function(){
                        alert(data["responseJSON"]["false_message"]["username"]);
                   }, 100);
               }
               else if (data["responseJSON"]['false_message']['email']=='Invalid Username'){
                   alert("** email not contain any space or special charcter before '@gmail.com or @yahoo.com'");
               }
               if (data["responseJSON"]["false_message"]["email"]=='** Email already exists') {
                   setTimeout(function(){
                        // $('#id_email').fadeOut('slow');
                        alert(data["responseJSON"]["false_message"]["email"]);
                   }, 100);
               }

               else if (data["responseJSON"]["false_message"]["email"]=='** Email must be in gmail.com only') {
                   alert(data["responseJSON"]["false_message"]["email"])
               }

               if (data["responseJSON"]["false_message"]["password2"]=='** Your password must be same') {
                   setTimeout(function(){
                        // $('#id_password').fadeOut('slow');
                        alert(data["responseJSON"]["false_message"]["password2"]);
                   }, 100);
               }

               // code
           }
           else if (data["responseJSON"]["logout"] == true){
               $("#logout_page")[0].reset();
               // code
           }
           else if (data["responseJSON"]["contact"] == true){
               location.reload();
               // code
           }
       };
   $(id_name).submit(function(s){
       s.preventDefault();
       var this_ = $(this);
       if (this_.hasClass('linkgenerate')){
        $('.hidebutton').html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> wait...");
       }
       var serializedData = $(this).serialize();
       $.ajax({
           type : 'POST',
           url :  this_.attr('data-href'),
           data : serializedData,
           success: function(data){
               if(this_.hasClass('subscribe')){
                   $('.alrt').fadeIn('slow').load(location.href + " .alrt").delay(3000).fadeOut('slow');

               }
               else if(this_.hasClass('linkgenerate')){
                   $('.hidebutton').html('');
                //    console.log(data.link);
                   $('.pastelink').html(data.link);
               }
               else {
                   location.reload();
               }
            },
           error: function(data){
               if(this_.hasClass('subscribe')){
                   $('.alrt').fadeIn('slow').load(location.href + " .alrt").delay(3000).fadeOut('slow');

               }
               else{
                   on_error(data=data);
               }
           },
      },)
  })
})
