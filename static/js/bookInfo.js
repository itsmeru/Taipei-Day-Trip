async function getBookInfo(bookingData,token){
    try{
        let res = await fetch("/api/booking",{
          method: "POST",
          headers:{
            "Content-Type":"application/json",
            "Authorization": `${token}`,
          },
          body:JSON.stringify(bookingData)
        })
        let result = await res.json();
        if (res.ok){
          return result.ok;
        }
      }catch (err){
        return err.message;
      }
    
}       

    