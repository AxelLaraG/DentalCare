


CREATE TABLE `tratamientos` (
    `id_tratamiento` INT(11) NOT NULL AUTO_INCREMENT,  -- Clave primaria
    `id_usuario` INT(11) NOT NULL,  -- Clave foránea hacia la tabla 'usuarios'
    `nombre_tratamiento` VARCHAR(255) NOT NULL,  -- Nombre del tratamiento
    `fecha_inicio` DATE NOT NULL,  -- Fecha de inicio del tratamiento
    `ultima_actualizacion` DATE DEFAULT CURRENT_DATE,  -- Última actualización (fecha actual por defecto)
    PRIMARY KEY (`id_tratamiento`),  -- Definir la clave primaria
    FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id`) ON DELETE CASCADE  -- Relación con 'usuarios'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `detalles_tratamiento` (
    `id_detalle` INT(11) NOT NULL AUTO_INCREMENT,  -- Clave primaria
    `id_tratamiento` INT(11) NOT NULL,  -- Clave foránea hacia la tabla 'tratamientos'
    `id_dentista` INT(11) NOT NULL,  -- Clave foránea hacia la tabla 'dentistas'
    `descripcion_tratamiento` VARCHAR(255) NOT NULL,  -- Descripción del tratamiento realizado
    `fecha_detalle` DATE NOT NULL,  -- Fecha en la que se realizó el detalle del tratamiento
    PRIMARY KEY (`id_detalle`),  -- Definir la clave primaria
    FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamientos`(`id_tratamiento`) ON DELETE CASCADE,  -- Relación con 'tratamientos'
    FOREIGN KEY (`id_dentista`) REFERENCES `dentistas`(`id`) ON DELETE CASCADE  -- Relación con 'dentistas'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


