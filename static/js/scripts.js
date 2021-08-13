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
  
  $('#id_pickup').click(function() {
    if ($('#id_pickup').checked){
      alert('amazing')
    }else{
      alert('unchecked')
    }
  });
});

