def criar_tarefas():
    from app import app, db
    from models import Tarefa
    with app.app_context():
        tarefas_existentes = {t.descricao for t in Tarefa.query.all()}

        tarefas_novas = [
            # MOdulo 1
            {"id_modulo":1, "descricao":"mini_lesson1", "pontos":10, "numero_tarefa": 1},
            {"id_modulo":1, "descricao":"mini_lesson2", "pontos":20, "numero_tarefa": 2},
            {"id_modulo":1, "descricao":"mini_lesson3", "pontos":20, "numero_tarefa": 3},
            {"id_modulo":1, "descricao":"mini_lesson4", "pontos":25, "numero_tarefa": 4},
            #{"id_modulo":1, "descricao":"Avaliação Final — Módulo 1", "pontos":90, "numero_tarefa": 5},

            # Modulo 2
            
            {"id_modulo":2, "descricao":"mini_lesson2_1", "pontos":15, "numero_tarefa": 1},
            {"id_modulo":2, "descricao":"mini_lesson2_2", "pontos":20, "numero_tarefa": 2},
            {"id_modulo":2, "descricao":"mini_lesson2_3", "pontos":35, "numero_tarefa": 3},
            {"id_modulo":2, "descricao":"mini_lesson2_4", "pontos":40, "numero_tarefa": 4},
            {"id_modulo":2, "descricao":"mini_lesson2_5", "pontos":50, "numero_tarefa": 5},
            {"id_modulo":2, "descricao":"mini_lesson2_6", "pontos":100, "numero_tarefa": 6},

        ]

        for tarefa in tarefas_novas:
            if tarefa["descricao"] not in tarefas_existentes:
                nova = Tarefa(**tarefa)
                db.session.add(nova)

        db.session.commit()