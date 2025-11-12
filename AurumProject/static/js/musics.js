// 🎵 Controle global de música de fundo
let musicaFundo;

// Caminho da música atual vinda do backend 
const musicaSession = musicadasessao;

musicaFundo = new Audio(musicaSession)

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
  // Só toca se música estiver habilitada
  if (!window.MUSICA_ATIVA) return;

  // Se já houver música tocando, troca para a nova
  if (musicaFundo) {
    musicaFundo.pause();
  }

  // Cria o player de áudio
  musicaFundo = new Audio(caminho);
  musicaFundo.loop = true;
  musicaFundo.volume = volumeMusicaBanco/100;

  // retoma o tempo salvo
  const tempoSalvo = parseFloat(localStorage.getItem("tempo_musica"));
  if (isNaN(tempoSalvo)){
    musicaFundo.currentTime = 0;
  } else{
    musicaFundo.currentTime = tempoSalvo;
  }

  musicaFundo.play().catch(() => {});
}

// Função para pausar a música
function pausarMusicaFundo() {
  if (musicaFundo && !musicaFundo.paused) {
    musicaFundo.pause();
  }
}

// 🔹 Salva o tempo atual ao sair da página
window.addEventListener("beforeunload", () => {
      localStorage.setItem("tempo_musica", musicaFundo.currentTime);
});

window.addEventListener("timeupdate", () => {
      localStorage.setItem("tempo_musica", musicaFundo.currentTime);

});

// 🔹 Retoma a música quando a página carrega
window.addEventListener("load", () => {
  iniciarMusicaFundo(musicaSession);
});

// 🔹 Permite alternar dinamicamente (ligar/desligar som)
function alternarMusica(ativar) {
  window.MUSICA_ATIVA = ativar;
  if (ativar) {
    retomarMusica();
  } else {
    pausarMusicaFundo();
  }
}

function retomarMusica(){
  musicaFundo.play().catch(() => {});
}

const rangeVolume = document.getElementById("range_musica");

// Define volume inicial baseado no banco (valor já embutido via Jinja)
rangeVolume.value = volumeMusicaBanco; 

// Atualiza o volume ao mover o range
rangeVolume.addEventListener("input", () => {
  if (musicaFundo) {
    musicaFundo.volume = rangeVolume.value / 100;
  }
});