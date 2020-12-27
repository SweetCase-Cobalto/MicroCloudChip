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
    
    // click file item
    $('.file-item').click((e) => {
        var targetFile = e.target.id;
        var targetForm = targetFile + "-form"
        document.getElementById(targetForm).submit();
    });
});