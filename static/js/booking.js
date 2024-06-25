async function booking(form,attraction_id) {
  let date = form.date.value;
  let time = form.querySelector("input[name='halfday']:checked").value;
  let prices = form.querySelector(".money").textContent;
  let token = localStorage.getItem("authToken");
  let takePrice = prices.split(" ")[1]; //新台幣 2000元
  let price = parseInt(takePrice); // 2000
  let user = await tokenCheck();
  if (user === null){ openDialog('login-dialog'); return;}
  user_id = user.id;
  let bookingData = {
    user_id: user_id,
    attraction_id: attraction_id,
    date: date,
    time: time,
    price: price
  };
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
      window.location.href = "/booking";
    }
  }catch (err){
    return err.message;
  }

}
