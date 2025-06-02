function showLogin() {
    document.getElementById("initial-screen").classList.remove("active");
    document.getElementById("signup-screen").classList.remove("active");
    document.getElementById("login-screen").classList.add("active");
    document.getElementById("rank-screen").classList.remove("active");
}

function showSignup() {
    document.getElementById("initial-screen").classList.remove("active");
    document.getElementById("login-screen").classList.remove("active");
    document.getElementById("signup-screen").classList.add("active");
    document.getElementById("rank-screen").classList.remove("active");
}

function goBack() {
    document.getElementById("login-screen").classList.remove("active");
    document.getElementById("signup-screen").classList.remove("active");
    document.getElementById("initial-screen").classList.add("active");
    document.getElementById("rank-screen").classList.remove("active");
}

function telaRanking() {
    document.getElementById("initial-screen").classList.remove("active");
    document.getElementById("signup-screen").classList.remove("active");
    document.getElementById("login-screen").classList.remove("active");
    document.getElementById("rank-screen").classList.add("active");
}