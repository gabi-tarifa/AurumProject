-- Criação do banco de dados
CREATE DATABASE Aurum;
USE Aurum;

-- Tabela de usuários
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha CHAR(16) NOT NULL,
    data_cadastro DATE NOT NULL,
    CHECK (LENGTH(senha) BETWEEN 6 AND 16)
);

-- Tabela de módulos
CREATE TABLE Modulo (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- Tabela de tarefas
CREATE TABLE Tarefa (
    id_tarefa INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo INT NOT NULL,
    descricao TEXT NOT NULL,
    pontos INT NOT NULL,
    FOREIGN KEY (id_modulo) REFERENCES Modulo(id_modulo)
);

-- Tabela de tarefas realizadas pelo usuário
CREATE TABLE TarefaUsuario (
    id_tarefa_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_tarefa INT NOT NULL,
    data_conclusao DATE NOT NULL,
    pontuacao_obtida INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_tarefa) REFERENCES Tarefa(id_tarefa)
);

-- Tabela de premiações
CREATE TABLE Premiacao (
    id_premiacao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo ENUM('modulo_concluido', 'dias_consecutivos', 'ranking_top5') NOT NULL
);

-- Premiações conquistadas por usuários
CREATE TABLE PremiacaoUsuario (
    id_premiacao_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_premiacao INT NOT NULL,
    data_conquista DATE NOT NULL,
    referencia VARCHAR(255), -- Ex: nome do módulo, n° de dias, etc.
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_premiacao) REFERENCES Premiacao(id_premiacao)
);

-- Ranking semanal
CREATE TABLE RankingSemanal (
    id_ranking INT AUTO_INCREMENT PRIMARY KEY,
    semana_inicio DATE NOT NULL,
    semana_fim DATE NOT NULL
);

