async function bookInfo(){
    let token = localStorage.getItem("authToken");
    if (token){
        window.location.href="/booking";
    }
    else{
        openDialog('login-dialog');
    }
}