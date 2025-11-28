// Abre / fecha o dropdown
function toggleDropdown(btn) {
    const dropdown = btn.parentElement;
    const content = dropdown.querySelector('.dropdown-content');
    const isOpen = btn.classList.contains('open');

    // Fecha todos os outros dropdowns
    document.querySelectorAll('.dropdown-content').forEach(c => c.style.display = 'none');
    document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));

    // Abre o clicado
    if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
    }
}

// Fecha dropdown ao clicar fora
document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-content').forEach(c => c.style.display = 'none');
    document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
});

// Seleciona item do dropdown
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const selectedText = dropdown.querySelector('.selected-text');
        const input = dropdown.querySelector('input');
        const items = dropdown.querySelectorAll('.dropdown-item');

        items.forEach(item => {
            item.addEventListener('click', () => {
                selectedText.textContent = item.textContent;
                input.value = item.dataset.value;

                dropdown.querySelector('.dropdown-content').style.display = 'none';
                dropdown.querySelector('.dropdown-btn').classList.remove('open');
            });
        });
    });
});
