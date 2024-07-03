async function tokenCheck(){
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
        if (!res.ok){ // 過期
          alert(result.error);
          window.location.reload();
          return null
        }
        if (result.data !== null) {
          return result.data
        }else{ // 驗證失敗
          return null
        }
    } 
    else{ // 沒有token
      return null
    }
}
export {tokenCheck};
