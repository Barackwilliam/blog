function get_discuss_func(event){
    $(document).ready(function(){
     var this_ = $('.get_discuss');
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
         comm_state += "<form id='Public_comment_" + c_id + "' data-href='/q/discuss_q_and_a/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'> <div class='form-group row'><input type='hidden' name='post' value='" + post_id + "'><input type='hidden' name='path' value='" + post_slug_name + "'><input type='hidden' name='reply_to' value='" + c_username + "'><input type='hidden' name='comment_id' value='" + c_id + "'><label class='border-info' for='message'>Type message</label>";
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
     comm_state += "<form id='Public_comment_main_comment' data-href='/q/discuss_q_and_a/'><input type='hidden' name='csrfmiddlewaretoken' value='" + token + "'><div class='form-group row'><input type='hidden' name='post' value='" + post_id + "'><input type='hidden' name='path' value='" + post_slug_name + "'><label class='border-info' for='message'>Type message</label><textarea class='form-control' name='message' id='main_message_main_comment' rows='8' cols='80' placeholder='reply' required></textarea><button class='btn btn-sm bg-light shadow' id='Public_comment_submit_btnmain_commentmain' type='submit' name='button' onclick=reply_Public_comment(event,'main_comment','main') >Submit</button>";
     comm_state += "</div></form></div></div></div></div><hr></hr>";
 
     $('#accordian').html("").append(comm_state);
     var ts_ = $('.c-hover');
     ts_.attr('title',"<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>");
                 
  },
  error:function(){
 
  }
 })}
 )};