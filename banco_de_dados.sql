CREATE DATABASE IF NOT EXISTS sistema_consultas;

USE sistema_consultas;

CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    telefone VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade VARCHAR(50),
    horario_atendimento VARCHAR(50) NOT NULL COMMENT 'Formato: HH:MM HH:MM'
);

CREATE TABLE IF NOT EXISTS consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    data_consulta DATETIME,
    motivo TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'medico', 'atendente') NOT NULL
);

-- Primeiro remova a foreign key existente
ALTER TABLE consultas 
DROP FOREIGN KEY consultas_ibfk_1;

-- Adicione a nova foreign key com DELETE CASCADE
ALTER TABLE consultas
ADD CONSTRAINT consultas_ibfk_1 
FOREIGN KEY (paciente_id) 
REFERENCES pacientes(id)
ON DELETE CASCADE;

-- Faça o mesmo para a foreign key do médico
ALTER TABLE consultas 
DROP FOREIGN KEY consultas_ibfk_2;

ALTER TABLE consultas
ADD CONSTRAINT consultas_ibfk_2 
FOREIGN KEY (medico_id) 
REFERENCES medicos(id)
ON DELETE CASCADE;
