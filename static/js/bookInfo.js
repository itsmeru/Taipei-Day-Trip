function getBookInfo(){
    let bookingData = JSON.parse(localStorage.getItem("bookingData"));
    console.log(bookingData);
    token = localStorage.getItem("authToken");
    if (token){
        fetch("/api/user/auth",{
            method: "GET",
            headers: {
                "Content-Type":"application/json",
                "Authorization":`Bearer ${token}`
            }
        }).then((res)=>res.json())
          .then((result)=>console.log(result))
    }
}
getBookInfo();

    