-- Table pessoas
CREATE TABLE pessoas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255),
    cpf NUMERIC(11),
    data_nasc DATE,
    endereco VARCHAR(255),
    sexo VARCHAR(50),
    nome_social VARCHAR(255) DEFAULT 'NONE',
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table secretarias
CREATE TABLE secretarias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50),
    criado_em DATETIME,
    modificado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_em DATETIME,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table alunos
CREATE TABLE alunos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ra VARCHAR(50),
    status BOOLEAN DEFAULT TRUE,
    id_pessoa INT,
    id_secretaria INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table professores
CREATE TABLE professores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status BOOLEAN,
    id_pessoa INT,
    id_secretaria INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table inscricoes
CREATE TABLE inscricoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status BOOLEAN,
    id_aluno INT,
    id_secretaria INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table cursos
CREATE TABLE cursos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50),
    descricao TEXT,
    id_secretaria INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table turmas
CREATE TABLE turmas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50),
    descricao TEXT,
    capacidade INT,
    data_inicio DATE,
    data_fim DATE,
    id_curso INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table turmas_professores
CREATE TABLE turmas_professores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_inicio DATE,
    data_fim DATE,
    id_professor INT,
    id_turma INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table matriculas
CREATE TABLE matriculas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_inicio DATE,
    data_fim DATE,
    id_turma INT,
    id_inscricao INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table planos
CREATE TABLE planos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE,
    conteudo VARCHAR(255),
    id_turma INT,
    criado_em DATETIME,
    modificado_em DATETIME,
    deletado_em DATETIME,
    criado_por INT,
    modificado_por INT,
    deletado_por INT,
    ativo_flag BOOLEAN DEFAULT TRUE
);

-- Table faltas
CREATE TABLE faltas (
	id INT PRIMARY KEY AUTO_INCREMENT,
	falta BOOLEAN DEFAULT TRUE,
	justificativa VARCHAR(255),
	id_plano INT,
	id_matricula INT,
	criado_em DATETIME,
	modificado_em DATETIME,
    deletado_em DATETIME,
	criado_por INT,
    deletado_por INT,
    modificado_por INT,
	CONSTRAINT fk_falta_plano_id FOREIGN KEY (id_plano) REFERENCES planos(id),
	CONSTRAINT fk_falta_matricula_id FOREIGN KEY (id_matricula) REFERENCES matriculas(id)
);