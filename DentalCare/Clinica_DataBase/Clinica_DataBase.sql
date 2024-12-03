-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-12-2024 a las 06:34:21
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `clinica`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citasmedicas`
--

CREATE TABLE `citasmedicas` (
  `id` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_dentista` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `estado` enum('pendiente','confirmada','cancelada') DEFAULT 'pendiente',
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citasmedicas`
--

INSERT INTO `citasmedicas` (`id`, `id_paciente`, `id_dentista`, `fecha`, `hora`, `motivo`, `estado`, `fecha_creacion`) VALUES
(6, 1, 3, '2024-12-01', '09:00:00', 'Consulta de rutina', 'pendiente', '2024-12-01 01:50:58'),
(7, 3, 1, '2024-12-02', '10:00:00', 'Limpieza dental', 'cancelada', '2024-12-01 01:50:58'),
(8, 4, 4, '2024-12-03', '11:00:00', 'Revisión de caries', 'pendiente', '2024-12-01 01:50:58'),
(9, 4, 1, '2024-12-04', '14:00:00', 'Extracción de muela', 'pendiente', '2024-12-01 01:50:58'),
(10, 5, 1, '2024-12-05', '14:00:00', 'Consulta ortodoncia', 'cancelada', '2024-12-01 01:50:58'),
(11, 3, 1, '2024-12-01', '09:00:00', 'Consulta de rutina', 'confirmada', '2024-12-01 10:23:19'),
(12, 5, 4, '2024-12-01', '18:00:00', 'Prueba', 'cancelada', '2024-12-01 15:48:23'),
(13, 2, 3, '2024-12-01', '19:00:00', 'Prueba', 'cancelada', '2024-12-01 15:51:31'),
(14, 4, 3, '2024-12-01', '18:00:00', 'Prueba', 'cancelada', '2024-12-01 17:33:07'),
(15, 5, 4, '2024-12-01', '18:00:00', 'Prueba', 'cancelada', '2024-12-01 17:35:46'),
(16, 2, 3, '2024-12-01', '19:00:00', 'Prueba', 'cancelada', '2024-12-01 17:37:34'),
(17, 2, 3, '2024-12-02', '10:00:00', 'Prueba', 'cancelada', '2024-12-01 18:39:41'),
(18, 3, 4, '2024-12-02', '10:00:00', 'Prueba', 'pendiente', '2024-12-01 18:40:11'),
(19, 1, 1, '2024-12-02', '10:00:00', 'Prueba', 'confirmada', '2024-12-01 19:01:41'),
(20, 2, 1, '2024-12-02', '12:00:00', 'Prueba', 'cancelada', '2024-12-01 19:46:04'),
(21, 5, 3, '2024-12-02', '12:00:00', 'Prueba', 'confirmada', '2024-12-01 19:46:31'),
(22, 4, 3, '2024-12-02', '10:00:00', 'Prueba', 'pendiente', '2024-12-01 19:47:28'),
(23, 4, 1, '2024-12-04', '14:00:00', 'Axel', 'cancelada', '2024-12-02 15:25:02');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dentistas`
--

CREATE TABLE `dentistas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contrasenia` varchar(100) DEFAULT NULL,
  `licencia` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `dentistas`
--

INSERT INTO `dentistas` (`id`, `nombre`, `apellido`, `edad`, `direccion`, `email`, `contrasenia`, `licencia`) VALUES
(1, 'nancy', 'chavez', 20, 'htrs', 'nancy@gmail.com', '1234', '123456'),
(3, 'prueba', 'prueba', 1, 'prueba', 'prueba', NULL, 'prueba'),
(4, 'A', 'B', 20, 'htrs', 'B@gmail.com', '1234', '123456'),
(5, 'Dentista', 'Dentista', 23, 'Dentista', 'Dentista', 'Dentista', 'Dentista');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `expedientes`
--

