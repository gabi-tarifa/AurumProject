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

      if(conquista.raridade == "rara"){
        tocarSom("rare");
        setTimeout(() => popup.classList.add('fade-out'), 10500);
        setTimeout(() => popup.remove(), 13000);
      } else {
        if (conquista.raridade == "lendaria") {
          tocarSom("legendary");
        } else {
          tocarSom("regular");
        }
        setTimeout(() => popup.classList.add('fade-out'), 4500);
        setTimeout(() => popup.remove(), 5000);
      }
    }, delay);
  }
