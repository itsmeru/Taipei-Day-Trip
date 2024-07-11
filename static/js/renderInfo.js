let profile = document.querySelector(".profile");
let pic_current = document.querySelector(".pic-current");
let slider = document.querySelector(".slider");
let infos = document.querySelector(".infos");
let transports = document.querySelector(".transport");
let dots_container = document.querySelector(".dots-container");

// async function preloadImages(imageUrls) {
//   try {
//     let promises = imageUrls.map((imageUrl) => {
//       return new Promise((resolve, reject) => {
//         let img = new Image();
//         img.src = imageUrl;
//         img.onload = () => resolve(img);
//         img.onerror = (error) => reject(error);
//       });
//     });

//     // 等待所有圖片加載完成
//     await Promise.all(promises);
//     console.log("All images preloaded successfully.");
//   } catch (error) {
//     console.error("Failed to preload images:", error);
//   }
// }

async function renderInfo(id) {
  let data = await spotPage(id);
  let address = data["address"];  
  let category = data["category"];
  let description = data["description"];
  let mrt = data["MRT"];
  let name = data["name"];
  let transport = data["transpot"];
  let images =  data["images"];

  // preloadImages(images);

  let name_mrt = document.createElement("div");
  name_mrt.className = "name-mrt dialog-title font-bold";
  name_mrt.textContent = name;

  let catagory_mrt = document.createElement("div");
  catagory_mrt.className = "catagory-mrt";
  catagory_mrt.textContent = category + " at " + mrt;
  profile.insertBefore(catagory_mrt, profile.firstChild);
  profile.insertBefore(name_mrt, profile.firstChild);

  for (let i = 0; i < images.length; i++) {
    let img = new Image();
    img.src = images[i];
    slider.appendChild(img);
    let circle = document.createElement("span");
    circle.className = "circle";
    let dot = document.createElement("span");
    dot.className = "dot";
    if (i === 0) {
      dot.classList.add("active");
    }
    dot.onclick = () => showSlide(i);
    circle.appendChild(dot);
    dots_container.appendChild(circle);
    dots_container.style.width = `${images.length * 24}px`;
  }

  let info = document.createElement("div");
  info.className = "content font-regular";
  info.textContent = description;
  infos.insertBefore(info, infos.firstChild);

  let info2 = document.createElement("div");
  info2.className = "content font-regular";
  info2.textContent = address;
  infos.insertBefore(info2, transports);

  let info3 = document.createElement("div");
  info3.className = "content font-regular";
  info3.textContent = transport;
  infos.appendChild(info3);
}

document.addEventListener("DOMContentLoaded", () => {
  let morning_radio = document.getElementById("morning");
  let afternoon_radio = document.getElementById("afternoon");
  let tour_cost = document.getElementById("tour-cost");

  let updateCost = () => {
    if (morning_radio.checked) {
      tour_cost.textContent = "新台幣 2000元";
    } else if (afternoon_radio.checked) {
      tour_cost.textContent = "新台幣 2500元";
    }
  };

  morning_radio.addEventListener("change", updateCost);
  afternoon_radio.addEventListener("change", updateCost);

  updateCost();
});
