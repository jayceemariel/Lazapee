function on() {
    document.getElementById("overlay").style.display = "block";
  }
  
  function off() {
    document.getElementById("overlay").style.display = "none";
  }
  
let isNavOpen = false;
function openNav() {
    if (!isNavOpen) {
        document.getElementById("mySidebar").style.width = "240px";
        document.getElementById("main").style.marginLeft = "240px";
        // Rotates Icon
        document.querySelectorAll(".menu-icon").forEach(icon => icon.classList.add('open'));
        isNavOpen = true;
        
        document.querySelectorAll(".details-head").forEach(function(el) {
            el.classList.remove("hide");
          });

    } else {
        closeNav();
    }
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "auto";
    document.getElementById("main").style.marginLeft = "61px";

     // Rotates Icon
    document.querySelectorAll(".menu-icon").forEach(icon => icon.classList.remove('open'));
    isNavOpen = false;

    document.querySelectorAll(".details-head").forEach(function(el) {
        el.classList.add("hide");
      });
 
}

function handleNavClick(element) {
    // Remove the "active" class from all elements with class "sidebar-nav-ext"
    document.querySelectorAll('.sidebar-nav-ext').forEach(el => el.classList.remove('active'));

    // Add the "active" class to the clicked element
    element.classList.add('active');

}
