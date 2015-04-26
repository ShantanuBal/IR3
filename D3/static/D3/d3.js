jQuery(document).ready(function() {
    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');
 
        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });

     $("#submit").click(function(){
        //var query = document.getElementById('query').value;
    $.ajax({url: "http://127.0.0.1:8000/d3/", success: function(result){
        $("#tab1").html(result);
    }});
});
});