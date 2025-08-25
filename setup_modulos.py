def criar_modulos():
    from app import app, db
    from models import Modulo
    with app.app_context():
        modulo_existentes = {m.nome for m in Modulo.query.all()}

        modulos_novos = [
            {"nome": "Introdução ao Mundo Financeiro", "descricao":"Aprenda a diferenciar receitas e despesas, registrar gastos, identificar necessidades e desejos e montar um orçamento simples."}
            #,{"nome": "", "descricao":""}
        ]

        for modulo in modulos_novos:
            if modulo["nome"] not in modulo_existentes:
                nova = Modulo(**modulo)
                db.session.add(nova)

        db.session.commit()