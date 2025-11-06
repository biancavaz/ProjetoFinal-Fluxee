
  function toggleDropdown(element) {
    const dropdown = element.parentElement;
    dropdown.classList.toggle("open");
    const content = dropdown.querySelector(".dropdown-content");
    content.style.display = dropdown.classList.contains("open") ? "block" : "none";
  }

  document.addEventListener("click", function(event) {
    document.querySelectorAll(".dropdown").forEach(dropdown => {
      if (!dropdown.contains(event.target)) {
        dropdown.classList.remove("open");
        dropdown.querySelector(".dropdown-content").style.display = "none";
      }
    });
  });

  document.querySelectorAll(".dropdown-item").forEach(item => {
    item.addEventListener("click", function() {
      const dropdown = this.closest(".dropdown");
      const selectedText = dropdown.querySelector(".selected-text");
      const hiddenInput = dropdown.querySelector("input[type='hidden']");
      selectedText.textContent = this.textContent;
      hiddenInput.value = this.dataset.value;
      dropdown.classList.remove("open");
      dropdown.querySelector(".dropdown-content").style.display = "none";
    });
  });
