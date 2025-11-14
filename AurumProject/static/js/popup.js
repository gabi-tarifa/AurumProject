function exibirConquistaPopup(conquista, delay = 0) {
  setTimeout(() => {
    const popup = document.createElement('div');
    popup.classList.add('popup-conquista', `cor-${conquista.cor}`);
    popup.innerHTML = `
      <img src="/static/${conquista.imagem}" alt="Ícone da conquista">
      <div class="popup-texto">
        <strong>🏆 ${conquista.anuncio}</strong><br>
        <span><b>${conquista.nome}</b></span><br>
        <small>${conquista.descricao}</small>
      </div>
    `;
    document.body.appendChild(popup);

    let fadeTime, removeTime;

    if (conquista.raridade === "rara") {
      tocarSom("rare");
      fadeTime = 10500;
      removeTime = 13000;
    } else {
      tocarSom(conquista.raridade === "lendaria" ? "legendary" : "regular");
      fadeTime = 4500;
      removeTime = 5000;
    }

    setTimeout(() => popup.classList.add('fade-out'), fadeTime);

    // 🟡 Quando remover o popup → limpamos só essa conquista
    setTimeout(() => {
      popup.remove();
    }, removeTime);

    setTimeout(() => {
      fetch(`/limpar_popup_conquista_individual/${conquista.id_conquista}`);
    }, 1200);

  }, delay);
}