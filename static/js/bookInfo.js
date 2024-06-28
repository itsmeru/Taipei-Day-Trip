async function bookInfo(){
    if (window.tokenResult !== null) {
        window.location.href="/booking";
    } else{
        openDialog("login-dialog");
    }
}