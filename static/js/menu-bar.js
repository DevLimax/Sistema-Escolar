document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    
    menuToggle.addEventListener("click", function(event) {
        sidebar.classList.toggle("active");
        
        // Alternar o ícone do botão hambúrguer
        if (sidebar.classList.contains("active")) {
            menuToggle.innerHTML = "&times;"; // Ícone de fechar
        } else {
            menuToggle.innerHTML = "&#9776;"; // Ícone de hambúrguer
        }
    });
    
    // Fechar a navbar ao clicar fora dela
    document.addEventListener("click", function(event) {
        if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
            sidebar.classList.remove("active");
            menuToggle.innerHTML = "&#9776;";
        }
    });
});
