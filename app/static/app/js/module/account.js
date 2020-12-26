// 아이디/패스워드 조건
const ID_MAX_LENGTH = 12
const ID_MIN_LENGTH = 4
const ID_RE         = /^[a-zA-Z0-9]{4,12}$/;

const PSWD_MAX_LENGTH = 16
const PSWD_MIN_LENGTH = 4

function check_id(target_id) {
    if(target_id.length < ID_MIN_LENGTH || target_id.length > ID_MAX_LENGTH) {

        return false;
    }
    else if(!ID_RE.test(target_id)) {
        return false;
    }
    else {
        return true;
    }
}
function check_pswd(target_pswd) {
    if(target_pswd.length < PSWD_MIN_LENGTH || target_pswd.length > PSWD_MAX_LENGTH) {
        return false;
    } else {
        return true;
    }
}