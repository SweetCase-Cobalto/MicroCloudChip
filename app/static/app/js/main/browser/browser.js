$(() => {

    /* Menu buttons */
    // upload button event when file selected
    $('#upload-files').change((e) => {
        $('#go-to-upload-btn').css("visibility", "visible");
    });

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
    
    // click file item & download
    $('.file-item').click((e) => {
        var targetFile = e.target.id;
        var targetForm = targetFile + "-form"
        document.getElementById(targetForm).submit();
    });

    // Make New Directory
    $('#menu-browser-new-directory').click(() => {
        let newDirectoryName = prompt("Write New Directory Name");

        // Check File Name
        if(!checkDirectoryName(newDirectoryName)) {
            alert("Directory name is invalid");
            return;
        } else {
            document.getElementById('new-directory-name').value = newDirectoryName;
            document.getElementById('new-directory-form').submit();
        }

    });
});