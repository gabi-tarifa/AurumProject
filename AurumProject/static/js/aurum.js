document.getElementById("btnCadastrar").addEventListener('click', () => {
    window.location.href = "/cadastro";
});

document.getElementById("btnEntrar").addEventListener('click', () => {
    window.location.href = "/login";
});

document.getElementById("btnVoltar").addEventListener('click', () => {
    window.location.href = "/";
});



document.addEventListener("DOMContentLoaded", () => {

    //cadastro 
    
    const btnCadastro = document.getElementById("signup-btn");
    btnCadastro.addEventListener("click", async () => {
        const nome = document.querySelector('input[placeholder="Nome completo"]').value;
        const email = document.querySelector('input[placeholder="Email"]').value;
        const senha = document.querySelector('input[placeholder="Senha"]').value;

        if (!nome || !email || !senha) {
            alert("Por favor, preencha todos os campos.");
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

    //login

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
                window.location.href = "/inicial";  // Redireciona para a página inicial (a.html)
            } else {
                alert(data.mensagem);
            }

        } catch (error) {
            console.error("Erro ao fazer login:", error);
            alert("Erro ao fazer login. Verifique sua conexão.");
        }
    });
});
