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

const languages = [
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
});