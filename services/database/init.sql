-- Script de inicialización de base de datos
-- Sistema de Generación de PDFs

-- Eliminar tablas si existen (útil para desarrollo)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS system_settings CASCADE;
DROP TABLE IF EXISTS document_queue CASCADE;
DROP TABLE IF EXISTS generated_documents CASCADE;
DROP TABLE IF EXISTS template_signature_config CASCADE;
DROP TABLE IF EXISTS template_permissions CASCADE;
DROP TABLE IF EXISTS template_variables CASCADE;
DROP TABLE IF EXISTS template_resources CASCADE;
DROP TABLE IF EXISTS template_versions CASCADE;
DROP TABLE IF EXISTS templates CASCADE;
DROP TABLE IF EXISTS template_categories CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Crear secuencias para IDs
CREATE SEQUENCE seq_user_id START 1;
CREATE SEQUENCE seq_role_id START 1;
CREATE SEQUENCE seq_api_key_id START 1;
CREATE SEQUENCE seq_category_id START 1;
CREATE SEQUENCE seq_template_id START 1;
CREATE SEQUENCE seq_version_id START 1;
CREATE SEQUENCE seq_resource_id START 1;
CREATE SEQUENCE seq_variable_id START 1;
CREATE SEQUENCE seq_permission_id START 1;
CREATE SEQUENCE seq_config_id START 1;
CREATE SEQUENCE seq_document_id START 1;
CREATE SEQUENCE seq_queue_id START 1;
CREATE SEQUENCE seq_setting_id START 1;
CREATE SEQUENCE seq_log_id START 1;

-- Gestión de Usuarios y Seguridad
CREATE TABLE users (
    user_id BIGINT DEFAULT nextval('seq_user_id') PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    role_id BIGINT DEFAULT nextval('seq_role_id') PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT true NOT NULL
);

CREATE TABLE user_roles (
    user_id BIGINT REFERENCES users(user_id),
    role_id BIGINT REFERENCES roles(role_id),
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE api_keys (
    api_key_id BIGINT DEFAULT nextval('seq_api_key_id') PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) NOT NULL,
    key_value VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT true NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Gestión de Plantillas
CREATE TABLE template_categories (
    category_id BIGINT DEFAULT nextval('seq_category_id') PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT true NOT NULL
);

CREATE TABLE templates (
    template_id BIGINT DEFAULT nextval('seq_template_id') PRIMARY KEY,
    category_id BIGINT REFERENCES template_categories(category_id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_by BIGINT REFERENCES users(user_id) NOT NULL,
    updated_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE template_versions (
    version_id BIGINT DEFAULT nextval('seq_version_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL,
    version_number INTEGER NOT NULL,
    content JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_by BIGINT REFERENCES users(user_id) NOT NULL,
    updated_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(template_id, version_number)
);

CREATE TABLE template_resources (
    resource_id BIGINT DEFAULT nextval('seq_resource_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_path VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    size_bytes INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE template_variables (
    variable_id BIGINT DEFAULT nextval('seq_variable_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL,
    name VARCHAR(50) NOT NULL,
    default_value VARCHAR(255),
    required BOOLEAN DEFAULT false NOT NULL,
    variable_type VARCHAR(50) NOT NULL,
    validation_rules JSONB
);

CREATE TABLE template_permissions (
    permission_id BIGINT DEFAULT nextval('seq_permission_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL,
    role_id BIGINT REFERENCES roles(role_id) NOT NULL,
    can_view BOOLEAN DEFAULT false NOT NULL,
    can_edit BOOLEAN DEFAULT false NOT NULL,
    can_generate BOOLEAN DEFAULT false NOT NULL
);

CREATE TABLE template_signature_config (
    config_id BIGINT DEFAULT nextval('seq_config_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL UNIQUE,
    signature_count INTEGER DEFAULT 0 NOT NULL,
    coordinates_json JSONB,
    require_sequential BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Gestión de Documentos
CREATE TABLE generated_documents (
    document_id BIGINT DEFAULT nextval('seq_document_id') PRIMARY KEY,
    template_id BIGINT REFERENCES templates(template_id) NOT NULL,
    version_id BIGINT REFERENCES template_versions(version_id) NOT NULL,
    generated_by BIGINT REFERENCES users(user_id) NOT NULL,
    variables_json JSONB NOT NULL,
    status VARCHAR(50) NOT NULL,
    output_path VARCHAR(255),
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_queue (
    queue_id BIGINT DEFAULT nextval('seq_queue_id') PRIMARY KEY,
    document_id BIGINT REFERENCES generated_documents(document_id) NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0 NOT NULL,
    next_retry TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Configuración y Auditoría
CREATE TABLE system_settings (
    setting_id BIGINT DEFAULT nextval('seq_setting_id') PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NOT NULL,
    value_type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    log_id BIGINT DEFAULT nextval('seq_log_id') PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    details_json JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_template_versions_template_id ON template_versions(template_id);
CREATE INDEX idx_template_resources_template_id ON template_resources(template_id);
CREATE INDEX idx_template_variables_template_id ON template_variables(template_id);
CREATE INDEX idx_generated_documents_template_id ON generated_documents(template_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);

-- Datos iniciales
-- Rol de administrador
INSERT INTO roles (role_id, name, description, is_active)
VALUES (nextval('seq_role_id'), 'ADMIN', 'Administrador del sistema', true);

-- Usuario administrador por defecto
-- Password: Admin123! (hash generado con werkzeug.security.generate_password_hash)
INSERT INTO users (
    user_id,
    username,
    email,
    password_hash,
    is_active
) VALUES (
    nextval('seq_user_id'),
    'admin',
    'admin@templates.com',
    '{{ el hash generado por el script }}',
    true
);

-- Asignar rol de administrador al usuario
INSERT INTO user_roles (user_id, role_id, assigned_at)
SELECT
    (SELECT user_id FROM users WHERE username = 'admin'),
    (SELECT role_id FROM roles WHERE name = 'ADMIN'),
    CURRENT_TIMESTAMP;

-- API Key para el usuario administrador
INSERT INTO api_keys (
    api_key_id,
    user_id,
    key_value,
    description,
    is_active
) VALUES (
    nextval('seq_api_key_id'),
    (SELECT user_id FROM users WHERE username = 'admin'),
    'admin-dev-key-2024',
    'API Key de desarrollo para administrador',
    true
);