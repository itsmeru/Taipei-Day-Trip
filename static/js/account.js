document.addEventListener("DOMContentLoaded", async () => {
  let loginBtn = document.getElementById("login-btn");
  let logoutBtn = document.getElementById("logout-btn");
    let token = localStorage.getItem("authToken");
    if (token) {
        let res = await fetch("/api/user/auth", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        let result = await res.json();
        if (result.data !== "None") {
          logoutBtn.classList.remove("hidden");
        }else{
          localStorage.removeItem("authToken");
          loginBtn.classList.remove("hidden");
        }
    } else{
      localStorage.removeItem("authToken");
      loginBtn.classList.remove("hidden");
    }
});


async function signUp(event, form) {
  await handleForm(event, form,"/api/user","POST",()=>{
    showMessage(form, "註冊成功，請登入系統", "msg", "green");
    form.reset();
  })
}

async function signIn(event, form) {
  await handleForm(event,form,"/api/user/auth","PUT",(result)=>{
    localStorage.setItem("authToken",result.token);
    closeDialog("login-dialog");
    form.reset();
    window.location.reload();
  })
}

async function handleForm(event, form, url, method,sucessCb){
  event.preventDefault(); 
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  clearMessage(form);
  try{
    let res = await fetch(url,{
      method: method,
      headers:{"Content-Type": "application/json"},
      body: JSON.stringify({
        name: form.name?.value,
        email: form.email.value,
        password: form.password.value,
      })
    })
    let result = await res.json();
    if (!res.ok) throw new Error(result.message);
    sucessCb(result);
  }catch (err){
    showMessage(form, err.message, "error-message", "red");
    form.reset();
  }
  
}
async function showMessage(form, message, className, color){
  let messageDiv = form.querySelector(`.${className}`);
  if (!messageDiv) {
    messageDiv = document.createElement("div");
    messageDiv.classList.add(className);
    form.querySelector(".dialog-button").insertAdjacentElement("afterend", messageDiv);
  }
  messageDiv.textContent = message;
  messageDiv.style.color = color;
}



async function logout() {
  localStorage.removeItem("authToken");
  window.location.reload();
};