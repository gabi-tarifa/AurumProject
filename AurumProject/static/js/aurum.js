document.addEventListener("DOMContentLoaded", () => {
    const btnCadastro = document.getElementById("signup-btn");
    btnCadastro.addEventListener("click", async () => {
        const nome = document.querySelector('input[placeholder="Nome/Apelido"]').value;
        const email = document.querySelector('input[placeholder="Email"]').value;
        const senha = document.querySelector('input[placeholder="Senha"]').value;
        const confirmarSenha = document.querySelector('input[placeholder="Confirmar Senha"]').value;

        if (!nome || !email || !senha || !confirmarSenha) {
            alert("Por favor, preencha todos os campos.");
            return;
        }

        if(senha.length < 6 && senha.length > 16) {
            alert("A senha tem que ser maior que 6 dígitos e menor que 16 dígitos!");
            return;
        }

        if(confirmarSenha != senha){
            alert("As senhas não condizem! Verifique-as e tente novamente.");
            return;
        }

        try {
            const response = await fetch("/cadastro", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome, email, senha })
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.mensagem);
                window.location.href = "/login"; // Redireciona após cadastro
            } else {
                alert(data.mensagem);
            }
        } catch (error) {
            console.error("Erro ao cadastrar:", error);
            alert("Erro ao cadastrar. Verifique sua conexão.");
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("login-btn");

    btnLogin.addEventListener("click", async () => {
        const emailOuNome = document.querySelector('#login-screen input[placeholder="E-mail ou nome de usuário"]').value;
        const senha = document.querySelector('#login-screen input[placeholder="Senha"]').value;

        if (!emailOuNome || !senha) {
            alert("Por favor, preencha todos os campos.");
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
                alert(data.mensagem);
                window.location.href = "/introducao";  // Redireciona para a página de perguntas
            } else {
                alert(data.mensagem);
            }

        } catch (error) {
            console.error("Erro ao fazer login:", error);
            alert("Erro ao fazer login. Verifique sua conexão.");
        }
    });
});
