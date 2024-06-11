let down = document.querySelector(".down");
let attractions = document.querySelector(".attractions");
let page = 0;
let next_page;
let loading = false;
let current_address = "";
async function getSpot(address="") {
    if (loading) return;
    loading = true;
    try {
    if(address){page = 0;}
    let url = `/api/attractions?page=${page}`;
    if(address){
        current_address = address;
        url+=`&keyword=${current_address}`
        attractions.innerHTML = "";
    }else if (current_address){
        url+=`&keyword=${current_address}`
    }
    let res = await fetch(url);
    let data = await res.json();
    
    next_page = data["nextPage"];
    for (let i = 0; i < data["data"].length; i++) {
        let attraction = data["data"][i];
        let first_img = attraction["images"][0];
        showSpot(attraction["name"], attraction["MRT"], attraction["category"],first_img,attraction["id"]);
    }
    if (next_page !== null) {
        observer.observe(document.querySelector(".down")); 
        page = next_page;
    } else {
        observer.disconnect();
    }
    } catch (err) {
    console.error(err.message);
    } finally {
    loading = false;
    }
} 
    let observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
        getSpot();
        }
    });
    }, {
    root: null,
    threshold: 0.5
    });

document.addEventListener("DOMContentLoaded", function() {
    getSpot(); 
observer.observe(document.querySelector(".down")); 
});