import {tokenCheck} from "./controller/token.js"

async function statusBtn(){
    let loginBtn = document.getElementById("login-btn");
    let logoutBtn = document.getElementById("logout-btn");
    let tokenResult = await tokenCheck();
    if (tokenResult === null){
        localStorage.removeItem("authToken");
        loginBtn.classList.remove("hidden");
    }
    else{
        logoutBtn.classList.remove("hidden");
    }
    return tokenResult;
}
export {statusBtn};
