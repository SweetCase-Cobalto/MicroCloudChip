// Selected data list
var selectedDirectoryList = [];
var selectedFileList = [];


$(() => {

    $(document).ready(() => {
        $.ajax({
            url: "/microcloudchip/get_usage",
            type: "get",
            success: function(data) {
                var total = 0;
                var used = 0;
                var total_label = "byte";
                var used_label = "byte";
                var number_string = "";

                // Check Total
                if(data.total < 1000) { total = data.total; }
                else if(data.total < Math.pow(1000, 2)) { total = data.total/1000; total_label = "KB"; }
                else if(data.total < Math.pow(1000, 3)) { total = data.total/Math.pow(1000, 2); total_label = "MB"; }
                else if(data.total < Math.pow(1000, 4)) { total = data.total/Math.pow(1000, 3); total_label = "GB"; }
                else { total = data.total/Math.pow(1000, 4); total_label = "TB"; }

                // Check Usage
                if(data.used < 1000) { used = data.used; }
                else if(data.used < Math.pow(1000, 2)) { used = data.used/1000; used_label = "KB"; }
                else if(data.used < Math.pow(1000, 3)) { used = data.used/Math.pow(1000, 2); used_label = "MB"; }
                else if(data.used < Math.pow(1000, 4)) { used = data.used/Math.pow(1000, 3); used_label = "GB"; }
                else { used = data.used/Math.pow(1000, 4); used_label = "TB"; }
                
                // Make String
                total = total.toFixed(1);
                used = used.toFixed(1);

                number_string = used.toString() + used_label + " / " + total.toString() + total_label;

                // Change String
                $('#gate-to-number').text(number_string);
                
                // Change Percentage
                var used_percentage = parseInt(((data.used/data.total) * 100));
                var empty_percentage = 100 - used_percentage;

                $('#used-line').css("width", used_percentage.toString()+"%");
                $('#unused-line').css("width", empty_percentage.toString()+"%");
                
            }
        });
    });
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