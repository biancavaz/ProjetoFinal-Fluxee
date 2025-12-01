document.addEventListener("DOMContentLoaded", function() {
    const dropdownCategoria = document.querySelector(".categoria-servico .dropdownCategoria");
    const dropdownBtn = dropdownCategoria.querySelector(".dropdownCategoria-btn");
    const dropdownContent = dropdownCategoria.querySelector(".dropdownCategoria-content");
    const dropdownItems = dropdownCategoria.querySelectorAll(".dropdownCategoria-item");
    const selectedText = dropdownBtn.querySelector(".selected-text");
    const hiddenInput = dropdownCategoria.querySelector("input[type='hidden']");

    const camposTransporte = document.getElementById("campos-transporte-pequeno");

    // Inicialmente esconde os campos
    camposTransporte.style.display = "none";

    // Abre/fecha dropdown
    dropdownBtn.addEventListener("click", function(e) {
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    });

    // Seleção do item
    dropdownItems.forEach(function(item) {
        item.addEventListener("click", function() {
            const value = this.dataset.value;
            selectedText.textContent = this.textContent;
            hiddenInput.value = value;
            dropdownContent.style.display = "none";

            // Esconde todos os campos específicos
            camposTransporte.style.display = "none";
            // Desabilita os inputs quando não é transporte
            camposTransporte.querySelector('input[name="tipo_veiculo"]').disabled = true;
            camposTransporte.querySelector('input[name="quantidade_passageiros"]').disabled = true;
            camposTransporte.querySelector('input[name="preco_diaria"]').disabled = true;

            // Mostra Transporte se selecionado
            if(value === "transporte") {
                camposTransporte.style.display = "flex";
                // Habilita os inputs quando é transporte
                camposTransporte.querySelector('input[name="tipo_veiculo"]').disabled = false;
                camposTransporte.querySelector('input[name="quantidade_passageiros"]').disabled = false;
                camposTransporte.querySelector('input[name="preco_diaria"]').disabled = false;
            }
        });
    });

    // Fecha dropdown ao clicar fora
    document.addEventListener("click", function(e) {
        if(!dropdownCategoria.contains(e.target)) {
            dropdownContent.style.display = "none";
        }
    });
});
