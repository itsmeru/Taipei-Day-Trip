let profile = document.querySelector(".profile");
let pic_current = document.querySelector(".pic-current");
let slider = document.querySelector(".slider");
let infos = document.querySelector(".infos");
let transports = document.querySelector(".transport");
function renderInfo(address,category,description,mrt,name,transport,images){
    let name_mrt = document.createElement("div");
    name_mrt.className = "name-mrt dialog-title font-bold";
    name_mrt.textContent = name;

    let catagory_mrt = document.createElement("div");
    catagory_mrt.className = "catagory-mrt";
    catagory_mrt.textContent = category+" at "+ mrt;
    profile.insertBefore(catagory_mrt, profile.firstChild);
    profile.insertBefore(name_mrt, profile.firstChild);

    for(let i =0;i<images.length;i++){
        let img = document.createElement("img");
        img.setAttribute("src",images[i]);
        slider.appendChild(img);
    }

    let info = document.createElement("div");
    info.className = "content font-regular";
    info.textContent = description;
    infos.insertBefore(info, infos.firstChild);

    let info2 = document.createElement("div");
    info2.className = "content font-regular";
    info2.textContent = address;
    infos.insertBefore(info2,transports)

    let info3 = document.createElement("div");
    info3.className = "content font-regular";
    info3.textContent = transport;
    infos.appendChild(info3);


}