function alterarApelido() {
    alert("Função para alterar apelido");
}

function alterarFoto() {
    alert("Função para alterar foto de perfil");
}

function alterarSenha() {
    alert("Função para alterar senha");
}

 function resetarConfig() {
     if (confirm("Tem certeza que deseja redefinir as configurações?")) {
        alert("Configurações redefinidas!");
    }
}

/*const languages = [
    { code: "pt-BR", name: "Português (Brasil)" },
    { code: "pt-PT", name: "Português (Portugal)" },
    { code: "en-US", name: "English (United States)" },
    { code: "en-GB", name: "English (United Kingdom)" },
    { code: "es-ES", name: "Español (España)" },
    { code: "es-MX", name: "Español (México)" },
  ];

const select = document.getElementById("language");

languages.forEach(lang => {
    const option = document.createElement("option");
    option.value = lang.code;
    option.textContent = lang.name;
    select.appendChild(option);
});*/

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
