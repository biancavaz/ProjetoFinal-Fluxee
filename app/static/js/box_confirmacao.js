document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal-excluir');
    const mensagem = document.getElementById('mensagem-excluir');
    const btnCancelar = document.getElementById('btn-cancelar');
    const btnConfirmar = document.getElementById('btn-confirmar');

    let linkParaDeletar = null;

    // Seleciona todos os botões delete
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function() {
            const nomeProduto = this.dataset.nome;
            linkParaDeletar = this.dataset.link;
            mensagem.textContent = "Tem certeza que deseja excluir o produto '" + nomeProduto + "'?";
            modal.style.display = 'flex';
        });
    });

    btnCancelar.onclick = function() {
        modal.style.display = 'none';
        linkParaDeletar = null;
    }

    btnConfirmar.onclick = function() {
        if (linkParaDeletar) {
            window.location.href = linkParaDeletar;
        }
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            linkParaDeletar = null;
        }
    }
});
