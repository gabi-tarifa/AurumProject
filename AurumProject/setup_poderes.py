def criar_poderes():
    from app import app, db
    from models import Poderes
    with app.app_context():
        poderes_existentes = {c.nome for c in Poderes.query.all()}

        poderes_novos = [
            {"nome":"Segunda Chance","descricao":"Mantenha a sua ofensiva sem medo de errar!","preco":200,"imagem":"imgpoderes/broken-heart.png"}
        ]

        for poder in poderes_novos:
            if poder["nome"] not in poderes_existentes:
                nova = Poderes(**poder)
                db.session.add(nova)

        db.session.commit()