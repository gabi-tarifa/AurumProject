const sons = {
  click: new Audio("/static/sounds/ui/click.wav"),
  hover: new Audio("/static/sounds/ui/hover.ogg"),
  error: new Audio("/static/sounds/ui/error.wav"),
  regular: new Audio("/static/sounds/ui/regular.mp3"),
  rare: new Audio("/static/sounds/ui/rare.mp3"),
  legendary: new Audio("/static/sounds/ui/legendary.mp3"),
  
};

function tocarSom(tipo) {
  if (window.SONS_ATIVOS != true && window.SONS_ATIVOS != 'true') return;
  const som = sons[tipo]; 
  if (som) {
    som.currentTime = 0;
    som.play().catch(() => {}); // Evita erro se o navegador bloquear autoplay
    sessionStorage.setItem("ultimoSom", tipo);
  }
}

// 🔁 Função isolada para aplicar os eventos sonoros
function inicializarSons() {
  document.querySelectorAll("button, a, input[type='submit'], select, option, input[type='checkbox'], div#openMais, div.ranking-header h1, div.etapa.concluida, div.etapa.desbloquada")
    .forEach(el => {
      el.removeEventListener("click", handleClick);
      el.removeEventListener("mouseenter", handleHover);

      el.addEventListener("click", handleClick);
      el.addEventListener("mouseenter", handleHover);
    });
}

function handleClick() {
  tocarSom("click");
}

function handleHover() {
  tocarSom("hover");
}

// ⚙️ Inicializa ao carregar a página, se os sons estiverem ativos
document.addEventListener("DOMContentLoaded", () => {
  if (window.SONS_ATIVOS === true || window.SONS_ATIVOS === 'true') {
    inicializarSons();
  }
});

// 🟢 ativa/desativa dinamicamente + salva no localStorage
function ativarSons() {
  window.SONS_ATIVOS = true;
  localStorage.setItem('sons_ativos', 'true');
  inicializarSons();
}

function desativarSons() {
  window.SONS_ATIVOS = false;
  localStorage.setItem('sons_ativos', 'false');
}

// 🧠 Antes de sair da página, salva o tempo atual
window.addEventListener("beforeunload", () => {
  const nome = sessionStorage.getItem("ultimoSom");
  if (!nome) return;

  const som = sons[nome];
  sessionStorage.setItem("tempoSom", som.currentTime);
});

// 🚀 Ao carregar nova página, retoma se houver algo salvo
window.addEventListener("load", () => {
  const nome = sessionStorage.getItem("ultimoSom");
  const tempo = sessionStorage.getItem("tempoSom");

  if (nome && sons[nome]) {
    const som = sons[nome];
    som.currentTime = parseFloat(tempo || 0);
    som.play().catch(() => {});
  }
});