let p1_selection = '',
    p2_selection = '';


$('.p1-nav-dropdown .dropdown-item').click(function() {
    p1_selection = this.id;
    p2_selection = '';


    $('.p2').hide();
    $('.poem-2-' + this.id.split("-")[2]).show();
});
$('.p2-nav-dropdown .dropdown-item').click(function() { p2_selection = this.id; });

$('.poem-submit').click(function() {
   if (!p1_selection) { alert('Please select a poem from the `Poem 1` dropdown'); }
   else if (!p2_selection) { alert('Please select a poem from the `Poem 2` dropdown'); }
   else {
       let p1_id = p1_selection.split("-")[2],
           p2_id = p2_selection.split("-")[2];

       if (p1_id !== p2_id) {
           window.location.replace("http://127.0.0.1:5000/" + p1_id + "/" + p2_id);
       } else {
           alert('Please make sure selections are unique.');
       }
   }
});