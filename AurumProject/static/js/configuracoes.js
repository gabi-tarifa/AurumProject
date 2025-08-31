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

    if(nova.length < 6 || nova.length > 16 || !temMaiuscula(senha) || !temMinuscula(senha) || !temNumero(senha) || !temCaractereEspecial(senha)) {
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
    .then(r => r.json())
    .then(data => {
        alert(data.message);
        fecharDiv("div-senha");
    });
}

 function resetarConfig() {
     if (confirm("Tem certeza que deseja redefinir as configurações?")) {
        alert("Configurações redefinidas!");
    }
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
