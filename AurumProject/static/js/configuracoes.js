function abrirDiv(id) {
    document.getElementById(id).classList.remove("oculto");
}

function fecharDiv(id) {
    document.getElementById(id).classList.add("oculto");
}

document.getElementById("musica").addEventListener("change", function () {
  if (this.value === "adicionar") {
    document.getElementById("painel-musica").classList.remove("oculto");
    this.value = ""; // reseta o select
  }
});


function salvarApelido() {
    const apelido = document.getElementById("novo-apelido").value;
    fetch("/api/config/apelido", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ apelido })
    })
    .then(r => r.json())
    .then(() => fecharDiv("painel-apelido"));
}

function salvarEmail() {
    const email = document.getElementById("novo-email").value;
    fetch("/api/config/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
    })
    .then(r => r.json())
    .then(() => fecharDiv("painel-email"));
}

function temMaiuscula(str) {
    return /[A-Z]/.test(str);
}

function temMinuscula(str) {
    return /[a-z]/.test(str);
}

function temNumero(str) {
    return /\d/.test(str);
}

function temCaractereEspecial(str) {
    return /[!@#$%^&*(),.?":{}|<>]/.test(str);
}


function salvarSenha() {
    const atual = document.getElementById("senha-atual").value;
    const nova = document.getElementById("nova-senha").value;
    const confirmar = document.getElementById("confirmar-senha").value;
    const texto = document.getElementById("textoerro");

    if(nova.length < 6 || nova.length > 16 || !temMaiuscula(nova) || !temMinuscula(nova) || !temNumero(nova) || !temCaractereEspecial(nova)) {
        texto.innerHTML = "Um dos seguintes requisitos não foi cumprido: <br>- A senha tem que ser maior que 6 dígitos e menor que 16 dígitos;<br>- A senha deve conter pelo menos uma letra maiúscula;<br>- A senha deve conter pelo menos uma letra minúscula;<br>- A senha deve conter pelo menos um número;<br>- A senha deve conter pelo menos um caractere especial.";
        return;
        }
        
        if(confirmar != nova){
            texto.textContent = "As senhas não condizem!";
            return;
        }

    fetch("/api/config/senha", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ atual, nova })
    })
    .then(async (r) => {
        const data = await r.json();

        if (!r.ok) {
            // erro vindo do backend (ex: senha atual incorreta)
            texto.textContent = data.message;
            return;
        } else {
          texto.textContent = "";

          
          document.getElementById("senha-atual").value = "";
          document.getElementById("nova-senha").value = "";
          document.getElementById("confirmar-senha").value = "";

          fecharDiv("painel-senha");
        }
      });
}

function resetarConfig() {

    fetch("/api/config/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })
    .then(r => r.json())
    .then(data => {
        // atualiza checkboxes
        document.getElementById("sound").checked = data.sons;
        document.getElementById("music").checked = data.musica;

    })
    .catch(err => console.error(err));
}


const sel = document.getElementById('idioma');
const apiUrl = sel.dataset.url; // agora deve ter o valor correto

sel.addEventListener('change', async (e) => {
  e.preventDefault(); // se estiver dentro de um form
  const idioma = e.target.value;

  try {
    const r = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idioma })
    });

    if (r.ok) {
  console.log("Idioma alterado:", idioma);
  window.location.reload(); // força recarregar com o novo idioma
}
  } catch (err) {
    console.error(err);
  }
});


const tem = document.getElementById('tema');
const apiUrltem = tem.dataset.url; // agora deve ter o valor correto

tem.addEventListener('change', async (e) => {
  e.preventDefault(); // se estiver dentro de um form
  const tema = e.target.value;

  try {
    const r = await fetch(apiUrltem, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tema })
    });

    if (r.ok) {
  console.log("tema alterado:", tema);
  window.location.reload(); // força recarregar com o novo idioma
}
  } catch (err) {
    console.error(err);
  }
});

async function carregarConfig() {
    const r = await fetch("/api/config");
    if (!r.ok) {
        console.error("Erro ao buscar config");
        return;
    }
    const data = await r.json();

    document.getElementById("sound").checked = data.sons;
    document.getElementById("music").checked = data.musica;
}
carregarConfig();

