async function bookInfo(){
    if (tokenData !== null) {
        window.location.href="/booking";
    } else{
        openDialog("login-dialog");
    }
}