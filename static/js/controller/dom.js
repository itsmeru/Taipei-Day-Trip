import { statusBtn } from "../statusBtn.js";
document.addEventListener("DOMContentLoaded", async () => {
    const CLIENT_ID = "108619231081-5sc2vtc5ch8g08b4g0lk9lb4svep88nu.apps.googleusercontent.com";
    google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
        document.getElementById("g_id_onload"),
        { 
            prompt: "select_account" ,
             theme: "outline",
              size: "large",
              width:"310",
        }
    );

    function handleCredentialResponse(response) {
        let id_token = response.credential;
        localStorage.setItem("googleAuth",id_token);
        closeDialog("login-dialog");
        window.location.reload();
    }
    window.tokenResult = await statusBtn();
    if(typeof window.tokenCheckCallback === "function"){
        window.tokenCheckCallback(window.tokenResult)
    }

      
});
