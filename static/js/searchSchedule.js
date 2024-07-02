function searchSchedule(){
    if (window.tokenResult !== null) {
        window.location.href="/thankyou";
    } else{
        openDialog("login-dialog");
    }
}