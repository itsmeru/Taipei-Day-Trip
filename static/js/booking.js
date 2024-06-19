async function booking(form,id) {
  let date = form.date.value;
  let halfday = form.querySelector("input[name='halfday']:checked").value;
  let cost = form.querySelector(".money").textContent;
  let token = localStorage.getItem("authToken");
  let bookingData = {
    id : id,
    date: date,
    halfday: halfday,
    cost: cost
  };

  localStorage.setItem("bookingData", JSON.stringify(bookingData));

  window.location.href = "/booking";

}
