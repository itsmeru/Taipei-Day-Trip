async function tokenCheck(){
    let loginBtn = document.getElementById("login-btn");
    let logoutBtn = document.getElementById("logout-btn");
    let token = localStorage.getItem("authToken");
      if (token) {
          let res = await fetch("/api/user/auth", {
            method: "GET",
            headers: {
              "Authorization": `${token}`,
              "Content-Type": "application/json"
            }
          });
          let result = await res.json();
          if (!res.ok){
            alert(result.error);
            window.location.reload();
            localStorage.removeItem("authToken");
            loginBtn.classList.remove("hidden");
            return null
          }
          if (result.data !== null) {
            logoutBtn.classList.remove("hidden");
            return result.data
          }else{
            localStorage.removeItem("authToken");
            loginBtn.classList.remove("hidden");
            return null
          }
      } else{
        localStorage.removeItem("authToken");
        loginBtn.classList.remove("hidden");
        return null

      }
}
