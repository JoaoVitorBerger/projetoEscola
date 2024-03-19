-- Inserindo secretarias
INSERT INTO secretarias (nome) VALUES ('Secretaria de Educação');
INSERT INTO secretarias (nome) VALUES ('Secretaria de Saúde');
INSERT INTO secretarias (nome) VALUES ('Secretaria de Cultura');

-- Inserindo pessoas
INSERT INTO pessoas (nome, cpf, data_nasc, endereco, sexo) VALUES ('João da Silva', 12345678901, '1990-01-01', 'Rua A, 123', 'Masculino');
INSERT INTO pessoas (nome, cpf, data_nasc, endereco, sexo) VALUES ('Maria Oliveira', 98765432109, '1985-05-15', 'Avenida B, 456', 'Feminino');
INSERT INTO pessoas (nome, cpf, data_nasc, endereco, sexo) VALUES ('José Santos', 45678912345, '1978-11-30', 'Praça C, 789', 'Masculino');

-- Inserindo alunos
INSERT INTO alunos (ra, status, id_pessoa, id_secretaria) VALUES ('123456', TRUE, 1, 1);
INSERT INTO alunos (ra, status, id_pessoa, id_secretaria) VALUES ('654321', TRUE, 2, 2);
INSERT INTO alunos (ra, status, id_pessoa, id_secretaria) VALUES ('987654', TRUE, 3, 3);

-- Inserindo professores
INSERT INTO professores (status, id_pessoa, id_secretaria) VALUES (TRUE, 1, 1);
INSERT INTO professores (status, id_pessoa, id_secretaria) VALUES (TRUE, 2, 2);
INSERT INTO professores (status, id_pessoa, id_secretaria) VALUES (TRUE, 3, 3);

-- Inserindo cursos
INSERT INTO cursos (nome, descricao, id_secretaria) VALUES ('Matemática', 'Curso de Matemática', 1);
INSERT INTO cursos (nome, descricao, id_secretaria) VALUES ('Português', 'Curso de Português', 2);
INSERT INTO cursos (nome, descricao, id_secretaria) VALUES ('História', 'Curso de História', 3);

-- Inserindo turmas
INSERT INTO turmas (nome, descricao, capacidade, data_inicio, data_fim, id_curso) VALUES ('Turma A', 'Turma de Matemática', 30, '2024-03-01', '2024-06-30', 1);
INSERT INTO turmas (nome, descricao, capacidade, data_inicio, data_fim, id_curso) VALUES ('Turma B', 'Turma de Português', 25, '2024-03-01', '2024-06-30', 2);
INSERT INTO turmas (nome, descricao, capacidade, data_inicio, data_fim, id_curso) VALUES ('Turma C', 'Turma de História', 20, '2024-03-01', '2024-06-30', 3);

-- Inserindo turmas_professores
INSERT INTO turmas_professores (data_inicio, data_fim, id_professor, id_turma) VALUES ('2024-03-01', '2024-06-30', 1, 1);
INSERT INTO turmas_professores (data_inicio, data_fim, id_professor, id_turma) VALUES ('2024-03-01', '2024-06-30', 2, 2);
INSERT INTO turmas_professores (data_inicio, data_fim, id_professor, id_turma) VALUES ('2024-03-01', '2024-06-30', 3, 3);

-- Inserindo inscricoes
INSERT INTO inscricoes (status, id_aluno, id_secretaria) VALUES (TRUE, 1, 1);
INSERT INTO inscricoes (status, id_aluno, id_secretaria) VALUES (TRUE, 2, 2);
INSERT INTO inscricoes (status, id_aluno, id_secretaria) VALUES (TRUE, 3, 3);

-- Inserindo matriculas
INSERT INTO matriculas (data_inicio, data_fim, id_turma, id_inscricao) VALUES ('2024-03-01', '2024-06-30', 1, 1);
INSERT INTO matriculas (data_inicio, data_fim, id_turma, id_inscricao) VALUES ('2024-03-01', '2024-06-30', 2, 2);
INSERT INTO matriculas (data_inicio, data_fim, id_turma, id_inscricao) VALUES ('2024-03-01', '2024-06-30', 3, 3);

-- Inserindo planos
INSERT INTO planos (data, conteudo, id_turma) VALUES ('2024-03-01', 'Plano de Matemática', 1);
INSERT INTO planos (data, conteudo, id_turma) VALUES ('2024-03-01', 'Plano de Português', 2);
INSERT INTO planos (data, conteudo, id_turma) VALUES ('2024-03-01', 'Plano de História', 3);

-- Inserindo faltas
INSERT INTO faltas (falta, id_plano, id_matricula) VALUES (TRUE, 1, 1);
INSERT INTO faltas (falta, id_plano, id_matricula) VALUES (TRUE, 2, 2);
INSERT INTO faltas (falta, justificativa, id_plano, id_matricula) VALUES (FALSE, 'Falta justificada', 3, 3);
