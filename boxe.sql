-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 07 juin 2023 à 01:56
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `boxe`
--

-- --------------------------------------------------------

--
-- Structure de la table `boxeurs`
--

CREATE TABLE `boxeurs` (
  `id` int(11) NOT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `categorie` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `boxeurs`
--

INSERT INTO `boxeurs` (`id`, `nom`, `prenom`, `categorie`) VALUES
(1, 'Mike', 'Tyson', 'lourds'),
(2, 'Muhammad', 'Ali', 'lourds'),
(3, 'Floyd', 'Mayweather', 'mi-moyen'),
(4, 'Manny', 'Pacquiao', 'mi-moyen'),
(5, 'Vasyl', 'Lomachenko', 'lÃ©gers'),
(6, 'Gennady', 'Golovkin', 'mi-lourds');

-- --------------------------------------------------------

--
-- Structure de la table `combats`
--

CREATE TABLE `combats` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `boxeur1_id` int(11) DEFAULT NULL,
  `boxeur2_id` int(11) DEFAULT NULL,
  `categorie` varchar(255) DEFAULT NULL,
  `lieu` varchar(255) DEFAULT NULL,
  `points1` int(11) DEFAULT NULL,
  `points2` int(11) DEFAULT NULL,
  `winner_id` int(11) DEFAULT NULL,
  `win_method` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `combats`
--

INSERT INTO `combats` (`id`, `date`, `boxeur1_id`, `boxeur2_id`, `categorie`, `lieu`, `points1`, `points2`, `winner_id`, `win_method`) VALUES
(1, '2025-05-05', 1, 2, 'lourds', 'Paris', NULL, NULL, 1, 'KO');

-- --------------------------------------------------------

--
-- Structure de la table `juge`
--

CREATE TABLE `juge` (
  `id` int(11) NOT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `juge`
--

INSERT INTO `juge` (`id`, `nom`, `prenom`) VALUES
(1, 'Robert', 'Byrd'),
(2, 'Kenny', 'Bayless'),
(3, 'Tony', 'Weeks');

-- --------------------------------------------------------

--
-- Structure de la table `score`
--

CREATE TABLE `score` (
  `id_score` int(11) NOT NULL,
  `juge_id` int(11) DEFAULT NULL,
  `combat_id` int(11) DEFAULT NULL,
  `round_number` int(11) DEFAULT NULL,
  `score_boxer1` int(11) DEFAULT NULL,
  `score_boxer2` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `score`
--

INSERT INTO `score` (`id_score`, `juge_id`, `combat_id`, `round_number`, `score_boxer1`, `score_boxer2`) VALUES
(5, 1, 1, 1, 1, 1),
(6, 1, 1, 1, 1, 1),
(7, 1, 1, 1, 1, 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `boxeurs`
--
ALTER TABLE `boxeurs`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `combats`
--
ALTER TABLE `combats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `boxeur1_id` (`boxeur1_id`),
  ADD KEY `boxeur2_id` (`boxeur2_id`);

--
-- Index pour la table `juge`
--
ALTER TABLE `juge`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`id_score`),
  ADD KEY `juge_id` (`juge_id`),
  ADD KEY `combat_id` (`combat_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `boxeurs`
--
ALTER TABLE `boxeurs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `combats`
--
ALTER TABLE `combats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `juge`
--
ALTER TABLE `juge`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `score`
--
ALTER TABLE `score`
  MODIFY `id_score` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `combats`
--
ALTER TABLE `combats`
  ADD CONSTRAINT `combats_ibfk_1` FOREIGN KEY (`boxeur1_id`) REFERENCES `boxeurs` (`id`),
  ADD CONSTRAINT `combats_ibfk_2` FOREIGN KEY (`boxeur2_id`) REFERENCES `boxeurs` (`id`);

--
-- Contraintes pour la table `score`
--
ALTER TABLE `score`
  ADD CONSTRAINT `score_ibfk_1` FOREIGN KEY (`juge_id`) REFERENCES `juge` (`id`),
  ADD CONSTRAINT `score_ibfk_2` FOREIGN KEY (`combat_id`) REFERENCES `combats` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
