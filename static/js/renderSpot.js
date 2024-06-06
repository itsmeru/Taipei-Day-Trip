function showSpot(name,mrt_station,catego,first_img,id){
    let attractions = document.querySelector(".attractions");
    let attractions_group = document.createElement("div");
    attractions_group.classList.add("attractions-group");
    attractions_group.onclick = function(){spotPage(id);};

    let container_img = document.createElement("div");
    container_img.classList.add("container-img");
    let attractions_img = document.createElement("img");
    attractions_img.setAttribute("src", first_img);
    attractions_img.classList.add("attractions-img");

    let attractions_text = document.createElement("div");
    attractions_text.textContent = name;
    attractions_text.classList.add("attractions-text","body","font-bold");

    let attractions_info =document.createElement("div");
    attractions_info.classList.add("attractions-info");

    let mrt =document.createElement("div");
    mrt.textContent = mrt_station;
    mrt.classList.add("body","font-medium");

    let category =document.createElement("div");
    category.textContent = catego;
    category.classList.add("body","font-medium");

    container_img.appendChild(attractions_img);
    container_img.appendChild(attractions_text);
    attractions_info.appendChild(mrt);
    attractions_info.appendChild(category);
    attractions_group.appendChild(container_img);
    attractions_group.appendChild(attractions_info);
    attractions.appendChild(attractions_group);
  }
