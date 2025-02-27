-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Tempo de geração: 15-Fev-2025 às 00:01
-- Versão do servidor: 8.0.41
-- versão do PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "America/Sao_Paulo";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de dados: `express`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `data_clients`
--

CREATE TABLE `data_clients` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `cpf_cnpj` varchar(20) DEFAULT NULL,
  `address` text,
  `company_name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Estrutura da tabela `data_iot`
--

CREATE TABLE `data_iot` (
  `id` int NOT NULL,
  `hardware_id` int NOT NULL,
  `credit` int DEFAULT NULL,
  `salescounter` int DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `uptime` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Estrutura da tabela `link_device`
--

CREATE TABLE `link_device` (
  `id` int NOT NULL,
  `client_id` int NOT NULL,
  `hardware_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `authorized` tinyint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Estrutura da tabela `system_user`
--

CREATE TABLE `system_user` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` tinyint NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `data_clients`
--
ALTER TABLE `data_clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Índices para tabela `data_iot`
--
ALTER TABLE `data_iot`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hardware_id` (`hardware_id`);

--
-- Índices para tabela `link_device`
--
ALTER TABLE `link_device`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `hardware_id` (`hardware_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Índices para tabela `system_user`
--
ALTER TABLE `system_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `data_clients`
--
ALTER TABLE `data_clients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `data_iot`
--
ALTER TABLE `data_iot`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1101;

--
-- AUTO_INCREMENT de tabela `link_device`
--
ALTER TABLE `link_device`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de tabela `system_user`
--
ALTER TABLE `system_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `data_iot`
--
ALTER TABLE `data_iot`
  ADD CONSTRAINT `data_iot_ibfk_1` FOREIGN KEY (`hardware_id`) REFERENCES `link_device` (`hardware_id`) ON DELETE CASCADE;

--
-- Limitadores para a tabela `link_device`
--
ALTER TABLE `link_device`
  ADD CONSTRAINT `link_device_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `data_clients` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
