import pytest

from src.login_Cajero import CuentaBancaria, MontoInvalido

from src.login import (
    PasswordInvalido,
    Usuario,
    UsuarioBloqueado,
    UsuarioInvalido,
)


def test_usuario_valido_se_crea_correctamente():
    usuario = Usuario("admin", "12345")

    assert usuario.username == "admin"
    assert usuario.password == "12345"
    assert usuario.activo is True
    assert usuario.intentos == 0

@pytest.mark.parametrize(
    ("username", "password", "mensaje"),
    [
        ("", "12345", "Nombre de usuario inválido"),
        ("admin", "", "Contraseña inválida"),
        (None, "12345", "Nombre de usuario inválido"),
        ("admin", None, "Contraseña inválida"),
    ],
)

def test_usuario_invalido_lanza_excepcion(username, password, mensaje):
    with pytest.raises((UsuarioInvalido, PasswordInvalido), match=mensaje):
        Usuario(username, password)

def test_login_exitoso_reinicia_intentos():
    usuario = Usuario("admin", "12345")

    assert usuario.login("admin", "12345") is True
    assert usuario.intentos == 0

def test_login_usuario_bloqueado():
    usuario = Usuario("admin", "12345", activo=False)
    with pytest.raises(UsuarioBloqueado, match="Usuario bloqueado"):
        usuario.login("admin", "12345")

def test_login_usuario_incorrecto():
    usuario = Usuario("admin", "12345")
    with pytest.raises(UsuarioInvalido, match="Usuario incorrecto"):
        usuario.login("user", "12345")

def test_login_con_password_incorrecto_aumenta_intentos_y_no_bloquea():
    usuario = Usuario("admin", "12345")

    with pytest.raises(PasswordInvalido, match="Contraseña incorrecta"):
        usuario.login("admin", "error")

    assert usuario.intentos == 1
    assert usuario.activo is True

def test_login_usuario_bloqueado_por_intentos_fallidos():
    usuario = Usuario("admin", "12345")

    with pytest.raises(PasswordInvalido, match="Contraseña incorrecta"):
        usuario.login("admin", "error1")
    with pytest.raises(PasswordInvalido, match="Contraseña incorrecta"):
        usuario.login("admin", "error2")
    with pytest.raises(UsuarioBloqueado, match="Usuario bloqueado por intentos fallidos"):
        usuario.login("admin", "error3")
    assert usuario.intentos == 3
    assert usuario.activo is False


#----------------------------------------------------------------------------------------
#Ejercicio 2

def test_saldo_debe_ser_numerico():
    with pytest.raises(MontoInvalido, match="El saldo debe ser numérico"):
        CuentaBancaria("mil")

def test_saldo_no_puede_ser_negativo():
    with pytest.raises(MontoInvalido, match="El saldo no puede ser negativo"):
        CuentaBancaria(-100)
    
