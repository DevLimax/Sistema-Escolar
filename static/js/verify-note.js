document.addEventListener('DOMContentLoaded', function() {
    const nota = document.querySelectorAll('.nota');
    const notaBimestral = document.querySelectorAll('.notaBimestral');
    const notaConceito = document.querySelectorAll('.notaConceito');
    const notaFinal = document.querySelectorAll('.notaFinal');
    const message = document.querySelector('.message-not-notes');

    nota.forEach(nota => {
        if (parseFloat(nota.textContent) < 6) {
            nota.style.color = 'red';
        } else {
            nota.style.color = 'green';
        }
    });

    message.style.color = 'yellow'
});