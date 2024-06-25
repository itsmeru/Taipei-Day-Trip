async function getBook(tokenData){
    let token = localStorage.getItem("authToken");
    if (token){
        let res = await fetch("/api/booking", {
              method: "GET",
              headers: {
                "Authorization": `${token}`,
                "Content-Type": "application/json"
              }
            })
        let result = await res.json();
        if (!res.ok){
            result = null
        }
        renderBook(result,tokenData);
    }

}