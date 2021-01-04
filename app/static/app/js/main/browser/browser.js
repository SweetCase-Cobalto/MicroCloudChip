// Selected data list
var selectedDirectoryList = [];
var selectedFileList = [];


$(() => {

    // Refresh event must be empty
    $(window).bind('beforeunload', (e) => {
    });
    
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
        if(newDirectoryName === null) { return; }

        if(!checkDirectoryName(newDirectoryName)) {
            alert("Directory name is invalid");
            return;
        } else {
            document.getElementById('new-directory-name').value = newDirectoryName;
            document.getElementById('new-directory-form').submit();
        }

    });
    

    // Selected Directory Checkbox
    $(".directory-checkbox").change((e) => {
        dirName = e.target.name;
        
        if(e.target.checked) {
            if(selectedDirectoryList.findIndex((e) => {
                if(dirName == e) { return true; }
            }) === -1) {
                selectedDirectoryList.push(dirName);
            }
        } else {
            const deletedIndex = selectedDirectoryList.findIndex((e) => {
                if(dirName == e) { return true; }
            });
            if(deletedIndex != -1) {
                selectedDirectoryList.splice(deletedIndex, 1);
            }
        }
    });
    // Selected File Checkbox
    $(".file-checkbox").change((e) => {
        fileName = e.target.name;

        if(e.target.checked) {
            if(selectedFileList.findIndex((e) => {
                if(fileName == e) { return true }
            }) === -1) {
                selectedFileList.push(fileName);
            }
        } else {
            const deletedIndex = selectedFileList.findIndex((e) => {
                if(fileName == e) { return true; }
            });
            if(deletedIndex != -1) {
                selectedFileList.splice(deletedIndex, 1);
            }
        }
    });

    // Upload Mutiple Files
    $('#menu-browser-download').click(() => {
        if(selectedFileList.length == 0 && selectedDirectoryList == 0) {
            alert('Selected Directory or File');
            return;
        } 
        selectedDirectoryString = ""
        selectedFileString = ""

        for(var idx in selectedDirectoryList) {
            selectedDirectoryString += selectedDirectoryList[idx] + ">";
        }
        for(var idx in selectedFileList) {
            selectedFileString += selectedFileList[idx] + ">"
        }

        document.getElementById('selected-directories').value = selectedDirectoryString.slice(0, selectedDirectoryString.length - 1);
        document.getElementById('selected-files').value = selectedFileString.slice(0, selectedFileString.length - 1);
        document.getElementById('download-multiple-form').submit();
    });

    // Delete Driectory
    $('#menu-browser-delete').click(() => {
        if(selectedFileList.length == 0 && selectedDirectoryList == 0) {
            alert('Selected Directory or File to delete');
            return;
        }
        if(confirm('Are you sure to Delete This Data?')) {
            selectedDirectoryString = ""
            selectedFileString = ""
            for(var idx in selectedDirectoryList) {
                selectedDirectoryString += selectedDirectoryList[idx] + ">";
            }
            for(var idx in selectedFileList) {
                selectedFileString  += selectedFileList[idx] + ">";
            }
            document.getElementById('deleted-directories').value = selectedDirectoryString.slice(0, selectedDirectoryString.length - 1);
            document.getElementById('deleted-files').value = selectedFileString.slice(0, selectedFileString.length - 1);
            document.getElementById('delete-form').submit();
        } else {
            return;
        }
    });
    
});