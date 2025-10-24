// 🎵 Controle global de música de fundo
let musicaFundo;

musicaSession = localStorage.getItem("musicaSelecionada");

// Caminhos das músicas do sistema
const musicas = {
  blind: "/static/sounds/music/blind.mp3",
  fest: "/static/sounds/music/fest.mp3",
  taswell: "/static/sounds/music/taswell.mp3",
  city: "/static/sounds/music/city.mp3",
  haggstrom: "/static/sounds/music/haggstrom.mp3",
  muskie: "/static/sounds/music/muskie.mp3",
  mutation: "/static/sounds/music/mutation.mp3",
  mice: "/static/sounds/music/mice.mp3"
};

// Função principal para iniciar ou retomar a música
function iniciarMusicaFundo(caminho) {
  // só ativa se música estiver permitida
  if (!window.MUSICA_ATIVA) return;


  if (!caminho || caminho === "adicionar") return;
  // cria se ainda não existir
  if (!musicaFundo) {
    musicaFundo = new Audio(caminho);
    musicaFundo.loop = true;
    musicaFundo.volume = 0.3;

    // retoma o tempo salvo
    const tempoSalvo = sessionStorage.getItem("tempoMusica");
    if (tempoSalvo) musicaFundo.currentTime = parseFloat(tempoSalvo);
  }

  musicaFundo.play().catch(() => {});
}

// Função para pausar a música
function pausarMusicaFundo() {
  if (musicaFundo && !musicaFundo.paused) {
    musicaFundo.pause();
  }
}

// Salva tempo atual antes de sair da página
window.addEventListener("beforeunload", () => {
  if (musicaFundo) {
    sessionStorage.setItem("tempoMusica", musicaFundo.currentTime);
  }
});

// Retoma quando entra
window.addEventListener("load", () => {
  iniciarMusicaFundo(musicaSession);
});

// Permite alternar dinamicamente
function alternarMusica(ativar) {
  window.MUSICA_ATIVA = ativar;
  if (ativar) {
    iniciarMusicaFundo(musicaSession);
  } else {
    pausarMusicaFundo();
  }
}