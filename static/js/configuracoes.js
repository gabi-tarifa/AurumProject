function abrirDiv(id) {
    document.getElementById(id).classList.remove("oculto");
}

function fecharDiv(id) {
    document.getElementById(id).classList.add("oculto");
}

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

async function carregarConfig() {
    const r = await fetch("/api/config");
    if (!r.ok) {
        console.error("Erro ao buscar config");
        return;
    }
    const data = await r.json();

    document.getElementById("sons").checked = data.sons;
    document.getElementById("musica").checked = data.musica;
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

    sons.addEventListener("change", salvarConfig);
    musica.addEventListener("change", salvarConfig);
    idioma.addEventListener("change", salvarConfig);
});
