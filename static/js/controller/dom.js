import { statusBtn } from "../statusBtn.js";
document.addEventListener("DOMContentLoaded", async () => {
    window.tokenResult = await statusBtn();
    if(typeof window.tokenCheckCallback === "function"){
        window.tokenCheckCallback(window.tokenResult)
    }
});
