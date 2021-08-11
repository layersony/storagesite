window.addEventListener('DOMContentLoaded', event => {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});

$(document).ready(function(){
  $("#id_end_date").datetimepicker(
    {
      format: 'Y-m-d H:i:i',
      formatTime: 'H:i:i',
      formatDate: 'Y-m-d',
    }
  );

});

$(document).ready(function(){
  $('#checkout').click(function(){
    bookingdetails = $('#bookingid').html()
    let leave = prompt('Are you sure you want to Move Out? (yes/no)').toLowerCase()

    
    if (leave == 'yes'){
      $.ajax({
        'url': '/ajax/checkout/',
        'type':'GET',
        'data':bookingdetails,
        'dataType': 'json',
        'success': function(data){
          console.log(data)
        }
      })
    }else if( leave == 'no'){
      console.log('stays')
    }else{
      alert('Invalid!, Enter Yes or No')
    }
  })
});