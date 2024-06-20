let currentSlide = 0;

function showSlide(index) {
  let slides = document.querySelectorAll(".slider img");
  let dots = document.querySelectorAll(".dots-container .dot");

  if (index >= slides.length) {
    currentSlide = 0;

  } else if (index < 0) {
    currentSlide = slides.length - 1;

  } else {
    currentSlide = index;

  }
  let offset = -currentSlide * 100;
  document.querySelector(".slider").style.transform = `translateX(${offset}%)`;

  document.querySelector(".dot.active").classList.remove("active");
  dots[currentSlide].classList.add("active");
}

function nextSlide() {
  showSlide(currentSlide + 1);
}

function prevSlide() {
  showSlide(currentSlide - 1);
}
