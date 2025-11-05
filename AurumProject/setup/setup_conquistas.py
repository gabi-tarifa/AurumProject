def criar_conquistas():
    from app import app, db
    from models import Conquistas
    with app.app_context():
        conquistas_existentes = {c.nome for c in Conquistas.query.all()}

        conquistas_novas = [
            {"nome": "conquista_primeiro_acesso_nome", "descricao": "conquista_primeiro_acesso_desc", "imagem": "icons/enter.png", "cor": "vermelha", "raridade": "regular"},
            {"nome": "conquista_customizou_perfil_nome", "descricao": "conquista_customizou_perfil_desc", "imagem": "icons/user-edit.png", "cor": "verde", "raridade": "rara"},
            {"nome": "conquista_quiz_pensador_nome", "descricao": "conquista_quiz_pensador_desc", "imagem": "icons/knowledge.png", "cor": "amarela", "raridade": "rara"},
            {"nome": "conquista_og_nome", "descricao": "conquista_og_desc", "imagem": "icons/exclusive.png", "cor": "azul", "raridade": "lendaria"},
            {"nome": "conquista_vencedor_nome", "descricao": "conquista_vencedor_desc", "imagem": "icons/winner.png", "cor": "dourada", "raridade": "regular"},
            {"nome": "conquista_veterano_nome", "descricao": "conquista_veterano_desc", "imagem": "icons/stars.png", "cor": "dourada", "raridade": "rara"},
            {"nome": "conquista_campeao_nome", "descricao": "conquista_campeao_desc", "imagem": "icons/crown.png", "cor": "dourada", "raridade": "lendaria"},
            {"nome": "conquista_invicto_nome", "descricao": "conquista_invicto_desc", "imagem": "icons/1st-prize.png", "cor": "dourada", "raridade": "lendaria"},
            {"nome": "conquista_quizzer_nome", "descricao": "conquista_quizzer_desc", "imagem": "icons/quizzer.png", "cor": "azul", "raridade": "regular"},
            {"nome": "conquista_quizzeiro_nome", "descricao": "conquista_quizzeiro_desc", "imagem": "icons/quizzeiro.png", "cor": "azul", "raridade": "regular"},
            {"nome": "conquista_maluco_quiz_nome", "descricao": "conquista_maluco_quiz_desc", "imagem": "icons/maluco_por_quiz.png", "cor": "azul", "raridade": "rara"},
            {"nome": "conquista_fanatico_quiz_nome", "descricao": "conquista_fanatico_quiz_desc", "imagem": "icons/fire.png", "cor": "azul", "raridade": "lendaria"},
            {"nome": "conquista_em_crescimento_nome", "descricao": "conquista_em_crescimento_desc", "imagem": "icons/sprout.png", "cor": "azul", "raridade": "regular"},
            {"nome": "conquista_experiente_nome", "descricao": "conquista_experiente_desc", "imagem": "icons/statistics.png", "cor": "azul", "raridade": "regular"},
            {"nome": "conquista_guru_nome", "descricao": "conquista_guru_desc", "imagem": "icons/guru.png", "cor": "azul", "raridade": "rara"},
            {"nome": "conquista_aurum_master_nome", "descricao": "conquista_aurum_master_desc", "imagem": "icons/ranking.png", "cor": "darkazul", "raridade": "lendaria"},
            {"nome": "conquista_primeira_ofensiva_nome", "descricao": "conquista_primeira_ofensiva_desc", "imagem": "icons/winner.png", "cor": "laranja", "raridade": "regular"},
            {"nome": "conquista_semana_fogo_nome", "descricao": "conquista_semana_fogo_desc", "imagem": "icons/streak.png", "cor": "laranja", "raridade": "regular"},
            {"nome": "conquista_persistente_nome", "descricao": "conquista_persistente_desc", "imagem": "icons/ofensiva_30.png", "cor": "vermelha", "raridade": "rara"},
            {"nome": "conquista_imparavel_nome", "descricao": "conquista_imparavel_desc", "imagem": "icons/ofensiva_180.png", "cor": "vermelha", "raridade": "rara"},
            {"nome": "conquista_lenda_constancia_nome", "descricao": "conquista_lenda_constancia_desc", "imagem": "icons/crown.png", "cor": "darkred", "raridade": "lendaria"},
            {"nome": "conquista_farinha_nome", "descricao": "conquista_farinha_desc", "imagem": "icons/ifsp.png", "cor": "branco", "raridade": "lendaria"},
        ]

        for conquista in conquistas_novas:
            if conquista["nome"] not in conquistas_existentes:
                nova = Conquistas(**conquista)
                db.session.add(nova)

        db.session.commit()
