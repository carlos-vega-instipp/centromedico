(() => {
    'use strict';
    // Switches
    const switchCheck = document.querySelector('#switchCheck');
    const estado = document.querySelector('#estado');
    
    // Establecer el estado inicial del texto
    estado.textContent = switchCheck.checked ? 'Activo' : 'Inactivo';

    switchCheck.addEventListener('change', function () {
        if (this.checked) {
            estado.textContent = 'Activo';
        } else {
            estado.textContent = 'Inactivo';
        }
    });

})();