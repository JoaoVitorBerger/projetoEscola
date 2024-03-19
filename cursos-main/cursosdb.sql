CREATE TABLE secretarias (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(50),
	criado_em DATETIME,
	modificado_em DATETIME,
	criado_por INT,
	modificado_por INT,
	ativo_flag BOOLEAN DEFAULT TRUE
);

CREATE TABLE pessoas (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(255),
	cpf NUMERIC(11),
	data_nasc DATE,
	endereco VARCHAR(255),
	sexo VARCHAR(50),
	nome_social VARCHAR(255),
	criado_em DATETIME,
	modificado_em DATETIME,
	deletado_em DATETIME,
	criado_por INT,
	modificado_por INT,
	deletado_por INT,
	ativo_flag BOOLEAN DEFAULT TRUE
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_aluno_pessoa_id FOREIGN KEY (id_pessoa) REFERENCES pessoas(id),
	CONSTRAINT fk_aluno_secretaria_id FOREIGN KEY (id_secretaria) REFERENCES secretarias(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_professor_pessoa_id FOREIGN KEY (id_pessoa) REFERENCES pessoas(id),
	CONSTRAINT fk_professor_secretaria_id FOREIGN KEY (id_secretaria) REFERENCES secretarias(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_incricao_aluno_id FOREIGN KEY (id_aluno) REFERENCES alunos(id),
	CONSTRAINT fk_incricao_secretaria_id FOREIGN KEY (id_secretaria) REFERENCES secretarias(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_curso_secretaria_id FOREIGN KEY (id_secretaria) REFERENCES secretarias(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_turma_curso_id FOREIGN KEY (id_curso) REFERENCES cursos(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_turma_professor_id FOREIGN KEY (id_professor) REFERENCES professores(id),
	CONSTRAINT fk_turma_turma_id FOREIGN KEY (id_turma) REFERENCES turmas(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_matricula_turma_id FOREIGN KEY (id_turma) REFERENCES turmas(id),
	CONSTRAINT fk_matricula_inscricao_id FOREIGN KEY (id_inscricao) REFERENCES inscricoes(id)
);

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
	ativo_flag BOOLEAN DEFAULT TRUE,
	CONSTRAINT fk_plano_turma_id FOREIGN KEY (id_turma) REFERENCES turmas(id)
);

CREATE TABLE faltas (
	id INT PRIMARY KEY AUTO_INCREMENT,
	falta BOOLEAN DEFAULT TRUE,
	justificativa VARCHAR(255),
	id_plano INT,
	id_matricula INT,
	criado_em DATETIME,
	modificado_em DATETIME,
	criado_por INT,
	modificado_por INT,
	CONSTRAINT fk_falta_plano_id FOREIGN KEY (id_plano) REFERENCES planos(id),
	CONSTRAINT fk_falta_matricula_id FOREIGN KEY (id_matricula) REFERENCES matriculas(id)
);