// dashboard.js - Enhancements for Dashboard Page

document.addEventListener('DOMContentLoaded', function() {
    console.log("Dashboard loaded successfully!");
    
    const buttons = document.querySelectorAll('.button');
    
    buttons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.transform = "scale(1.05)";
        });
        button.addEventListener('mouseout', function() {
            this.style.transform = "scale(1)";
        });
    });

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
        });
    }
});
