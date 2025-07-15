document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.header__menu-toggle');
    const offcanvasElement = document.getElementById('offcanvasNavbar');

    if (menuToggle && offcanvasElement) { // Проверка на null!
        const bsOffcanvas = new bootstrap.Offcanvas(offcanvasElement);

        menuToggle.addEventListener('click', function() {
            if (offcanvasElement.classList.contains('show')) {
                bsOffcanvas.hide();
                menuToggle.setAttribute('aria-expanded', 'false');
            } else {
                bsOffcanvas.show();
                menuToggle.setAttribute('aria-expanded', 'true');
            }
        });
    } else {
        console.error('Не найден элемент с классом .header__menu-toggle или id #offcanvasNavbar');
    }

});