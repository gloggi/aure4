
$(function () {
    $('#id_email').focus();

    $('select[disable=True]').click(function(e) {
        e.preventDefault();
    })

    $('#id_abteilung').change(function() {
        if ($(this).val() == 'andere') {
            $('#abteilung_create').slideDown();
        } else {
            $('#abteilung_create').hide();
        }
    });

    $('#id_abteilung').change();

});
