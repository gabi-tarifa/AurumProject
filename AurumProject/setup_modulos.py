def criar_modulos():
    from app import app, db
    from models import Modulo
    with app.app_context():
        modulo_existentes = {m.chave_nome for m in Modulo.query.all()}

        modulos_novos = [
            {"chave_nome": "Introdução ao Mundo Financeiro", "chave_descricao":"Aprenda a diferenciar receitas e despesas, registrar gastos, identificar necessidades e desejos e montar um orçamento simples."}
            #,{"nome": "", "descricao":""}
        ]

        for modulo in modulos_novos:
            if modulo["chave_nome"] not in modulo_existentes:
                nova = Modulo(**modulo)
                db.session.add(nova)

        db.session.commit()