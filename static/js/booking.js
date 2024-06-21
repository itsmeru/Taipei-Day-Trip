async function booking(form,attraction_id) {
  let date = form.date.value;
  let time = form.querySelector("input[name='halfday']:checked").value;
  let prices = form.querySelector(".money").textContent;
  let token = localStorage.getItem("authToken");
  let takePrice = prices.split(" ")[1]; //新台幣 2000元
  let price = parseInt(takePrice); // 2000
  let user = await tokenCheck();
  if (user === null){alert("請先登入會員"); return;}
  user_id = user.id;
  let bookingData = {
    user_id: user_id,
    attraction_id: attraction_id,
    date: date,
    time: time,
    price: price
  };
  getBookInfo(bookingData,token);
  
  window.location.href = "/booking";

}
