let down = document.querySelector(".down");
let attractions = document.querySelector(".attractions");
let loadingIndicator = document.getElementById("loading-indicator");
let endOfContent = document.getElementById("end-of-content");
let page = 0;
let next_page;
let loading = false;
let current_address = "";


async function preloadImages(imageUrls) {
  try {
    let promises = imageUrls.map((imageUrl) => {
      return new Promise((resolve, reject) => {
        let img = new Image();
        img.onload = () => resolve(img);
        img.onerror = (error) => reject(error);
        img.src = imageUrl;
      });
    });

    // 等待所有圖片加載完成
    await Promise.all(promises);
    console.log("All preload successful.");
  } catch (error) {
    console.error("Failed to preload images:", error);
  }
}

async function getSpot(address = "") {
  if (loading) return;
  loading = true;
  loadingIndicator.style.display = "block";
  try {
    if (address) {
      page = 0;
      endOfContent.style.display = "none";
    }
    let url = `/api/attractions?page=${page}`;
    if (address) {
      current_address = address;
      url += `&keyword=${current_address}`;
      attractions.innerHTML = "";
    } else if (current_address) {
      url += `&keyword=${current_address}`;
    }
    let res = await fetch(url);
    let data = await res.json();

    next_page = data["nextPage"];
    let imageUrls = data["data"].map(attraction => attraction["images"][0]);
    await preloadImages(imageUrls);

    for (let i = 0; i < data["data"].length; i++) {
      let attraction = data["data"][i];
      let first_img = attraction["images"][0];
      renderSpot(
        attraction["name"],
        attraction["MRT"],
        attraction["category"],
        first_img,
        attraction["id"]
      );
    }
    if (next_page !== null) {
      observer.observe(down);
      page = next_page;
    } else {
      observer.disconnect();
      endOfContent.style.display = "block";
    }
  } catch (err) {
    console.error(err.message);
  } finally {
    loading = false;
    loadingIndicator.style.display = "none";
  }
}

let observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        getSpot();
      }
    });
  },
  {
    root: null,
    threshold: 0.5,
  }
);

document.addEventListener("DOMContentLoaded", async function () {
  await getSpot();
  observer.observe(down);
});
