from werkzeug.security import generate_password_hash

def generate_admin_password_hash(password="Admin123!"):
    """Genera el hash de la contraseña admin para el script SQL."""
    return generate_password_hash(password, method='pbkdf2:sha256')

if __name__ == "__main__":
    password = "Admin123!"
    hashed = generate_admin_password_hash(password)
    print(f"Hash para '{password}': {hashed}")

    # Generar SQL para actualizar el usuario
    sql = f"""
    UPDATE users
    SET password_hash = '{hashed}'
    WHERE username = 'admin';
    """
    print("\nSQL para actualizar usuario:")
    print(sql)