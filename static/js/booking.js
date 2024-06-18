function booking(form) {
  let date = form.date.value;
  let halfday = form.querySelector("input[name='halfday']:checked").value;
  let cost = form.querySelector(".money").textContent;

  console.log("Date:", date);
  console.log("Half Day:", halfday);
  console.log("Cost:", cost);
  window.location.href = "/booking";

}
