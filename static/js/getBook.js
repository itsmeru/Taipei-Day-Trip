async function getBook(){
    let token = localStorage.getItem("authToken");
    if (tokenData){
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
        renderBook(result);
    }

}