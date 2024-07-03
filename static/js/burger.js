function toggleMenu() {
  let popupMenu = document.getElementById("popupMenu");
  popupMenu.classList.toggle("active");
  
  let loginBtn = document.getElementById("login-btn");
  let mobileLoginBtn = document.getElementById("mobile-login-btn");
  let mobileLogoutBtn = document.getElementById("mobile-logout-btn");
  
  if (loginBtn.classList.contains("hidden")) {
    mobileLoginBtn.classList.add("hidden");
    mobileLogoutBtn.classList.remove("hidden");
  } else {
    mobileLoginBtn.classList.remove("hidden");
    mobileLogoutBtn.classList.add("hidden");
  }
}

function closeMenu() {
  let popupMenu = document.getElementById("popupMenu");
  popupMenu.classList.remove("active");
}

