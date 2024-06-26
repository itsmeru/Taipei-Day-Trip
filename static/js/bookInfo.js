async function bookInfo(){
    if (tokenData){ //from account.js (global variable)
        window.location.href="/booking";
    }
    else{
        openDialog("login-dialog");
    }
}