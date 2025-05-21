-- Tabla de Roles
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    nombreRol VARCHAR(50) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE, -- Se usa BOOLEAN en lugar de BIT
    rol_padre INT NULL,
    FOREIGN KEY (rol_padre) REFERENCES Roles(id) -- Eliminar ON DELETE para evitar ciclos
);

-- Tabla de Permisos
CREATE TABLE Permisos (
    id SERIAL PRIMARY KEY,
    nombrePermiso VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY,
    nombreUsuario VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    ci VARCHAR(20) UNIQUE NOT NULL, -- Ampliar para incluir identificaciones extranjeras
    tipo_identificacion VARCHAR(10) NOT NULL, -- 'Boliviano' o 'Extranjero'
    ci_departamento CHAR(2) DEFAULT 'EX', -- Abreviatura para bolivianos, 'EX' para extranjeros
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
    activo BOOLEAN DEFAULT TRUE,
    bloqueada BOOLEAN DEFAULT FALSE,
    imagen VARCHAR(255),
    imagen_url VARCHAR(500),
    correo_verificado BOOLEAN DEFAULT FALSE,
    intentos_fallidos INT DEFAULT 0,
    fecha_bloqueo TIMESTAMP NULL,
    fecha_recuperacion TIMESTAMP NULL,
    UNIQUE (ci)
);


-- Tabla de Notificaciones
CREATE TABLE Notificaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    tipo VARCHAR(50) NOT NULL, -- 'correo' o 'SMS'
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Tabla de Roles de Usuarios
CREATE TABLE UsuarioRoles (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    rol_id INT,
    UNIQUE (usuario_id, rol_id), -- Evitar duplicados
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES Roles(id) ON DELETE CASCADE
);

-- Tabla de Roles y Permisos
CREATE TABLE RolPermisos (
    id SERIAL PRIMARY KEY,
    rol_id INT,
    permiso_id INT,
    UNIQUE (rol_id, permiso_id), -- Evitar duplicados
    FOREIGN KEY (rol_id) REFERENCES Roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permiso_id) REFERENCES Permisos(id) ON DELETE CASCADE
);

-- Tabla de Registro de Actividades
CREATE TABLE RegistroActividades (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(255),
    fecha TIMESTAMP DEFAULT NOW(),
    detalles TEXT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Tabla de Sesiones (para control de sesiones activas)
CREATE TABLE Sesiones (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    token VARCHAR(255) UNIQUE NOT NULL, -- Token de sesión
    fecha_inicio TIMESTAMP DEFAULT NOW(),
    fecha_fin TIMESTAMP NULL, -- Para el cierre de sesión
    ip VARCHAR(45), -- Para guardar la IP del usuario
    activo BOOLEAN DEFAULT TRUE, -- Indica si la sesión está activa
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- Tabla de Revocaciones de Permisos (opcional)
CREATE TABLE Revocaciones (
    id SERIAL PRIMARY KEY,
    permiso_id INT,
    fecha_inicio TIMESTAMP DEFAULT NOW(),
    fecha_fin TIMESTAMP NULL, -- Fecha de finalización de la revocación
    FOREIGN KEY (permiso_id) REFERENCES Permisos(id) ON DELETE CASCADE
);
