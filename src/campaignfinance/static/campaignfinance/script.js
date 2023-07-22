var menuToggle = document.getElementById("menu-toggle");
var menuTable = document.getElementById("menu-table");

function toggleMenu() {
    if (menuTable.style.display === "none") {
        menuTable.style.display = "block";
        menuToggle.textContent = "Hide Menu";
    } else {
        menuTable.style.display = "none";
        menuToggle.textContent = "Show Menu";
    }
}

function hideMenuTable() {
    if ( window.innerWidth > 768) {
        menuTable.style.display = "none";
        menuToggle.textContent = "Show Menu";
    }
}

toggleMenu();

menuToggle.addEventListener("click", toggleMenu);
window.addEventListener("resize", hideMenuTable);

function submitForm(form) {
    form.submit();
}

document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category-select');
    const sortbySelect = document.getElementById('sortby-select');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            submitForm(this.form);
        });
    }

    if (sortbySelect) {
        sortbySelect.addEventListener('change', function() {
            submitForm(this.form);
        });
    }
});