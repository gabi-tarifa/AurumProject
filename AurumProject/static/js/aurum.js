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

// 🔹 Função auxiliar para validar idade mínima
function validarIdade(minIdade, dataNascimentoStr) {
    const texto = document.getElementById("textoerro");
    const dataNascimento = new Date(dataNascimentoStr);
    const hoje = new Date();

    if (isNaN(dataNascimento)) {
        texto.textContent = "Por favor, selecione uma data de nascimento válida.";
        return false;
    }

    let idade = hoje.getFullYear() - dataNascimento.getFullYear();
    const mes = hoje.getMonth() - dataNascimento.getMonth();

    if (mes < 0 || (mes === 0 && hoje.getDate() < dataNascimento.getDate())) {
        idade--;
    }

    if (idade < minIdade) {
        return false;
    }

    texto.textContent = "";
    return true;
}

document.addEventListener("DOMContentLoaded", () => {
    const btnCadastro = document.getElementById("signup-btn");
    const texto = document.getElementById("textoerro");
    btnCadastro.addEventListener("click", async () => {
        const nome = document.querySelector('input[placeholder="Nome/Apelido"]').value;
        const email = document.querySelector('input[placeholder="Email"]').value;
        const senha = document.querySelector('input[placeholder="Senha"]').value;
        const confirmarSenha = document.querySelector('input[placeholder="Confirmar Senha"]').value;
        const dataNascimento = document.getElementById('data_nascimento').value;
        const idioma = document.getElementById("idioma").value;

        if (!nome || !email || !senha || !confirmarSenha) {
            texto.textContent = "Por favor, preencha todos os campos";
            return;
        }

        
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            texto.textContent = "Por favor, insira um email válido (ex: nome@exemplo.com)";
            return;
        }

        if(senha.length < 6 || senha.length > 16 || !temMaiuscula(senha) || !temMinuscula(senha) || !temNumero(senha) || !temCaractereEspecial(senha)) {
            texto.innerHTML = "Um dos seguintes requisitos não foi cumprido: <br>- A senha tem que ser maior que 6 dígitos e menor que 16 dígitos;<br>- A senha deve conter pelo menos uma letra maiúscula;<br>- A senha deve conter pelo menos uma letra minúscula;<br>- A senha deve conter pelo menos um número;<br>- A senha deve conter pelo menos um caractere especial.";
            return;
        }
        
        if(confirmarSenha != senha){
            texto.textContent = "As senhas não condizem!";
            return;
        }

        if (!validarIdade(12, dataNascimento)) {
            texto.textContent = "Você precisa ter pelo menos 12 anos para se cadastrar.";
            return;
        }

        try {
            const response = await fetch("/cadastro", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome, email, senha, idioma })
            });

            const data = await response.json();
            if (response.ok) {
                window.location.href = "/login"; // Redireciona após cadastro
            } else {
                texto.textContent = "Opa, algo deu errado. Tente novamente mais tarde"
            }
        } catch (error) {
            console.error("Erro ao cadastrar:", error);
            texto.textContent = "Erro ao cadastrar. Verifique sua conexão.";
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("login-btn");

    btnLogin.addEventListener("click", async () => {
        const emailOuNome = (document.querySelector('#login-screen input[placeholder="E-mail ou nome de usuário"]').value).toLowerCase();
        const senha = document.querySelector('#login-screen input[placeholder="Senha"]').value;
        const textoerro = document.getElementById("textoerro");

        if (!emailOuNome || !senha) {
            textoerro.textContent = "Por favor, preencha todos os campos.";
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ emailOuNome, senha })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = "/introducao";  // Redireciona para a página de perguntas
            } else {
                textoerro.textContent = "Usuário ou senha incorreta";
            }

        } catch (error) {
            console.error("Erro ao fazer login:", error);
            textoerro.textContent = "Usuário ou senha incorreta";
        }
    });
});
