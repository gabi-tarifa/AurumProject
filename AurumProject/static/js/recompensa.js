function abrirModalRanking(info) {
    const overlay = document.createElement("div");
    overlay.classList.add("modal-ranking-overlay");

    overlay.innerHTML = `
      <div class="modal-ranking">
        <h2>🏁 Ranking Encerrado</h2>

        <p><b>Posição:</b> #${info.posicao}</p>
        <p><b>Recompensa:</b> ${info.recompensa} moedas</p>
        <p><b>Total de vitórias:</b> ${info.vitorias}</p>
        <p><b>Sequência atual:</b> ${info.streak}</p>

        <button id="receber-btn">Receber recompensa</button>
      </div>
    `;
    if (tema_atual === "cla"){
      modal = document.getElementById("modal-ranking");
      modal.classList.add("claro")
    }
    document.body.appendChild(overlay);

    document.getElementById("receber-btn").onclick = () => {
        overlay.remove();
        fetch("/limpar_popup_ranking");
    };
}