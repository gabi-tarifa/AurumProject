def criar_conteudo():
    from app import app, db
    from models import ConteudoTarefa
    with app.app_context():
        conteudo_existente = {c.conteudo or c.pergunta for c in ConteudoTarefa.query.all()}

        conteudos_novos = [
            # M1 - MINI-AULA 1 — Receita e Despesa
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson1_text"},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q1", "alternativas": "lesson1_q1_a1||lesson1_q1_a2||lesson1_q1_a3||lesson1_q1_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q2", "alternativas": "lesson1_q2_a1||lesson1_q2_a2||lesson1_q2_a3||lesson1_q2_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q3", "alternativas": "lesson1_q3_a1||lesson1_q3_a2||lesson1_q3_a3||lesson1_q3_a4", "correta": 3},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q4", "alternativas": "lesson1_q4_a1||lesson1_q4_a2||lesson1_q4_a3||lesson1_q4_a4", "correta": 3},
            {"numero_tarefa": 1, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson1_q5", "alternativas": "lesson1_q5_a1||lesson1_q5_a2||lesson1_q5_a3||lesson1_q5_a4", "correta": 2},

            # M1 - MINI-AULA 2 — Como Registrar Gastos
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson2_text"},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q1", "alternativas": "lesson2_q1_a1||lesson2_q1_a2||lesson2_q1_a3||lesson2_q1_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q2", "alternativas": "lesson2_q2_a1||lesson2_q2_a2||lesson2_q2_a3||lesson2_q2_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q3", "alternativas": "lesson2_q3_a1||lesson2_q3_a2||lesson2_q3_a3||lesson2_q3_a4", "correta": 3},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q4", "alternativas": "lesson2_q4_a1||lesson2_q4_a2||lesson2_q4_a3||lesson2_q4_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson2_q5", "alternativas": "lesson2_q5_a1||lesson2_q5_a2||lesson2_q5_a3||lesson2_q5_a4", "correta": 2},

            # M1 - MINI-AULA 3 — Necessidade vs. Desejo
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson3_text"},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q1", "alternativas": "lesson3_q1_a1||lesson3_q1_a2||lesson3_q1_a3||lesson3_q1_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q2", "alternativas": "lesson3_q2_a1||lesson3_q2_a2||lesson3_q2_a3||lesson3_q2_a4", "correta": 3},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q3", "alternativas": "lesson3_q3_a1||lesson3_q3_a2||lesson3_q3_a3||lesson3_q3_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q4", "alternativas": "lesson3_q4_a1||lesson3_q4_a2||lesson3_q4_a3||lesson3_q4_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson3_q5", "alternativas": "lesson3_q5_a1||lesson3_q5_a2||lesson3_q5_a3||lesson3_q5_a4", "correta": 2},

            # M1 - MINI-AULA 4 — Criando um Orçamento
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "texto", "conteudo": "lesson4_text"},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q1", "alternativas": "lesson4_q1_a1||lesson4_q1_a2||lesson4_q1_a3||lesson4_q1_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q2", "alternativas": "lesson4_q2_a1||lesson4_q2_a2||lesson4_q2_a3||lesson4_q2_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q3", "alternativas": "lesson4_q3_a1||lesson4_q3_a2||lesson4_q3_a3||lesson4_q3_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q4", "alternativas": "lesson4_q4_a1||lesson4_q4_a2||lesson4_q4_a3||lesson4_q4_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 1, "tipo": "quiz", "pergunta": "lesson4_q5", "alternativas": "lesson4_q5_a1||lesson4_q5_a2||lesson4_q5_a3||lesson4_q5_a4", "correta": 1},

            # M2 - Mini-aula 1 — Juros Simples
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "texto", "conteudo": "lesson_2_1_text"},
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_1_q1", "alternativas": "lesson_2_1_q1_a1||lesson_2_1_q1_a2||lesson_2_1_q1_a3||lesson_2_1_q1_a4", "correta": 1},
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_1_q2", "alternativas": "lesson_2_1_q2_a1||lesson_2_1_q2_a2||lesson_2_1_q2_a3||lesson_2_1_q2_a4", "correta": 1},
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_1_q3", "alternativas": "lesson_2_1_q3_a1||lesson_2_1_q3_a2||lesson_2_1_q3_a3||lesson_2_1_q3_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_1_q4", "alternativas": "lesson_2_1_q4_a1||lesson_2_1_q4_a2||lesson_2_1_q4_a3||lesson_2_1_q4_a4", "correta": 1},
            {"numero_tarefa": 1, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_1_q5", "alternativas": "lesson_2_1_q5_a1||lesson_2_1_q5_a2||lesson_2_1_q5_a3||lesson_2_1_q5_a4", "correta": 2},

            # M2 - Mini-aula 2 — Crédito e Empréstimos
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "texto", "conteudo": "lesson_2_2_text"},
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_2_q1", "alternativas": "lesson_2_2_q1_a1||lesson_2_2_q1_a2||lesson_2_2_q1_a3||lesson_2_2_q1_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_2_q2", "alternativas": "lesson_2_2_q2_a1||lesson_2_2_q2_a2||lesson_2_2_q2_a3||lesson_2_2_q2_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_2_q3", "alternativas": "lesson_2_2_q3_a1||lesson_2_2_q3_a2||lesson_2_2_q3_a3||lesson_2_2_q3_a4", "correta": 3},
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_2_q4", "alternativas": "lesson_2_2_q4_a1||lesson_2_2_q4_a2||lesson_2_2_q4_a3||lesson_2_2_q4_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_2_q5", "alternativas": "lesson_2_2_q5_a1||lesson_2_2_q5_a2||lesson_2_2_q5_a3||lesson_2_2_q5_a4", "correta": 3},

            # M2 - Mini-aula 3 — Poupança x Investimento
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "texto", "conteudo": "lesson_2_3_text"},
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_3_q1", "alternativas": "lesson_2_3_q1_a1||lesson_2_3_q1_a2||lesson_2_3_q1_a3||lesson_2_3_q1_a4", "correta": 2},
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_3_q2", "alternativas": "lesson_2_3_q2_a1||lesson_2_3_q2_a2||lesson_2_3_q2_a3||lesson_2_3_q2_a4", "correta": 2},
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_3_q3", "alternativas": "lesson_2_3_q3_a1||lesson_2_3_q3_a2||lesson_2_3_q3_a3||lesson_2_3_q3_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_3_q4", "alternativas": "lesson_2_3_q4_a1||lesson_2_3_q4_a2||lesson_2_3_q4_a3||lesson_2_3_q4_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_3_q5", "alternativas": "lesson_2_3_q5_a1||lesson_2_3_q5_a2||lesson_2_3_q5_a3||lesson_2_3_q5_a4", "correta": 2},

            # M2 - Mini-aula 4 — Juros no Cartão de Crédito
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "texto", "conteudo": "lesson_2_4_text"},
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_4_q1", "alternativas": "lesson_2_4_q1_a1||lesson_2_4_q1_a2||lesson_2_4_q1_a3||lesson_2_4_q1_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_4_q2", "alternativas": "lesson_2_4_q2_a1||lesson_2_4_q2_a2||lesson_2_4_q2_a3||lesson_2_4_q2_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_4_q3", "alternativas": "lesson_2_4_q3_a1||lesson_2_4_q3_a2||lesson_2_4_q3_a3||lesson_2_4_q3_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_4_q4", "alternativas": "lesson_2_4_q4_a1||lesson_2_4_q4_a2||lesson_2_4_q4_a3||lesson_2_4_q4_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_4_q5", "alternativas": "lesson_2_4_q5_a1||lesson_2_4_q5_a2||lesson_2_4_q5_a3||lesson_2_4_q5_a4", "correta": 1},

            # M2 - Mini-aula 5 — Taxas e Cálculos Básicos
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "texto", "conteudo": "lesson_2_5_text"},
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_5_q1", "alternativas": "lesson_2_5_q1_a1||lesson_2_5_q1_a2||lesson_2_5_q1_a3||lesson_2_5_q1_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_5_q2", "alternativas": "lesson_2_5_q2_a1||lesson_2_5_q2_a2||lesson_2_5_q2_a3||lesson_2_5_q2_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_5_q3", "alternativas": "lesson_2_5_q3_a1||lesson_2_5_q3_a2||lesson_2_5_q3_a3||lesson_2_5_q3_a4", "correta": 1},
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_5_q4", "alternativas": "lesson_2_5_q4_a1||lesson_2_5_q4_a2||lesson_2_5_q4_a3||lesson_2_5_q4_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_5_q5", "alternativas": "lesson_2_5_q5_a1||lesson_2_5_q5_a2||lesson_2_5_q5_a3||lesson_2_5_q5_a4", "correta": 2},

            # M2 - Avaliação Final — Módulo 2"
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q1", "alternativas": "lesson_2_6_q1_a1||lesson_2_6_q1_a2||lesson_2_6_q1_a3||lesson_2_6_q1_a4", "correta": 1},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q2", "alternativas": "lesson_2_6_q2_a1||lesson_2_6_q2_a2||lesson_2_6_q2_a3||lesson_2_6_q2_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q3", "alternativas": "lesson_2_6_q3_a1||lesson_2_6_q3_a2||lesson_2_6_q3_a3||lesson_2_6_q3_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q4", "alternativas": "lesson_2_6_q4_a1||lesson_2_6_q4_a2||lesson_2_6_q4_a3||lesson_2_6_q4_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q5", "alternativas": "lesson_2_6_q5_a1||lesson_2_6_q5_a2||lesson_2_6_q5_a3||lesson_2_6_q5_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q6", "alternativas": "lesson_2_6_q6_a1||lesson_2_6_q6_a2||lesson_2_6_q6_a3||lesson_2_6_q6_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q7", "alternativas": "lesson_2_6_q7_a1||lesson_2_6_q7_a2||lesson_2_6_q7_a3||lesson_2_6_q7_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q8", "alternativas": "lesson_2_6_q8_a1||lesson_2_6_q8_a2||lesson_2_6_q8_a3||lesson_2_6_q8_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q9", "alternativas": "lesson_2_6_q9_a1||lesson_2_6_q9_a2||lesson_2_6_q9_a3||lesson_2_6_q9_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 2, "tipo": "quiz", "pergunta": "lesson_2_6_q10", "alternativas": "lesson_2_6_q10_a1||lesson_2_6_q10_a2||lesson_2_6_q10_a3||lesson_2_6_q10_a4", "correta": 1},

            #M3 - Mini-aula 1 — Juros Compostos
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "texto", "conteudo": "lesson_3_1_text"},
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_1_q1", "alternativas": "lesson_3_1_q1_a1||lesson_3_1_q1_a2||lesson_3_1_q1_a3||lesson_3_1_q1_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_1_q2", "alternativas": "lesson_3_1_q2_a1||lesson_3_1_q2_a2||lesson_3_1_q2_a3||lesson_3_1_q2_a4", "correta": 3},
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_1_q3", "alternativas": "lesson_3_1_q3_a1||lesson_3_1_q3_a2||lesson_3_1_q3_a3||lesson_3_1_q3_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_1_q4", "alternativas": "lesson_3_1_q4_a1||lesson_3_1_q4_a2||lesson_3_1_q4_a3||lesson_3_1_q4_a4", "correta": 2},
            {"numero_tarefa": 1, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_1_q5", "alternativas": "lesson_3_1_q5_a1||lesson_3_1_q5_a2||lesson_3_1_q5_a3||lesson_3_1_q5_a4", "correta": 3},

            #M3 - Mini-aula 2 — Inflação
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "texto", "conteudo": "lesson_3_2_text"},
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_2_q1", "alternativas": "lesson_3_2_q1_a1||lesson_3_2_q1_a2||lesson_3_2_q1_a3||lesson_3_2_q1_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_2_q2", "alternativas": "lesson_3_2_q2_a1||lesson_3_2_q2_a2||lesson_3_2_q2_a3||lesson_3_2_q2_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_2_q3", "alternativas": "lesson_3_2_q3_a1||lesson_3_2_q3_a2||lesson_3_2_q3_a3||lesson_3_2_q3_a4", "correta": 2},
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_2_q4", "alternativas": "lesson_3_2_q4_a1||lesson_3_2_q4_a2||lesson_3_2_q4_a3||lesson_3_2_q4_a4", "correta": 1},
            {"numero_tarefa": 2, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_2_q5", "alternativas": "lesson_3_2_q5_a1||lesson_3_2_q5_a2||lesson_3_2_q5_a3||lesson_3_2_q5_a4", "correta": 2},

            #M3 - Mini-aula 3 — Taxas Mensal x Taxa Anual
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "texto", "conteudo": "lesson_3_3_text"},
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_3_q1", "alternativas": "lesson_3_3_q1_a1||lesson_3_3_q1_a2||lesson_3_3_q1_a3||lesson_3_3_q1_a4", "correta": 2},
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_3_q2", "alternativas": "lesson_3_3_q2_a1||lesson_3_3_q2_a2||lesson_3_3_q2_a3||lesson_3_3_q2_a4", "correta": 2},
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_3_q3", "alternativas": "lesson_3_3_q3_a1||lesson_3_3_q3_a2||lesson_3_3_q3_a3||lesson_3_3_q3_a4", "correta": 2},
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_3_q4", "alternativas": "lesson_3_3_q4_a1||lesson_3_3_q4_a2||lesson_3_3_q4_a3||lesson_3_3_q4_a4", "correta": 1},
            {"numero_tarefa": 3, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_3_q5", "alternativas": "lesson_3_3_q5_a1||lesson_3_3_q5_a2||lesson_3_3_q5_a3||lesson_3_3_q5_a4", "correta": 1},

            #M3 - Mini-aula 4 — Comparando Investimentos
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "texto", "conteudo": "lesson_3_4_text"},
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_4_q1", "alternativas": "lesson_3_4_q1_a1||lesson_3_4_q1_a2||lesson_3_4_q1_a3||lesson_3_4_q1_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_4_q2", "alternativas": "lesson_3_4_q2_a1||lesson_3_4_q2_a2||lesson_3_4_q2_a3||lesson_3_4_q2_a4", "correta": 3},
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_4_q3", "alternativas": "lesson_3_4_q3_a1||lesson_3_4_q3_a2||lesson_3_4_q3_a3||lesson_3_4_q3_a4", "correta": 2},
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_4_q4", "alternativas": "lesson_3_4_q4_a1||lesson_3_4_q4_a2||lesson_3_4_q4_a3||lesson_3_4_q4_a4", "correta": 1},
            {"numero_tarefa": 4, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_4_q5", "alternativas": "lesson_3_4_q5_a1||lesson_3_4_q5_a2||lesson_3_4_q5_a3||lesson_3_4_q5_a4", "correta": 2},

            #M3 - Mini-aula 5 — Planejamento de Médio Prazo
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "texto", "conteudo": "lesson_3_5_text"},
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_5_q1", "alternativas": "lesson_3_5_q1_a1||lesson_3_5_q1_a2||lesson_3_5_q1_a3||lesson_3_5_q1_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_5_q2", "alternativas": "lesson_3_5_q2_a1||lesson_3_5_q2_a2||lesson_3_5_q2_a3||lesson_3_5_q2_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_5_q3", "alternativas": "lesson_3_5_q3_a1||lesson_3_5_q3_a2||lesson_3_5_q3_a3||lesson_3_5_q3_a4", "correta": 3},
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_5_q4", "alternativas": "lesson_3_5_q4_a1||lesson_3_5_q4_a2||lesson_3_5_q4_a3||lesson_3_5_q4_a4", "correta": 2},
            {"numero_tarefa": 5, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_5_q5", "alternativas": "lesson_3_5_q5_a1||lesson_3_5_q5_a2||lesson_3_5_q5_a3||lesson_3_5_q5_a4", "correta": 1},

            #M3 - Avaliação Final - Módulo 3
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q1", "alternativas": "lesson_3_6_q1_a1||lesson_3_6_q1_a2||lesson_3_6_q1_a3||lesson_3_6_q1_a4", "correta": 1},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q2", "alternativas": "lesson_3_6_q2_a1||lesson_3_6_q2_a2||lesson_3_6_q2_a3||lesson_3_6_q2_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q3", "alternativas": "lesson_3_6_q3_a1||lesson_3_6_q3_a2||lesson_3_6_q3_a3||lesson_3_6_q3_a4", "correta": 3},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q4", "alternativas": "lesson_3_6_q4_a1||lesson_3_6_q4_a2||lesson_3_6_q4_a3||lesson_3_6_q4_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q5", "alternativas": "lesson_3_6_q5_a1||lesson_3_6_q5_a2||lesson_3_6_q5_a3||lesson_3_6_q5_a4", "correta": 3},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q6", "alternativas": "lesson_3_6_q6_a1||lesson_3_6_q6_a2||lesson_3_6_q6_a3||lesson_3_6_q6_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q7", "alternativas": "lesson_3_6_q7_a1||lesson_3_6_q7_a2||lesson_3_6_q7_a3||lesson_3_6_q7_a4", "correta": 3},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q8", "alternativas": "lesson_3_6_q8_a1||lesson_3_6_q8_a2||lesson_3_6_q8_a3||lesson_3_6_q8_a4", "correta": 1},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q9", "alternativas": "lesson_3_6_q9_a1||lesson_3_6_q9_a2||lesson_3_6_q9_a3||lesson_3_6_q9_a4", "correta": 2},
            {"numero_tarefa": 6, "id_modulo": 3, "tipo": "quiz", "pergunta": "lesson_3_6_q10", "alternativas": "lesson_3_6_q10_a1||lesson_3_6_q10_a2||lesson_3_6_q10_a3||lesson_3_6_q10_a4", "correta": 1}

        ]


        for conteudo in conteudos_novos:
            valor = conteudo.get("conteudo") or conteudo.get("pergunta")
            if valor not in conteudo_existente:
                novo = ConteudoTarefa(**conteudo)
                db.session.add(novo)

        db.session.commit()