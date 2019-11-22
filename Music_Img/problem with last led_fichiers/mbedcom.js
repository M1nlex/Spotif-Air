// w
$.ajaxSetup({ cache: true });
var browser_name = (jQuery.browser.msie ? "ie" : (
  jQuery.browser.webkit ? "webkit" : (
    jQuery.browser.mozilla ? "mozilla" : "unknown"
  )
));
browser_name += (jQuery.browser.version ? jQuery.browser.version : "0");

// This version of Chrome seems to be causing problems with hanging apache
// workers, let's just disable syntax highlighting for it
if (browser_name !== 'webkit67.0.3396.87') {
  $.getScript("/compiler/?request=/ijs/theitf:theitf;aboutedit&SA=1&browser="+browser_name+"&v=1.05", function () {
      setTimeout(function() {
          if ($.isReady && typeof codifyByClass != 'undefined') {
              codifyByTagClass('pre', 'fragment');
              codifyByTagClass('pre', 'mbed-code');
              codifyByTagClass('pre', 'mbed-diff', 0, 1);
          } else {
              setTimeout(arguments.callee, 100);
          }
      });
  });
}

$.ajaxSetup({ cache: false });


// When the DOM has loaded, init the form link.
$(document).ready(function() {
    $("abbr.timeago").timeago();
    add_dynamic();
    //SyntaxHighlighter.config.toolbar = false;

    //SyntaxHighlighter.all()
    $.ajaxSetup ({
        cache: false
    });

    var loadUrl = "/jsutil/preview/";
    $("#preview").click(function() {
        $("#loading").html("<img src='/static/img/spin.gif' alt='loading...' />");

        $('#result').show('fast');
        var title = '';
        if ($("#id_name").length != 0) {
            title = $("#id_name").val().replace(/-/g,' ')
        }
        var content = $("#id_content").val();
        var wikislug = $("#id_wikislug").val();
        if ($("#id_content").length == 0) {
            content = $("#id_body").val();
            if ($("#id_body").length == 0) {
                content = $("#id_comment").val();
            }
        }

        $("#resultcontent").load(loadUrl, { title: title, content: content, wikislug: wikislug },
            function(){
                $("#loading").html("");
                codifyByClass('mbed-code');
            });
    });

    $("#bpreview").click(function() {
        $("#loading").html("<img src='/static/img/spin.gif' alt='loading...' />");
        var title = '';
        $('#result').show('fast');
        var content =  $("#id_preview").val() + $("#id_body").val();

        $("#resultcontent").load(loadUrl, {title:title, content:content},
            function(){
                $("#loading").html("");
            });
    });

    $(".archived-label").click(function (e) {
        e.target.style.display = "none";
        $(e.target.parentNode).removeClass("archived");
    });

    $('#post-comment, #post-comment-bottom').toggle(function() {
        $("#comment-form").slideDown("slow");
        scrollToElement("#comment-form");

    }, function() {
        $("#comment-form").slideUp("slow");
        scrollToElement("#comment-form");

    });
});


function getSelText() {
    var txt = '';
    if (window.getSelection) {
        txt = window.getSelection();
    } else if (document.getSelection) {
        txt = document.getSelection();
    } else if (document.selection) {
        txt = document.selection.createRange().text;
    }
    return txt
}

function scrollToElement(selector, time, verticalOffset) {
    time = typeof(time) != 'undefined' ? time : 1000;
    verticalOffset = typeof(verticalOffset) != 'undefined' ? verticalOffset : 0;
    element = $(selector);
    offset = element.offset();
    offsetTop = offset.top + verticalOffset;
    $('html, body').animate({
        scrollTop: offsetTop
    }, time);
}

function add_dynamic() {
    $(".quotelink").click( function(objEvent) {
           var postId = $(objEvent.target);
           var quoteBody = getSelText().toString();
           if (quoteBody.length == 0) {
                quoteBody = $(postId).parent().parent().find(".comment-messagebody").html();
           }
           var quoteAuthor = $(postId).parent().parent().parent().find(".authortext").html();
           tinyMCE.execInstanceCommand('id_body', 'mceInsertContent', 0, '<blockquote class="quote"><span class="quoteheader">' + quoteAuthor + 
                ' wrote:</span><br/> ' + quoteBody + '</blockquote>');
           $('#comment-form').slideDown('slow');
           scrollToElement("#comment-form");
        }
    );

    $(".quotelink2").click(function( objEvent ) {
           var postId = $(objEvent.target).parent().parent().parent();
           var quoteBody = getSelText().toString();

           if (quoteBody.length == 0) {
                quoteBody = unescape($(postId).find(".comment-wikitext").text());
           }
           var quoteAuthor = $(postId).parent().find(".authorusername").html();
           insertAtCaret('id_content', "\n<<quote " + quoteAuthor + ">>\n" + quoteBody.trim() + "\n<</quote>>\n");
           $('#comment-form').slideDown('slow');
           scrollToElement("#comment-form");
        }
    );

    $(".quotelink3").click(function( objEvent ){
           var postId = $(objEvent.target);
           var quoteBody = getSelText().toString();

           if (quoteBody.length == 0) {
                quoteBody = unescape($(postId).parent().parent().find(".comment-wikitext").text());
           }
           var quoteAuthor = $(postId).parent().parent().parent().find(".authorusername").html();
           insertAtCaret('id_body', "\n<<quote " + quoteAuthor + ">>\n" + quoteBody + "\n<</quote>>\n");
           $('#comment-form').slideDown('slow');
           scrollToElement("#comment-form");
        }
    );
}

function confirmpost(url, conftext) {
    var agree = confirm(conftext);
    if (agree) {
        $.post(url);
        window.location.reload();
        return true;
    }
    else
        return false;
}

function follow(obj, id, app, model) {
   $.get("/follow/", { id: id, a: app, m: model}, function(data){
        if (data == '1') {  
            $(obj).attr('class', 'button small secondary btn-unfollow') ;
            $(obj).html('   Following' );
            $(obj).attr('title', '"You are following this item. Click to unfollow.');
        } else { 
            $(obj).attr('class', 'button small secondary btn-follow');
            $(obj).html('   Follow' );
            $(obj).attr('title', 'Click to follow ');
        }
   });
}
 
function favourite(obj, id, app, name, model) {
   $.get("/favourite/", { id: id, a: app, n: name, m: model}, function(data) {
        if (data == '1') {
            $(obj).attr('src', '/static/img/icons/star.png') ;
        } else { 
            $(obj).attr('src', '/static/img/icons/greystar.png');
        }
   });
}
  
function insertAtCaret(areaId, ins) {
    //modified to work with the filebrowser popup:
    if (window.opener) {
        var el = window.opener.document.getElementById(areaId);
    } else {
        var el = document.getElementById(areaId);
    }
    if (el.setSelectionRange){
        el.value = el.value.substring(0,el.selectionStart) + ins + el.value.substring(el.selectionStart,el.selectionEnd) + el.value.substring(el.selectionEnd,el.value.length);
    }
    else if (window.opener.document.selection && window.opener.document.selection.createRange) {
        el.focus();
        var range = window.opener.document.selection.createRange();
        range.text = ins + range.text;
    }
}
