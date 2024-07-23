async function bookInfo(){
    if (window.tokenResult !== null) {
        window.location.href="/booking";
    } else{
        openDialog("login-dialog");
    }
}
async function board(){
    if (window.tokenResult !== null) {
        window.location.href="/board";
    } else{
        openDialog("login-dialog");
    }
}