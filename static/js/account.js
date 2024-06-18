document.addEventListener("DOMContentLoaded",()=>{
  let token = localStorage.getItem("authToken");
  if (token){
    fetch("/api/user/auth",{
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,  
        "Content-Type": "application/json"
      }
    }).then((res)=>res.json())
      .then((result)=>{
        if (result.data !== "None"){
          toggleLogoutButton();
        }
      })
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
    toggleLogoutButton();
    form.reset();
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



function toggleLogoutButton() {
  let nav_button = document.querySelector("#toggle-btn");
  if (localStorage.getItem("authToken")) {
    nav_button.textContent = "登出系統";
    nav_button.onclick = logout;
  } else {
    nav_button.textContent = "登入/註冊";
    nav_button.onclick = function() {
      openDialog("login-dialog");
    };
  }
}
async function logout() {
  localStorage.removeItem("authToken");
  toggleLogoutButton();
};

