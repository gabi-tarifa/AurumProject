def criar_conteudo():
    from app import app, db
    from models import ConteudoTarefa
    with app.app_context():
        conteudo_existente = {c.conteudo or c.pergunta for c in ConteudoTarefa.query.all()}

        conteudos_novos = [
            # ===== Mini-aula 1 — Receita e Despesa (id_tarefa = 1) =====
            {"id_tarefa":1, "tipo":"texto", "conteudo":"<h3>Conceito</h3> <p><strong>Receita</strong>: Todo dinheiro que entra. (Ex.: salário, venda de produtos, mesada, aluguéis recebidos.)</p> <p><strong>Despesa</strong>: Todo dinheiro que sai. (Ex.: contas de luz, compras no mercado, passagem de ônibus.)</p>"},
            {"id_tarefa":1, "tipo":"texto", "conteudo":"<h3>Exemplo prático</h3><p>Se você recebe R$ 1.500 e gasta R$ 600 em contas, a parte que sobra pode ser usada para outros propósitos.</p><p>Portanto, os R$1.500,00 recebidos são RECEITA e os R$600,00 gastos são DESPESAS</p>"},
            {"id_tarefa":1, "tipo":"quiz", "pergunta":"O que é uma receita?", "alternativas":"O dinheiro que você gasta||O dinheiro que você recebe||Uma dívida", "correta":2},

            # ===== Mini-aula 2 — Como Registrar Gastos (id_tarefa = 2) =====
            {"id_tarefa":2, "tipo":"texto", "conteudo":"<h3>Por que registrar?</h3><p>Registrar os gastos ajuda a saber para onde o dinheiro está indo.</p><p>Você pode usar papel, planilha ou aplicativos gratuitos.</p>"},
            {"id_tarefa":2, "tipo":"texto", "conteudo":"<h3>Modelo simples</h3><table><thead><tr><th>Data</th><th>Descrição</th><th>Tipo</th><th>Valor</th></tr></thead><tbody><tr><td>05/08</td><td>Conta de luz</td><td>Despesa</td><td>R$ 120</td></tr><tr><td>07/08</td><td>Salário</td><td>Receita</td><td>R$ 1.500</td></tr><tr><td>09/08</td><td>Cinema</td><td>Despesa</td><td>R$ 40</td></tr></tbody></table>"},
            {"id_tarefa":2, "tipo":"quiz",  "pergunta":"Registrar gastos serve para:", "alternativas":"Controlar o dinheiro||Gastar mais||Ganhar dinheiro fácil", "correta":1},
            {"id_tarefa":2, "tipo":"quiz",  "pergunta":"É possível registrar gastos:", "alternativas":"Apenas em aplicativos pagos||Em papel, planilha ou app||Somente no banco", "correta":2},

            # ===== Mini-aula 3 — Necessidade vs. Desejo (id_tarefa = 3) =====
            {"id_tarefa":3, "tipo":"texto", "conteudo":"<h3>Necessidade vs. Desejo</h3><p><strong>Necessidade</strong>: gasto essencial, que você não pode deixar de pagar (moradia, alimentação, saúde).</p><p><strong>Desejo</strong>: gasto que pode ser adiado ou evitado (viagem, roupa nova, celular mais moderno).</p>"},
            {"id_tarefa":3, "tipo":"texto", "conteudo":"<h3>Exemplos</h3><ul><li><strong>Necessidade:</strong> pagar aluguel.</li><li><strong>Desejo:</strong> comprar tênis novo porque está na moda.</li></ul>"},
            {"id_tarefa":3, "tipo":"quiz",  "pergunta":"Comprar comida é:", "alternativas":"Desejo||Necessidade", "correta":2},
            {"id_tarefa":3, "tipo":"quiz",  "pergunta":"Comprar um celular de última geração é:", "alternativas":"Necessidade||Desejo", "correta":2},

            # ===== Mini-aula 4 — Criando um Orçamento (id_tarefa = 4) =====
            {"id_tarefa":4, "tipo":"texto", "conteudo":"<h3>Passo a passo</h3><ol><li>Liste todas as receitas do mês.</li><li>Liste todas as despesas.</li><li>Subtraia as despesas das receitas.</li><li>Se sobrar dinheiro → guardar uma parte.</li><li>Se faltar dinheiro → cortar despesas desnecessárias.</li></ol>"},
            {"id_tarefa":4, "tipo":"texto", "conteudo":"<h3>Exemplo</h3><p><strong>Receita:</strong> R$ 2.000</p><p><strong>Despesa:</strong> R$ 1.500</p><p><strong>Sobra:</strong> R$ 500 → guardar R$ 200 e usar R$ 300 para lazer.</p>"},
            {"id_tarefa":4, "tipo":"quiz",  "pergunta":"No orçamento, se as despesas forem maiores que a receita:", "alternativas":"Está sobrando dinheiro||Está faltando dinheiro", "correta":2},
            {"id_tarefa":4, "tipo":"quiz",  "pergunta":"Guardar parte do que sobra é:", "alternativas":"Desperdício||Uma boa prática financeira", "correta":2},

            # ===== Avaliação Final — Módulo 1 (id_tarefa = 5) =====
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Qual dos itens abaixo é uma receita?", "alternativas":"Conta de energia||Salário||Compra de mercado", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Qual das opções é uma despesa fixa?", "alternativas":"Aluguel||Ingresso de cinema||Presentes", "correta":1},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Registrar gastos ajuda a:", "alternativas":"Perder tempo||Controlar o dinheiro||Gastar mais", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Necessidade é:", "alternativas":"Algo essencial||Algo supérfluo||Algo divertido", "correta":1},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Se a receita for de R$ 2.000 e a despesa R$ 2.500, a pessoa está:", "alternativas":"Economizando||Endividando||Investindo", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Comprar comida é:", "alternativas":"Desejo||Necessidade||Desperdício", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Comprar roupas de marca todo mês é:", "alternativas":"Necessidade||Desejo||Receita", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"No orçamento, o primeiro passo é:", "alternativas":"Listar receitas||Listar desejos||Listar compras do mês", "correta":1},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Se sobra dinheiro no fim do mês, o ideal é:", "alternativas":"Gastar tudo||Guardar uma parte||Esconder", "correta":2},
            {"id_tarefa":5, "tipo":"quiz", "pergunta":"Uma boa prática para melhorar o orçamento é:", "alternativas":"Cortar despesas desnecessárias||Comprar mais||Não anotar nada", "correta":1}
        ]

        for conteudo in conteudos_novos:
            valor = conteudo.get("conteudo") or conteudo.get("pergunta")
            if valor not in conteudo_existente:
                novo = ConteudoTarefa(**conteudo)
                db.session.add(novo)

        db.session.commit()