async function deleteSchedule(user_id,attraction_id){
    let token = localStorage.getItem("authToken");
    let res = await fetch("/api/booking",{
        method: "DELETE",
        headers:{
            "Content-Type":"application/json",
            "Authorization": `${token}`,
        },
        body:JSON.stringify({"user_id":user_id,"attraction_id":attraction_id})
    })
    let result = await res.json();
    window.location.reload();
}