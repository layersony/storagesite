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

    

    $('.view_unit').click(function(){
        var unitName = $(this).attr('data-unitname');
        var unitWidth = $(this).attr('data-unitwidth');
        var unitHeight = $(this).attr('data-unitheight');
        var unitLength = $(this).attr('data-unitlength');
        var unitSize = $(this).attr('data-unitsize');
        var unitOccupied = $(this).attr('data-occupied');
        var dailyCharge = $(this).attr('data-daily');
        var weeklyCharge = $(this).attr('data-weekly');
        var monthlyCharge = $(this).attr('data-monthly');
        var property = $(this).attr('data-property');
        var temp = $(this).attr('data-temp');
        var onsite_booking_url = "onsite_booking/" + unitName
        var delete_url = "delete_unit/" + unitName


        $('#unitName').text(unitName);
        $('#unitWidth').text(unitWidth);
        $('#unitHeight').text(unitHeight);
        $('#unitLength').text(unitLength);
        $('#unitSize').text(unitSize);
        $('#status').text(unitOccupied);
        $('#monthlyCharge').text(monthlyCharge);
        $('#weeklyCharge').text(weeklyCharge);
        $('#dailyCharge').text(dailyCharge);
        $('#property').text(property);
        $('#temp').text(temp);
        $('#onsiteBooking').attr('href', onsite_booking_url);
        $('#deleteUnit').attr('href', delete_url);

    })

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
