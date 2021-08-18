window.addEventListener('DOMContentLoaded', event => {

    const datatablesSimple = document.getElementById('datatablesSimple');
    const datatablesSimpleuser = document.getElementById('datatablesSimpleusers');
    const datatablesSimpleprofile = document.getElementById('datatablesSimpleprofile');
    const datatablesSimpleBooking = document.getElementById('datatablesSimpleBooking');
    const datatablesPayment = document.getElementById('datatablesPayment');


    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
    if (datatablesSimpleuser) {
        new simpleDatatables.DataTable(datatablesSimpleuser);
    }
    if (datatablesSimpleprofile) {
        new simpleDatatables.DataTable(datatablesSimpleprofile);
    }
    if (datatablesSimpleBooking) {
        new simpleDatatables.DataTable(datatablesSimpleBooking);
    }
    if (datatablesPayment) {
        new simpleDatatables.DataTable(datatablesPayment);
    }
});
