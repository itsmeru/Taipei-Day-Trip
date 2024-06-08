let list_container = document.querySelector(".list-container");
function showMrt(address){
    let search_input = document.querySelector(".search-input");
    let div = document.createElement("div");
    div.classList.add("mrt-name");
    let button = document.createElement("button");
    button.textContent = address;
    button.classList.add("list-item","body", "font-medium");
    button.onclick = function(){getSpot(address);search_input.value = address;}
    div.appendChild(button);
    list_container.appendChild(div);
  }


    
    let leftButton = document.querySelector(".left-container button");
    let rightButton = document.querySelector(".right-container button");

    leftButton.addEventListener("click", function() {
      list_container.scrollBy({ left: -400, behavior: "smooth" });
    });

    rightButton.addEventListener("click", function() {
      list_container.scrollBy({ left: 400, behavior: "smooth" });
    });