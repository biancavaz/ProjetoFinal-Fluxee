// ===========================
// Função para abrir/fechar dropdown
// ===========================
function toggleDropdown(btn) {
    const dropdown = btn.closest('.dropdown');
    if (!dropdown) return;

    const content = dropdown.querySelector('.dropdown-content');
    if (!content) return;

    const isOpen = btn.classList.contains('open');

    // Fecha todos os outros dropdowns
    document.querySelectorAll('.dropdown-content').forEach(c => {
        if(c) c.style.display = 'none';
    });
    document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));

    // Abre o clicado
    if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
    }
}

// ===========================
// Fecha dropdown ao clicar fora
// ===========================
document.addEventListener('click', (event) => {
    // Se o clique foi dentro de um dropdown, não fecha
    if (event.target.closest('.dropdown')) return;

    document.querySelectorAll('.dropdown-content').forEach(c => {
        if(c) c.style.display = 'none';
    });
    document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
});

// ===========================
// Seleciona item do dropdown
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const selectedText = dropdown.querySelector('.selected-text');
        const input = dropdown.querySelector('input');
        const items = dropdown.querySelectorAll('.dropdown-item');
        const btn = dropdown.querySelector('.dropdown-btn');

        if(!selectedText || !input || !btn) return;

        items.forEach(item => {
            item.addEventListener('click', () => {
                selectedText.textContent = item.textContent;
                input.value = item.dataset.value;

                const content = dropdown.querySelector('.dropdown-content');
                if(content) content.style.display = 'none';
                btn.classList.remove('open');
            });
        });
    });
});
