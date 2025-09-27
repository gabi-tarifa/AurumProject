def criar_conteudo():
    from app import app, db
    from models import ConteudoTarefa
    with app.app_context():
        conteudo_existente = {c.conteudo or c.pergunta for c in ConteudoTarefa.query.all()}

        conteudos_novos = [
                # MINI-AULA 1 — Receita e Despesa
                {"numero_tarefa":1, "id_modulo":1, "tipo":"texto", "conteudo":"<h3>Receita e Despesa</h3><p><strong>Receita</strong> é todo dinheiro que entra no seu bolso (salário, mesada, bônus, venda de produtos).</p><p><strong>Despesa</strong> é todo dinheiro que sai (contas fixas, lazer, compras, transporte).</p><p><em>Dica:</em> Pense em entrada e saída. Se o dinheiro entra → receita. Se sai → despesa.</p><p><strong>Exemplo:</strong> Você recebe R$ 2.000 (receita). Paga R$ 800 de aluguel, R$ 200 de luz e R$ 200 de transporte (despesas). Sobra R$ 800 para poupar ou gastar com lazer.</p>"},

                {"numero_tarefa":1, "id_modulo":1, "tipo":"quiz", "pergunta":"O que melhor define uma receita?", "alternativas":"Valor gasto em contas fixas||Entrada de dinheiro no orçamento||Dívida contraída com o banco||Redução de despesas no mês", "correta":2},
                {"numero_tarefa":1, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual das situações representa uma despesa?", "alternativas":"Receber comissão de vendas||Pagar mensalidade da academia||Vender um objeto usado||Guardar dinheiro na poupança", "correta":2},
                {"numero_tarefa":1, "id_modulo":1, "tipo":"quiz", "pergunta":"Ao pagar o aluguel, o que ocorre no orçamento?", "alternativas":"Aumenta a receita||Surge uma nova dívida||Há uma saída de dinheiro||O saldo total não se altera", "correta":3},
                {"numero_tarefa":1, "id_modulo":1, "tipo":"quiz", "pergunta":"Uma pessoa recebe R$ 2.000 e gasta R$ 1.800. Seu saldo final é:", "alternativas":"Superávit de R$ 1.800||Déficit de R$ 200||Sobra de R$ 200||Nenhuma alteração no orçamento", "correta":3},
                {"numero_tarefa":1, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual opção é um exemplo de receita extra?", "alternativas":"Conta de energia atrasada||Bônus salarial inesperado||Compra parcelada de eletrodoméstico||Pagamento do cartão de crédito", "correta":2},


                # MINI-AULA 2 — Como Registrar Gastos
                {"numero_tarefa":2, "id_modulo":1, "tipo":"texto", "conteudo":"<h3>Como Registrar Gastos</h3><p>Registrar gastos é como tirar uma foto das suas finanças. Sem esse controle, você não sabe para onde seu dinheiro vai.</p><p>Pode ser feito em papel, planilha ou aplicativo gratuito.</p><p>É importante registrar tanto receitas quanto despesas, até as pequenas.</p><table><tr><th>Data</th><th>Descrição</th><th>Tipo</th><th>Valor</th></tr><tr><td>05/08</td><td>Conta de luz</td><td>Despesa</td><td>R$120</td></tr><tr><td>07/08</td><td>Salário</td><td>Receita</td><td>R$1500</td></tr><tr><td>09/08</td><td>Cinema</td><td>Despesa</td><td>R$40</td></tr></table>"},

                {"numero_tarefa":2, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual é o principal motivo para registrar gastos?", "alternativas":"Descobrir para onde o dinheiro está indo||Garantir aumento automático da receita||Reduzir o valor das despesas fixas||Evitar ter de pagar impostos", "correta":1},
                {"numero_tarefa":2, "id_modulo":1, "tipo":"quiz", "pergunta":"Onde é possível registrar gastos de forma eficiente?", "alternativas":"Somente em aplicativos pagos||Em papel, planilha ou aplicativos gratuitos||Apenas em relatórios bancários||Guardando tudo de memória", "correta":2},
                {"numero_tarefa":2, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual risco surge ao não registrar seus gastos?", "alternativas":"Aumentar automaticamente a receita||Ter sempre saldo positivo||Esquecer compromissos financeiros||Reduzir o número de despesas", "correta":3},
                {"numero_tarefa":2, "id_modulo":1, "tipo":"quiz", "pergunta":"Uma vantagem clara de anotar despesas é:", "alternativas":"Saber se o dinheiro está indo para necessidades ou desejos||Facilitar a aprovação de crédito no banco||Evitar receber salário em espécie||Aumentar artificialmente a renda mensal", "correta":1},
                {"numero_tarefa":2, "id_modulo":1, "tipo":"quiz", "pergunta":"Se alguém gasta R$ 50 em lazer e não registra, o que pode acontecer?", "alternativas":"O valor é transformado em receita||O gasto pode ser esquecido||O dinheiro retorna ao saldo||O gasto é automaticamente classificado como fixo", "correta":2},


                # MINI-AULA 3 — Necessidade vs. Desejo
                {"numero_tarefa":3, "id_modulo":1, "tipo":"texto", "conteudo":"<h3>Necessidade vs. Desejo</h3><p><strong>Necessidade:</strong> gastos que você não pode deixar de pagar (alimentação, moradia, transporte, saúde).</p><p><strong>Desejo:</strong> gastos que trazem prazer, mas podem ser adiados ou evitados (roupas de marca, viagens, eletrônicos novos).</p><p><em>Dica:</em> Antes de gastar, pergunte: “Eu realmente preciso disso agora?”</p>"},

                {"numero_tarefa":3, "id_modulo":1, "tipo":"quiz", "pergunta":"Comprar alimentos básicos é um exemplo de:", "alternativas":"Gasto opcional||Necessidade||Desperdício financeiro||Investimento de longo prazo", "correta":2},
                {"numero_tarefa":3, "id_modulo":1, "tipo":"quiz", "pergunta":"Trocar de celular mesmo com o antigo funcionando é:", "alternativas":"Atualização necessária||Desejo||Receita variável||Despesa obrigatória", "correta":2},
                {"numero_tarefa":3, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual opção representa uma necessidade essencial?", "alternativas":"Moradia (aluguel ou prestação)||Ingresso de cinema||Viagem internacional||Novo console de videogame", "correta":1},
                {"numero_tarefa":3, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual dos gastos abaixo é claramente um desejo?", "alternativas":"Plano de saúde||Sapato de marca||Conta de água||Transporte para o trabalho", "correta":2},
                {"numero_tarefa":3, "id_modulo":1, "tipo":"quiz", "pergunta":"Por que diferenciar necessidade de desejo é tão importante?", "alternativas":"Para saber o limite do cartão||Para priorizar o que garante sobrevivência||Para gastar sempre mais em lazer||Para não precisar economizar", "correta":2},


                # MINI-AULA 4 — Criando um Orçamento
                {"numero_tarefa":4, "id_modulo":1, "tipo":"texto", "conteudo":"<h3>Criando um Orçamento</h3><p>Um orçamento é um mapa do seu dinheiro.</p><p>Primeiro, liste receitas.</p><p>Depois, anote todas as despesas.</p><p>Subtraia despesas das receitas para saber se sobra ou falta.</p><p>Se sobrar → guarde uma parte.</p><p>Se faltar → corte gastos desnecessários.</p><p><strong>Exemplo:</strong><br>Receita: R$ 2.000<br>Despesas: R$ 1.500<br>Saldo: R$ 500<br>Decisão: guardar R$ 200 e usar R$ 300 para lazer.</p>"},

                {"numero_tarefa":4, "id_modulo":1, "tipo":"quiz", "pergunta":"Se suas despesas superam suas receitas, o que significa?", "alternativas":"Você tem sobra de dinheiro||O orçamento está em déficit||As finanças estão equilibradas||Não há impacto no saldo final", "correta":2},
                {"numero_tarefa":4, "id_modulo":1, "tipo":"quiz", "pergunta":"Guardar parte do dinheiro que sobra é considerado:", "alternativas":"Uma prática saudável de finanças pessoais||Obrigação legal||Endividamento futuro||Desperdício de capital", "correta":1},
                {"numero_tarefa":4, "id_modulo":1, "tipo":"quiz", "pergunta":"Se alguém ganha R$ 1.000 e gasta exatamente R$ 1.000, o saldo é:", "alternativas":"Equilíbrio, sem sobra nem déficit||Déficit de R$ 1.000||Superávit de R$ 1.000||Saldo positivo de R$ 500", "correta":1},
                {"numero_tarefa":4, "id_modulo":1, "tipo":"quiz", "pergunta":"Qual é a melhor atitude quando sobra dinheiro no mês?", "alternativas":"Usar tudo para lazer imediato||Reservar uma parte para poupança ou investimento||Antecipar novas dívidas||Adquirir bens por impulso", "correta":2},
                {"numero_tarefa":4, "id_modulo":1, "tipo":"quiz", "pergunta":"O que significa 'cortar despesas desnecessárias'?", "alternativas":"Eliminar gastos supérfluos||Reduzir a receita||Deixar de pagar contas fixas||Aumentar o limite do cartão de crédito", "correta":1}
        ]

        for conteudo in conteudos_novos:
            valor = conteudo.get("conteudo") or conteudo.get("pergunta")
            if valor not in conteudo_existente:
                novo = ConteudoTarefa(**conteudo)
                db.session.add(novo)

        db.session.commit()