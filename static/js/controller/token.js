async function tokenCheck(){
    let token = localStorage.getItem("authToken");
    let googleToken = localStorage.getItem("googleAuth");
    if (googleToken){
      let res = await fetch("/auth/google",{
          method:"POST",
          headers:{
            "Content-Type":"application/json"
          },
          body:JSON.stringify({"id_token":googleToken})
        });
        let result = await res.json();
        if (!res.ok){ 
          alert(result.error);
          localStorage.removeItem("googleAuth");
          window.location.reload();
          return null
        }
        if (result.data !== null) {
          let gtoken = result.token
          
          localStorage.setItem("authToken",`bearer ${gtoken}`)
          return result.data
        }else{ 
          return null
        }
    }
    else if (token) {
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
