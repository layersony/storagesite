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
<<<<<<< HEAD
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

=======
    

    $('.view_unit').click(function(){
        var unitName = $(this).attr('data-unitname');
        var monthlyCharge = $(this).attr('data-monthly');
        var onsite_booking_url = "onsite_booking/" + unitName

        $('#unitName').text(unitName);
        $('#monthlyCharge').text(monthlyCharge);
        $('#onsiteBooking').attr('href', onsite_booking_url);
    })
>>>>>>> master

    $("#id_end_date").datetimepicker(
      {
        format: 'Y-m-d H:i:i',
        formatTime: 'H:i:i',
        formatDate: 'Y-m-d',
      }
    );

    
});

new Autocomplete('#autocomplete', {
    search: input => {
        if (input.length < 1) {
            return []
        }
        const url = `/employee/search_client/?client=${input}`

        return new Promise(resolve => {
            fetch(url)
            .then(response => response.json())
            .then(data => {
                
                resolve(data.data);
            })
        })
        }
    })