CREATE TABLE `expedientes` (
  `id` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `tratamiento_inicial` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id`, `nombre`, `apellido`, `fecha_nacimiento`, `telefono`, `correo`, `direccion`, `fecha_registro`) VALUES
(1, 'Juan', 'Perez', '1985-07-23', '5551234567', 'juan.perez@example.com', 'Calle 1, Ciudad', '2024-12-01 01:44:31'),
(2, 'Ana', 'Gomez', '1990-11-05', '5559876543', 'ana.gomez@example.com', 'Calle 2, Ciudad', '2024-12-01 01:44:31'),
(3, 'Luis', 'Lopez', '1978-03-15', '5558765432', 'luis.lopez@example.com', 'Calle 3, Ciudad', '2024-12-01 01:44:31'),
(4, 'Maria', 'Hernandez', '2000-01-10', '5557654321', 'maria.hernandez@example.com', 'Calle 4, Ciudad', '2024-12-01 01:44:31'),
(5, 'Carlos', 'Ramirez', '1995-06-25', '5556543210', 'carlos.ramirez@example.com', 'Calle 5, Ciudad', '2024-12-01 01:44:31'),
(8, 'A', 'B', '2024-01-01', '1234567890', 'D@algo.com', 'C', '2024-12-01 22:38:06'),
(9, 'Prueba', 'Prueba B', '2024-12-02', '1234567890', '1@algo.com', '1', '2024-12-02 22:45:24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progresotratamiento`
--

CREATE TABLE `progresotratamiento` (
  `id` int(11) NOT NULL,
  `id_tratamiento` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `progresotratamiento`
--

INSERT INTO `progresotratamiento` (`id`, `id_tratamiento`, `fecha`, `descripcion`) VALUES
(1, 1, '2024-12-02 22:36:32', 'D1'),
(2, 2, '2024-12-02 22:36:45', 'D2'),
(3, 3, '2024-12-02 22:37:01', 'D3');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tratamientos`
--

CREATE TABLE `tratamientos` (
  `id` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_realizacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tratamientos`
--

INSERT INTO `tratamientos` (`id`, `id_paciente`, `descripcion`, `fecha_realizacion`) VALUES
(1, 8, 'Prueba 1', '2024-12-02 22:36:32'),
(2, 8, 'Prueba 2', '2024-12-02 22:36:45'),
(3, 8, 'Prueba 3', '2024-12-02 22:37:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contrasenia` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `edad`, `direccion`, `email`, `contrasenia`) VALUES
(6, 'prueba', 'prueba', 1, 'prueba', 'l', 'fa'),
(8, 'Usuario', 'Usuario', 1, 'Usuario', 'Usuario', 'Usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `citasmedicas`
--
ALTER TABLE `citasmedicas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_paciente` (`id_paciente`),
  ADD KEY `id_dentista` (`id_dentista`);

--
-- Indices de la tabla `dentistas`
--
ALTER TABLE `dentistas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `expedientes`
--
ALTER TABLE `expedientes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_paciente` (`id_paciente`),
  ADD KEY `tratamiento_inicial` (`tratamiento_inicial`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `progresotratamiento`
--
ALTER TABLE `progresotratamiento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_tratamiento` (`id_tratamiento`);

--
-- Indices de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_paciente` (`id_paciente`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `citasmedicas`
--
ALTER TABLE `citasmedicas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `dentistas`
--
ALTER TABLE `dentistas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `expedientes`
--
ALTER TABLE `expedientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `progresotratamiento`
--
ALTER TABLE `progresotratamiento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citasmedicas`
--
ALTER TABLE `citasmedicas`
  ADD CONSTRAINT `CitasMedicas_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`),
  ADD CONSTRAINT `CitasMedicas_ibfk_2` FOREIGN KEY (`id_dentista`) REFERENCES `dentistas` (`id`);

--
-- Filtros para la tabla `expedientes`
--
ALTER TABLE `expedientes`
  ADD CONSTRAINT `Expedientes_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Expedientes_ibfk_2` FOREIGN KEY (`tratamiento_inicial`) REFERENCES `tratamientos` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `progresotratamiento`
--
ALTER TABLE `progresotratamiento`
  ADD CONSTRAINT `ProgresoTratamiento_ibfk_1` FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamientos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD CONSTRAINT `Tratamientos_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
