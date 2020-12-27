$(() => {
    // click back button
    $('#back').click(() => {
        document.getElementById('back-form').submit();
    });

    // click directory item
    $('.directory-item').click( (e) => {
        var targetDirectory = e.target.id;
        var targetForm = targetDirectory+"-form";
        document.getElementById(targetForm).submit();
    });
});