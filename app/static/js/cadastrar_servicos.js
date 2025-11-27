document.addEventListener("DOMContentLoaded", function() {
    const dropdownCategoria = document.querySelector(".categoria-servico .dropdownCategoria");
    const dropdownBtn = dropdownCategoria.querySelector(".dropdownCategoria-btn");
    const dropdownContent = dropdownCategoria.querySelector(".dropdownCategoria-content");
    const dropdownItems = dropdownCategoria.querySelectorAll(".dropdownCategoria-item");
    const selectedText = dropdownBtn.querySelector(".selected-text");
    const hiddenInput = dropdownCategoria.querySelector("input[type='hidden']");

    // Seleciona os campos específicos
    const linhaTransporte = document.querySelector(".linha-transporte");
    const linhaLimpeza = document.querySelector(".linha-limpeza");
    const linhaSeguranca = document.querySelector(".linha-seguranca");

    // Abre/fecha dropdown
    dropdownBtn.addEventListener("click", function(e) {
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    });

    // Seleção do item
    dropdownItems.forEach(function(item) {
        item.addEventListener("click", function() {
            const value = this.dataset.value;
            selectedText.textContent = this.textContent;
            hiddenInput.value = value; // atualiza input hidden
            dropdownContent.style.display = "none";

            // Esconde todos os campos
            linhaTransporte.style.display = "none";
            linhaLimpeza.style.display = "none";
            linhaSeguranca.style.display = "none";

            // Mostra a linha correta
            if(value === "transporte") linhaTransporte.style.display = "flex";
            if(value === "limpeza") linhaLimpeza.style.display = "flex";
            if(value === "seguranca") linhaSeguranca.style.display = "flex";
        });
    });

    // Fecha dropdown ao clicar fora
    document.addEventListener("click", function(e) {
        if(!dropdownCategoria.contains(e.target)) {
            dropdownContent.style.display = "none";
        }
    });
});
