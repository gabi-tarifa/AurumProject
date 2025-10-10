def criar_conteudo():
    from app import app, db
    from models import ConteudoTarefa
    with app.app_context():
        conteudo_existente = {c.conteudo or c.pergunta for c in ConteudoTarefa.query.all()}

        conteudos_novos = [
            # MINI-AULA 1 — Receita e Despesa
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson1_text"},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q1", "alternativas": "lesson1_q1_a1||lesson1_q1_a2||lesson1_q1_a3||lesson1_q1_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q2", "alternativas": "lesson1_q2_a1||lesson1_q2_a2||lesson1_q2_a3||lesson1_q2_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q3", "alternativas": "lesson1_q3_a1||lesson1_q3_a2||lesson1_q3_a3||lesson1_q3_a4", "correta": 3},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q4", "alternativas": "lesson1_q4_a1||lesson1_q4_a2||lesson1_q4_a3||lesson1_q4_a4", "correta": 3},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q5", "alternativas": "lesson1_q5_a1||lesson1_q5_a2||lesson1_q5_a3||lesson1_q5_a4", "correta": 2},

            # MINI-AULA 2 — Como Registrar Gastos
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson2_text"},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q1", "alternativas": "lesson2_q1_a1||lesson2_q1_a2||lesson2_q1_a3||lesson2_q1_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q2", "alternativas": "lesson2_q2_a1||lesson2_q2_a2||lesson2_q2_a3||lesson2_q2_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q3", "alternativas": "lesson2_q3_a1||lesson2_q3_a2||lesson2_q3_a3||lesson2_q3_a4", "correta": 3},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q4", "alternativas": "lesson2_q4_a1||lesson2_q4_a2||lesson2_q4_a3||lesson2_q4_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q5", "alternativas": "lesson2_q5_a1||lesson2_q5_a2||lesson2_q5_a3||lesson2_q5_a4", "correta": 2},

            # MINI-AULA 3 — Necessidade vs. Desejo
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson3_text"},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q1", "alternativas": "lesson3_q1_a1||lesson3_q1_a2||lesson3_q1_a3||lesson3_q1_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q2", "alternativas": "lesson3_q2_a1||lesson3_q2_a2||lesson3_q2_a3||lesson3_q2_a4", "correta": 3},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q3", "alternativas": "lesson3_q3_a1||lesson3_q3_a2||lesson3_q3_a3||lesson3_q3_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q4", "alternativas": "lesson3_q4_a1||lesson3_q4_a2||lesson3_q4_a3||lesson3_q4_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q5", "alternativas": "lesson3_q5_a1||lesson3_q5_a2||lesson3_q5_a3||lesson3_q5_a4", "correta": 2},

            # MINI-AULA 4 — Criando um Orçamento
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson4_text"},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q1", "alternativas": "lesson4_q1_a1||lesson4_q1_a2||lesson4_q1_a3||lesson4_q1_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q2", "alternativas": "lesson4_q2_a1||lesson4_q2_a2||lesson4_q2_a3||lesson4_q2_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q3", "alternativas": "lesson4_q3_a1||lesson4_q3_a2||lesson4_q3_a3||lesson4_q3_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q4", "alternativas": "lesson4_q4_a1||lesson4_q4_a2||lesson4_q4_a3||lesson4_q4_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q5", "alternativas": "lesson4_q5_a1||lesson4_q5_a2||lesson4_q5_a3||lesson4_q5_a4", "correta": 1},
        ]


        for conteudo in conteudos_novos:
            valor = conteudo.get("conteudo") or conteudo.get("pergunta")
            if valor not in conteudo_existente:
                novo = ConteudoTarefa(**conteudo)
                db.session.add(novo)

        db.session.commit()