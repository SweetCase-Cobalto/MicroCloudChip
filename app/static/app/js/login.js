$(() => {
    $('#login-btn').click(() => {
        // Checking Logins
        
        document.getElementById('editor').submit();
    });
    $('#login-btn').hover(() => {
        $('#login-btn').css("color", "#AECCD1");
        console.log('a');
    }, () => {
        $('#login-btn').css("color", "#277BBA");
    });
});