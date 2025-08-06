def criar_conquistas():
    from app import app, db
    from models import Conquistas
    with app.app_context():
        conquistas_existentes = {c.nome for c in Conquistas.query.all()}

        conquistas_novas = [
            {"nome": "Primeiro Acesso", "descricao": "Você acessou o sistema pela primeira vez!", "imagem": "icons/enter.png", "cor": "vermelha"},
            {"nome": "Eu sou eu mesmo", "descricao": "Customizou seu perfil", "imagem": "icons/user-edit.png", "cor": "verde"},
            {"nome": "\"Quiz\" Pensador", "descricao": "Completou um quiz sem errar nenhuma questão.", "imagem": "icons/knowledge.png", "cor": "amarela"},
            {"nome": "Eu SOU um OG", "descricao": "Criou sua conta e fez login em até um mês depois do nosso lancamento.", "imagem": "icons/exclusive.png", "cor": "azul"},
            {"nome": "Vencedor", "descricao": "Terminou em primeiro lugar no ranking", "imagem": "icons/winner.png", "cor": "dourada"},
            {"nome": "Veterano", "descricao": "Terminou em primeiro lugar no ranking 10 vezes", "imagem": "icons/stars.png", "cor": "dourada"},
            {"nome": "Campeão", "descricao": "Terminou em primeiro lugar no ranking 100 vezes", "imagem": "icons/crown.png", "cor": "dourada"},
            {"nome": "Campeão Invicto", "descricao": "Terminou em primeiro lugar no ranking 30 vezes consecutivas", "imagem": "icons/1st-prize.png", "cor": "dourada"},
            {"nome": "Quizzer", "descricao": "Completou seu primeiro quiz", "imagem": "icons/quizzer.png", "cor": "azul"},
            {"nome": "Quizzeiro", "descricao": "Completou 10 quizes", "imagem": "icons/quizzeiro.png", "cor": "azul"},
            {"nome": "Maluco por quiz", "descricao": "Completou 50 quizes", "imagem": "icons/maluco_por_quiz.png", "cor": "azul"},
            {"nome": "Fanático por quiz", "descricao": "Completou 100 quizes", "imagem": "icons/fire.png", "cor": "azul"},
            {"nome": "Em crescimento", "descricao": "Alcançou 100 pontos", "imagem": "icons/sprout.png", "cor": "azul"},
            {"nome": "Experiente", "descricao": "Alcançou 1.000 pontos", "imagem": "icons/statistics.png", "cor": "azul"},
            {"nome": "O Guru", "descricao": "Alcançou 10.000 pontos", "imagem": "icons/guru.png", "cor": "azul"},
            {"nome": "Aurum Master", "descricao": "Alcançou 99.999 pontos", "imagem": "icons/ranking.png", "cor": "darkazul"},
            {"nome": "Primeira Ofensiva", "descricao": "Completou atividades em 1 dia seguido", "imagem": "icons/winner.png", "cor": "laranja"},
            {"nome": "Semana de Fogo", "descricao": "Completou atividades em 7 dias seguido", "imagem": "icons/streak.png", "cor": "laranja"},
            {"nome": "Persistente", "descricao": "Completou atividades por 30 dias seguidos", "imagem": "icons/ofensiva_30.png", "cor": "vermelha"},
            {"nome": "Imparável", "descricao": "Completou atividades por 180 dias seguidos", "imagem": "icons/ofensiva_180.png", "cor": "vermelha"},
            {"nome": "Lenda da Constância", "descricao": "Completou atividades por 365 dias seguidos", "imagem": "icons/crown.png", "cor": "darkred"},

        ]

        for conquista in conquistas_novas:
            if conquista["nome"] not in conquistas_existentes:
                nova = Conquistas(**conquista)
                db.session.add(nova)

        db.session.commit()