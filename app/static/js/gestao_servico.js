const modal = document.getElementById('modal-solicitar');
const btnSolicitar = document.querySelectorAll('.btn-solicitar');
const fecharModal = document.querySelector('.fechar');

// Abre o modal e mostra a categoria correta
btnSolicitar.forEach(btn => {
    btn.addEventListener('click', () => {
        const categoria = btn.getAttribute('data-categoria').toLowerCase();

        // Esconde todas as categorias
        document.querySelectorAll('.categoria').forEach(box => {
            box.style.display = 'none';
        });

        // Mostra apenas a categoria clicada
        const box = document.querySelector(`.categoria.${categoria}`);
        if (box) box.style.display = 'block';

        // Mostra o modal
        modal.style.display = 'block';
    });
});

// Fecha modal clicando no X
fecharModal.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Fecha modal clicando fora da área do conteúdo
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});



