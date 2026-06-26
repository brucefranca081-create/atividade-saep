CREATE DATABASE saep_estoque;

USE saep_estoque;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

SHOW TABLES;
DESCRIBE produtos;
SELECT * FROM produtos;
