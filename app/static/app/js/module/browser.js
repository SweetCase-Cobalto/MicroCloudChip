const INVALID_DIRECTORY_CHARSET = ['/', '\'', '"', '?', '!', '>', '<', '|', '*', ';'];

function checkDirectoryName(filename) {
    if(filename.length == 0) { return false; }
    else if(filename.length == 1) {
        if(filename.charAt(0) === ' ') { return false; }
        else {
            var flag = true;
            INVALID_DIRECTORY_CHARSET.forEach(invalidChar => {
                if(filename.charAt(0) === invalidChar) { flag = false; }
            });
            
            return flag;
        }
    } else {
        if(filename.charAt(0) === ' ' || filename.charAt(filename.length-1) ===' ') { return false; }
        for(var i = 0; i < filename.length; i++) {
            var flag = true;
            INVALID_DIRECTORY_CHARSET.forEach(invalidChar => {
                if((filename.charAt(i) === invalidChar) == true) {
                    flag = false;
                    return;
                }
            });
            if(!flag) { return false; }
        }
        return true;
    }
}