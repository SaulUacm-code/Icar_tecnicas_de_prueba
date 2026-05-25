import pytest

from src.usuarios import AutenticacionSimple, UsuarioYaExiste, UsuarioInvalido


def test_registrar_usuario_exitoso():
    auth = AutenticacionSimple()
    assert auth.registrar("usuario1", "password123") is True
    assert auth.usuarios["usuario1"] == "password123"


def test_registrar_usuario_existente_levanta_excepcion():
    auth = AutenticacionSimple()
    auth.registrar("usuario1", "password123")

    with pytest.raises(UsuarioYaExiste, match="ya está registrado"):
        auth.registrar("usuario1", "password123")


def test_registrar_usuario_invalido_tamano_corto():
    auth = AutenticacionSimple()

    with pytest.raises(UsuarioInvalido, match="al menos 5 caracteres"):
        auth.registrar("usr", "password123")


def test_registrar_usuario_invalido_caracteres():
    auth = AutenticacionSimple()

    with pytest.raises(UsuarioInvalido, match="solo puede contener letras y números"):
        auth.registrar("usuario!", "password123")


def test_registrar_password_demasiado_corta():
    auth = AutenticacionSimple()

    with pytest.raises(UsuarioInvalido, match="al menos 8 caracteres"):
        auth.registrar("usuario1", "pass")


def test_iniciar_sesion_exitoso():
    auth = AutenticacionSimple()
    auth.registrar("usuario1", "password123")
    assert auth.iniciar_sesion("usuario1", "password123") is True


def test_iniciar_sesion_usuario_no_registrado_levanta_excepcion():
    auth = AutenticacionSimple()

    with pytest.raises(UsuarioInvalido, match="no está registrado"):
        auth.iniciar_sesion("usuario1", "password123")


def test_iniciar_sesion_contraseña_incorrecta_levanta_excepcion():
    auth = AutenticacionSimple()
    auth.registrar("usuario1", "password123")

    with pytest.raises(UsuarioInvalido, match="contraseña es incorrecta"):
        auth.iniciar_sesion("usuario1", "wrongpass")