document.addEventListener("DOMContentLoaded", () => {
    const sons = document.getElementById("sound");
    const musica = document.getElementById("music");
    const idioma = document.getElementById("idioma");

    function salvarConfig() {
        fetch("/api/config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sons: sons.checked,
                musica: musica.checked,
                idioma: idioma.value
            })
        });
    }

    sons.addEventListener("change", salvarConfig);musica.addEventListener("change", (e) => {
    salvarConfig();
    alternarMusica(e.target.checked); // ativa/desativa instantaneamente
});
    idioma.addEventListener("change", salvarConfig);
    document.getElementById("sound").addEventListener("change", (e) => {
    if (e.target.checked) {
        ativarSons();
    } else {
        desativarSons();
    }
    })
});

document.addEventListener("DOMContentLoaded", () => {
  const lista = document.getElementById("musica");
  const btnExcluir = document.getElementById("btn-excluir-musica");

  // 1️⃣ Adiciona as músicas do sistema (que já estão no JS)
  for (const [nome, caminho] of Object.entries(musicas)) {
    const opt = document.createElement("option");
    opt.value = caminho;
    opt.textContent = nome.charAt(0).toUpperCase() + nome.slice(1);
    opt.dataset.tipo = "sistema";
    lista.appendChild(opt);
  }

  // 2️⃣ Adiciona as músicas do usuário (vindas via Jinja)
  if (Array.isArray(musicasUsuario)) {
    for (const musica of musicasUsuario) {
      const opt = document.createElement("option");
      opt.value = musica.caminho;
      opt.textContent = `${musica.nome}`;
      opt.dataset.tipo = "usuario";
      lista.appendChild(opt);
    }
  }

  const add = document.createElement("option");
  add.value = "adicionar";
  add.textContent = '+ Adicionar nova música:';
  lista.appendChild(add);

  const ultimaMusica = musicaSession;
  if (ultimaMusica) {
    lista.value = ultimaMusica;
    iniciarMusicaFundo(ultimaMusica);
  }

  function atualizarVisibilidadeBotao() {
    const selectedOption = lista.options[lista.selectedIndex];
    if (selectedOption && selectedOption.dataset.tipo === "usuario") {
      btnExcluir.style.display = "inline-block";
    } else {
      btnExcluir.style.display = "none";
    }
  }


  // Quando o usuário trocar a música no select
  lista.addEventListener("change", (e) => {
    const caminho = e.target.value;

    // 🔹 Se o usuário escolheu "Adicionar nova música"
    if (caminho != "adicionar" && caminho != "") {  // 🔹 Atualiza a música no banco de dados (sem reload)
      fetch("/atualizar_musica_tocada", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ musica: caminho }),
      })
      .then(res => res.json())
      .then(data => {
        if (data.sucesso) {
          console.log("Música salva no banco:", caminho);
        } else {
          console.error("Erro ao salvar música:", data.erro);
        }
      })
      .catch(err => console.log("Erro ao enviar requisição:", err));

        iniciarMusicaFundo(caminho);
      }
    atualizarVisibilidadeBotao();
  });

  // 🔹 Clique no botão de exclusão
  btnExcluir.addEventListener("click", () => {
  const selectedOption = lista.options[lista.selectedIndex];
  if (!selectedOption || selectedOption.dataset.tipo !== "usuario") return;

  const nomeMusica = selectedOption.textContent;

  // Exibe o modal personalizado
  const modal = document.getElementById("modal-excluir");
  const modalTexto = document.getElementById("modal-texto");
  const btnConfirmar = document.getElementById("btn-confirmar-exclusao");
  const btnCancelar = document.getElementById("btn-cancelar-exclusao");

  modalTexto.textContent = `Deseja realmente excluir "${nomeMusica}"?`;
  modal.style.display = "flex";

  // Evita duplicar listeners
  const limparEventos = () => {
    btnConfirmar.replaceWith(btnConfirmar.cloneNode(true));
    btnCancelar.replaceWith(btnCancelar.cloneNode(true));
  };

  limparEventos();

  // Confirma exclusão
  document.getElementById("btn-confirmar-exclusao").addEventListener("click", () => {
    fetch(`/deletar_musica`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ caminho: selectedOption.value }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.sucesso) {
          selectedOption.remove();
          localStorage.removeItem("musicaSelecionada");
          iniciarMusicaFundo(musicas.taswell);
        }
      })
      .catch(err => {
        console.error("Erro ao excluir:", err);
      })
      .finally(() => {
        modal.style.display = "none";
      });
  });

  // Cancela exclusão
  document.getElementById("btn-cancelar-exclusao").addEventListener("click", () => {
    modal.style.display = "none";
  });
});

  atualizarVisibilidadeBotao();
});