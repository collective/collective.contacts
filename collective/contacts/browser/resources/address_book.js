
function categories_counter(category){
        len = jq("#"+category+"-collapsable li").length
        jq("#"+category+"-len").html("("+len+")");
}

function persons_counter(){
    len = jq(".members-listing ul li").length;
    jq("#persons-len").html("("+len+")");
}
variables_record= {};
function selectorManager(group_of_selectables, dataset_name){
    group_of_selectables.click(function(){
        if (variables_record[dataset_name] && variables_record[dataset_name] != this){
            jq(variables_record[dataset_name]).removeClass('selected');
        }
        jq(this).addClass('selected');
        variables_record[dataset_name] = this;
    });
}
function clearDataset(dataset_name){
    delete variables_record[dataset_name];
}


function collapsablePanels(){
    jq.each(jq('.collapsable-trigger'), function(){
        jq(this).click(function(event){
            event.preventDefault();
            collapsable = jq(this).attr('href');
            jq(collapsable).toggleClass('collapse');
            jq(this).toggleClass('add');
        });
    });
}


function getParams(str) {
    var params = str.split("?")[1].split("&");
    var result = Array();
    var i = 0;
    for(i=0;i<params.length;i=i+1){
        var param = params[i].split("=");
        if(param.length == 2){
            result[param[0]] = param[1];
        }
    }
    return result;
}

function ajaxCallMemberData(element) {
    jq('.member-data-wrapper').empty();
    jq('.members-data .ajax-loader').css('display', 'block');
    jq.ajax({
        url: "@@member_data_view",
        data: ({memberUID : getParams(jq(element).attr('UID'))['memberUID']}),
        dataType: "html",
        success: function(html) {
            jq('.members-data .ajax-loader').css('display', 'none');
            jq('.members-data .member-data-wrapper').html(html);
        }
    });
}


function ajaxCall(element) {
    jq('.members-listing').empty();
    jq('.members .ajax-loader').css('display', 'block');

    var uid_str = "";
    if(element==undefined){
        uid_str = jq('#catUID').val();
    }else{
        uid_str = getParams(jq(element).attr('UID'))['UID'];
    }
    var json_data = jq.ajax({
          url: "@@member_listing_view",
          data: ({UID : uid_str,
                  search:jq('.members #searchMembers').val()}),
          dataType: "html",
          success: function(html_members) {
                jq('.members .ajax-loader').css('display', 'none');
                jq('.members .members-listing').html(html_members);
                jq('.members a').each(function(){
                    jq(this).attr('UID', jq(this).attr('href'));
                    jq(this).removeAttr('href');
                });
                jq('.members a').click(function(){
                    ajaxCallMemberData(jq(this));
                });
                //new list so we need new css selected handler
                selectorManager(jq('.members a.selectable'), 'members');
                persons_counter()
              }
       }
    );
}
jq(document).ready(function() {

    jq("#AddressBookView").bind("keypress", function(e) {
             if (e.keyCode == 13) {
                //~ ajaxCall();
                 return false;
            }
         });

    /* var search_button = jq('.members .find');
    jq("<a class='search_persons_button'>Search</a>").insertAfter(search_button);
    search_button.remove();*/

    jq('.categories a.selectable').click(function(){
        jq(this).attr('UID', jq(this).attr('href'));
        jq(this).removeAttr('href');
        jq('#catUID').val(getParams(jq(this).attr('UID'))['UID']);
        ajaxCall(jq(this));
        clearDataset('members'); //clear the selected information
    });

   jq('.members a.selectable').click(function(){
        jq(this).attr('UID', jq(this).attr('href'));
        jq(this).removeAttr('href');
        ajaxCallMemberData(jq(this));
        });
    jq('.members .find').css( 'display', 'None' ).attr("disabled", "true");
    jq('.members #searchMembers').attr("class", "ajax");
    jq('.members #searchMembers').bind("keypress", function(e) {
             if (e.keyCode == 13) {
                 ajaxCall();

            }
    });
    jq('.categories a.selectable').each(function(){
       jq(this).attr('UID', jq(this).attr('href'));
       jq(this).removeAttr('href');
    });
    jq('.members a.selectable').each(function(){
       jq(this).attr('UID', jq(this).attr('href'));
       jq(this).removeAttr('href');
    });

    //handler for the css class selected
    selectorManager(jq('.categories a.selectable'), 'categories');
    selectorManager(jq('.members a.selectable'), 'members');

    //handler for collapsable panels
    collapsablePanels();
    categories_counter("groups");
    categories_counter("org");
    persons_counter();
});
