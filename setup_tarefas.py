def criar_tarefas():
    from app import app, db
    from models import Tarefa
    with app.app_context():
        tarefas_existentes = {t.descricao for t in Tarefa.query.all()}

        tarefas_novas = [
            {"id_modulo":1, "descricao":"Mini-aula 1 — Receita e Despesa", "pontos":10},
            {"id_modulo":1, "descricao":"Mini-aula 2 — Como Registrar Gastos", "pontos":10},
            {"id_modulo":1, "descricao":"Mini-aula 3 — Necessidade vs. Desejo", "pontos":10},
            {"id_modulo":1, "descricao":"Mini-aula 4 — Criando um Orçamento", "pontos":10},
            {"id_modulo":1, "descricao":"Avaliação Final — Módulo 1", "pontos":60}
        ]

        for tarefa in tarefas_novas:
            if tarefa["descricao"] not in tarefas_existentes:
                nova = Tarefa(**tarefa)
                db.session.add(nova)

        db.session.commit()