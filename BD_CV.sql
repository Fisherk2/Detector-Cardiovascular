-- Creacion de base de datos.

CREATE DATABASE Cardiovascular
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE Cardiovascular;
   
-- Creacion de tabla donde se almacena la informacion del usuario.

#DELETE FROM usuario;
#ALTER TABLE usuario AUTO_INCREMENT = 1;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    age MEDIUMINT NOT NULL,				-- Age | Objective Feature | age | int (days)
    gender BIT(2) NOT NULL,				-- Gender | Objective Feature | gender | categorical code (1 - women, 2 - men) |
    height SMALLINT NOT NULL,			-- Height | Objective Feature | height | int (cm) |
    weight SMALLINT NOT NULL,			-- Weight | Objective Feature | weight | float (kg) |
    smoke BIT NOT NULL,					-- Smoking | Subjective Feature | smoke | binary |
    alco BIT NOT NULL,					-- Alcohol intake | Subjective Feature | alco | binary |
    active BIT NOT NULL					-- Physical activity | Subjective Feature | active | binary |
);

-- Creacion de tabla donde se almacena los registros del usuario.
          
CREATE TABLE register (
	fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de registro
    id_usuario INT NOT NULL,
    ap_hi SMALLINT NOT NULL, 		-- Systolic blood pressure | Examination Feature | ap_hi | int |
    ap_lo SMALLINT NOT NULL, 		-- Diastolic blood pressure | Examination Feature | ap_lo | int |
    cholesterol BIT(2) NOT NULL,	-- Cholesterol | Examination Feature | cholesterol | 1: normal, 2: above normal, 3: well above normal |
    gluc BIT(2) NOT NULL,			-- Glucose | Examination Feature | gluc | 1: normal, 2: above normal, 3: well above normal |
	CONSTRAINT FK_usuarioID FOREIGN KEY (id_usuario)
    REFERENCES usuario(id)
    ON DELETE CASCADE
);

#DROP TABLE register;
              
-- Creamos index de busqueda para registro

CREATE INDEX idx_usuario
ON register (id_usuario); 

-- Creacion de usuario CRUD (Para toda la base de datos)
   
CREATE USER 'adminCV'@'localhost' IDENTIFIED BY 'admin123';
GRANT SELECT, INSERT, UPDATE, DELETE ON Cardiovascular.* TO 'adminCV'@'localhost';
FLUSH PRIVILEGES;

-- Creacion de usuario solo escritura y lectura (Para la tabla register)
#CREATE USER 'registerCV'@'localhost' IDENTIFIED BY 'register123';
#GRANT SELECT, INSERT ON Cardiovascular.register TO 'registerCV'@'localhost';
#FLUSH PRIVILEGES;

-- Creacion de usuario solo escritura (Para la tabla usuarios)
#CREATE USER 'userCV'@'localhost' IDENTIFIED BY 'user123';
#GRANT SELECT ON Cardiovascular.usuario TO 'userCV'@'localhost';
#FLUSH PRIVILEGES;

-- Registros de ejemplo
INSERT INTO usuario (name, age, gender, height, weight, smoke, alco, active) 
VALUES ('Fisher', 9861, 2, 176, 85, 0, 0, 0);

#TRUNCATE TABLE register;

INSERT INTO register (id_usuario, ap_hi, ap_lo, cholesterol, gluc)
VALUES (1, 120, 80, 1, 1);  -- Usuario 1, valores normales

#(1, 120, 80, 1, 1);  -- Usuario 1, valores normales
#(1, 130, 85, 2, 1);  -- Usuario 1, colesterol por encima de lo normal
#(1, 140, 90, 3, 2);  -- Usuario 1, colesterol muy alto, glucosa alta
#(1, 110, 70, 1, 1);  -- Usuario 1, valores normales
#(1, 150, 95, 3, 3);  -- Usuario 1, valores muy altos de colesterol y glucosa
#(1, 125, 80, 2, 2);  -- Usuario 1, colesterol alto y glucosa alta
#(1, 135, 88, 2, 1);  -- Usuario 1, colesterol alto
#(1, 145, 92, 3, 2);  -- Usuario 1, colesterol y glucosa altos
#(1, 118, 75, 1, 1);  -- Usuario 1, valores normales
#(1, 160, 100, 3, 3); -- Usuario 1, valores muy altos de todo







