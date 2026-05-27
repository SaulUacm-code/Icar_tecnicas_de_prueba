import pytest

from src.biblioteca import (
    Biblioteca,
    ErrorDevolucion,
    ErrorLibroInvalido,
    ErrorPrestamo,
    ErrorUsuarioInvalido,
    Libro,
    Usuario,
)


def test_crear_libro_valido():
    libro = Libro("Python", "Guido", "PY-1", 2)

    assert libro.titulo == "Python"
    assert libro.autor == "Guido"
    assert libro.isbn == "PY-1"
    assert libro.copias_disponibles == 2


@pytest.mark.parametrize(
    ("titulo", "autor", "isbn", "copias", "mensaje"),
    [
        ("", "Guido", "PY-1", 1, "El título del libro es inválido"),
        ("Python", "", "PY-1", 1, "El autor del libro es inválido"),
        ("Python", "Guido", "", 1, "El ISBN del libro es inválido"),
        ("Python", "Guido", "PY-1", -1, "Las copias disponibles deben ser un número entero positivo"),
    ],
)
def test_libro_invalido_lanza_excepcion(titulo, autor, isbn, copias, mensaje):
    with pytest.raises(ErrorLibroInvalido, match=mensaje):
        Libro(titulo, autor, isbn, copias)


def test_usuario_y_prestamo_exitoso():
    libro = Libro("Test", "Autor", "T-1", 1)
    usuario = Usuario("U1", "Ana")

    assert usuario.tomar_prestado(libro) is True
    assert usuario.libros_prestados == ["Test"]
    assert libro.copias_disponibles == 0


def test_prestamo_sin_copias_lanza_excepcion():
    libro = Libro("Sin stock", "Autor", "S-1", 0)
    usuario = Usuario("U2", "Luis")

    with pytest.raises(ErrorPrestamo, match="No hay copias disponibles para préstamo"):
        usuario.tomar_prestado(libro)


def test_devolver_libro_y_error_si_no_lo_tiene():
    libro = Libro("Devuelto", "Autor", "D-1", 1)
    usuario = Usuario("U3", "Mara")

    usuario.tomar_prestado(libro)
    assert usuario.devolver_libro(libro) is True
    assert libro.copias_disponibles == 1

    with pytest.raises(ErrorDevolucion, match="no tiene prestado este libro"):
        usuario.devolver_libro(libro)


def test_biblioteca_registra_y_busca_libros():
    biblioteca = Biblioteca()
    libro = Libro("Algoritmos", "Autor", "A-1", 1)
    usuario = Usuario("U4", "Pablo")

    biblioteca.agregar_libro(libro)
    biblioteca.registrar_usuario(usuario)

    assert biblioteca.buscar_libro("algoritmos") is libro
    assert biblioteca.buscar_libro("No existe") is None


def test_prestar_libro_valida_usuarios_y_libros():
    biblioteca = Biblioteca()
    libro = Libro("Patrones", "Autor", "P-1", 1)
    usuario = Usuario("U5", "Sofi")

    biblioteca.agregar_libro(libro)
    biblioteca.registrar_usuario(usuario)

    assert biblioteca.prestar_libro("U5", "Patrones") is True

    with pytest.raises(ErrorUsuarioInvalido, match="ID de usuario inválido"):
        biblioteca.prestar_libro("", "Patrones")

    with pytest.raises(ErrorLibroInvalido, match="Título de libro inválido"):
        biblioteca.prestar_libro("U5", "")

    with pytest.raises(ErrorUsuarioInvalido, match="Usuario no encontrado"):
        biblioteca.prestar_libro("ZZZ", "Patrones")

    with pytest.raises(ErrorLibroInvalido, match="Libro no encontrado"):
        biblioteca.prestar_libro("U5", "Inexistente")