-- Pontuação dos usuários no ranking semanal
CREATE TABLE RankingUsuario (
    id_ranking_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_ranking INT NOT NULL,
    id_usuario INT NOT NULL,
    pontuacao_total INT NOT NULL,
    posicao INT NOT NULL,
    FOREIGN KEY (id_ranking) REFERENCES RankingSemanal(id_ranking),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

ALTER TABLE Usuario
ADD COLUMN pontos INT NOT NULL DEFAULT 0,
ADD COLUMN profilepicture VARCHAR(255) NOT NULL DEFAULT 'https://cdn-icons-png.flaticon.com/256/149/149071.png';

DELIMITER //

CREATE PROCEDURE CalcularRankingSemanal(IN data_inicio DATE, IN data_fim DATE)
BEGIN
    DECLARE id_rank INT;

    -- Cria novo ranking semanal
    INSERT INTO RankingSemanal (semana_inicio, semana_fim)
    VALUES (data_inicio, data_fim);

    -- Pega o ID do ranking recém-criado
    SET id_rank = LAST_INSERT_ID();

    -- Calcula pontuação total dos usuários na semana e insere no ranking
    INSERT INTO RankingUsuario (id_ranking, id_usuario, pontuacao_total, posicao)
    SELECT
        id_rank,
        tu.id_usuario,
        SUM(tu.pontuacao_obtida) AS total_pontos,
        RANK() OVER (ORDER BY SUM(tu.pontuacao_obtida) DESC) AS posicao
    FROM TarefaUsuario tu
    WHERE tu.data_conclusao BETWEEN data_inicio AND data_fim
    GROUP BY tu.id_usuario;

    -- Premia os top 5 usuários
    INSERT INTO PremiacaoUsuario (id_usuario, id_premiacao, data_conquista, referencia)
    SELECT
        ru.id_usuario,
        p.id_premiacao,
        CURRENT_DATE,
        CONCAT('Ranking semanal ', DATE_FORMAT(data_inicio, '%d/%m'), ' a ', DATE_FORMAT(data_fim, '%d/%m'))
    FROM RankingUsuario ru
    JOIN Premiacao p ON p.tipo = 'ranking_top5'
    WHERE ru.id_ranking = id_rank AND ru.posicao <= 5;
END //

DELIMITER ;

CALL CalcularRankingSemanal('2025-05-20', '2025-05-26');

INSERT INTO Premiacao (nome, descricao, tipo)
VALUES ('Top 5 semanal', 'Premiação para os 5 primeiros colocados no ranking da semana.', 'ranking_top5');

DELIMITER //

CREATE PROCEDURE PremiarDiasConsecutivos(IN dias_alvo INT)
BEGIN
    DECLARE hoje DATE;
    SET hoje = CURRENT_DATE;

    -- Premiação necessária
    DECLARE premiacao_id INT;
    SELECT id_premiacao INTO premiacao_id
    FROM Premiacao
    WHERE tipo = 'dias_consecutivos'
    LIMIT 1;

    -- CTE para obter dias consecutivos por usuário
    WITH DiasAtividade AS (
        SELECT DISTINCT id_usuario, data_conclusao
        FROM TarefaUsuario
        WHERE data_conclusao BETWEEN DATE_SUB(hoje, INTERVAL dias_alvo DAY) AND hoje
    ),
    Sequencias AS (
        SELECT
            id_usuario,
            data_conclusao,
            ROW_NUMBER() OVER (PARTITION BY id_usuario ORDER BY data_conclusao) AS ordem
        FROM DiasAtividade
    ),
    Agrupados AS (
        SELECT
            id_usuario,
            DATE_SUB(data_conclusao, INTERVAL ordem DAY) AS grupo,
            COUNT(*) AS dias_seguidos
        FROM Sequencias
        GROUP BY id_usuario, grupo
    )
    -- Insere premiação se atingiu o número de dias consecutivos
    INSERT INTO PremiacaoUsuario (id_usuario, id_premiacao, data_conquista, referencia)
    SELECT
        a.id_usuario,
        premiacao_id,
        CURDATE(),
        CONCAT(dias_alvo, ' dias consecutivos')
    FROM Agrupados a
    WHERE a.dias_seguidos >= dias_alvo
      AND NOT EXISTS (
        SELECT 1 FROM PremiacaoUsuario pu
        WHERE pu.id_usuario = a.id_usuario
          AND pu.id_premiacao = premiacao_id
          AND pu.referencia = CONCAT(dias_alvo, ' dias consecutivos')
    );
END //

DELIMITER ;

CALL PremiarDiasConsecutivos(7);

DELIMITER //

CREATE PROCEDURE PremiarModuloConcluido()
BEGIN
    DECLARE premiacao_id INT;

    SELECT id_premiacao INTO premiacao_id
    FROM Premiacao
    WHERE tipo = 'modulo_concluido'
    LIMIT 1;

    -- Lista de módulos com tarefas concluídas por usuário
    INSERT INTO PremiacaoUsuario (id_usuario, id_premiacao, data_conquista, referencia)
    SELECT
        tu.id_usuario,
        premiacao_id,
        CURRENT_DATE,
        CONCAT('Módulo: ', m.nome)
    FROM Modulo m
    JOIN Tarefa t ON t.id_modulo = m.id_modulo
    JOIN TarefaUsuario tu ON tu.id_tarefa = t.id_tarefa
    GROUP BY tu.id_usuario, m.id_modulo
    HAVING COUNT(DISTINCT t.id_tarefa) = (
        SELECT COUNT(*) FROM Tarefa WHERE id_modulo = m.id_modulo
    )
    AND NOT EXISTS (
        SELECT 1 FROM PremiacaoUsuario pu
        WHERE pu.id_usuario = tu.id_usuario
          AND pu.id_premiacao = premiacao_id
          AND pu.referencia = CONCAT('Módulo: ', m.nome)
    );
END //

DELIMITER ;

CALL PremiarModuloConcluido();

-- Dias consecutivos
INSERT IGNORE INTO Premiacao (nome, descricao, tipo)
VALUES ('Dias consecutivos', 'Fez tarefas por vários dias seguidos', 'dias_consecutivos');

-- Módulo concluído
INSERT IGNORE INTO Premiacao (nome, descricao, tipo)
VALUES ('Módulo concluído', 'Completou todas as tarefas de um módulo', 'modulo_concluido');
