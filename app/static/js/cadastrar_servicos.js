document.addEventListener("DOMContentLoaded", function() {
    const dropdownCategoria = document.querySelector(".categoria-servico .dropdownCategoria");
    const dropdownBtn = dropdownCategoria.querySelector(".dropdownCategoria-btn");
    const dropdownContent = dropdownCategoria.querySelector(".dropdownCategoria-content");
    const dropdownItems = dropdownCategoria.querySelectorAll(".dropdownCategoria-item");
    const selectedText = dropdownBtn.querySelector(".selected-text");
    const hiddenInput = dropdownCategoria.querySelector("input[type='hidden']");

    const camposTransporte = document.getElementById("campos-transporte-pequeno");
    const camposSeguranca = document.getElementById("campos-seguranca");
    const camposLimpeza = document.getElementById("campos-limpeza");

    // Inicialmente esconde todos os campos específicos
    camposTransporte.style.display = "none";
    camposSeguranca.style.display = "none";
    camposLimpeza.style.display = "none";

    // Função para desabilitar/habilitar inputs de um container
    function toggleInputs(container, enable) {
        const inputs = container.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.disabled = !enable;
        });
    }

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

            // Esconde todos os campos específicos e desabilita seus inputs
            camposTransporte.style.display = "none";
            toggleInputs(camposTransporte, false);

            camposSeguranca.style.display = "none";
            toggleInputs(camposSeguranca, false);

            camposLimpeza.style.display = "none";
            toggleInputs(camposLimpeza, false);

            // Mostra e habilita os campos da categoria selecionada
            if (value === "transporte") {
                camposTransporte.style.display = "flex";
                toggleInputs(camposTransporte, true);
            } else if (value === "seguranca") {
                camposSeguranca.style.display = "flex";
                toggleInputs(camposSeguranca, true);
            } else if (value === "limpeza") {
                camposLimpeza.style.display = "flex";
                toggleInputs(camposLimpeza, true);
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
