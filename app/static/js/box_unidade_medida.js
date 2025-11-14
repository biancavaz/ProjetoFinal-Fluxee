document.addEventListener("DOMContentLoaded", function() {
  const dropdowns = document.querySelectorAll(".dropdown");

  dropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector(".dropdown-btn");
    const content = dropdown.querySelector(".dropdown-content");
    const items = dropdown.querySelectorAll(".dropdown-item");
    const selectedText = dropdown.querySelector(".selected-text");
    const hiddenInput = dropdown.querySelector("input[type='hidden']");

    btn.addEventListener("click", function(e) {
      e.stopPropagation();

      // Fecha todas as outras dropdowns
      dropdowns.forEach(d => {
        if (d !== dropdown) {
          d.querySelector(".dropdown-content").classList.remove("show");
          d.querySelector(".dropdown-btn").classList.remove("open");
        }
      });

      // Alterna a própria dropdown
      btn.classList.toggle("open");
      // Mostra conteúdo **quando a dropdown estiver aberta**
      if (btn.classList.contains("open")) {
        content.classList.add("show");
      } else {
        content.classList.remove("show");
      }
    });

    // Seleção de item
    items.forEach(item => {
      item.addEventListener("click", function(e) {
        e.stopPropagation();
        selectedText.textContent = this.textContent;
        if (hiddenInput) hiddenInput.value = this.dataset.value;

        content.classList.remove("show");
        btn.classList.remove("open");
      });
    });
  });

  // Clique fora fecha todas dropdowns
  document.addEventListener("click", function() {
    dropdowns.forEach(dropdown => {
      const content = dropdown.querySelector(".dropdown-content");
      const btn = dropdown.querySelector(".dropdown-btn");
      content.classList.remove("show");
      btn.classList.remove("open");
    });
  });
});
