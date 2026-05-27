class ErrorBiblioteca(Exception):
    """Clase base para excepciones personalizadas de la biblioteca"""
    pass


class ErrorLibroInvalido(ErrorBiblioteca):
    """Excepción para operaciones con libros inválidos"""
    pass


class ErrorUsuarioInvalido(ErrorBiblioteca):
    """Excepción para operaciones con usuarios inválidos"""
    pass


class ErrorPrestamo(ErrorBiblioteca):
    """Excepción para errores en préstamos"""
    pass


class ErrorDevolucion(ErrorBiblioteca):
    """Excepción para errores en devoluciones"""
    pass


class Libro:
    def __init__(self, titulo, autor, isbn, copias_disponibles=1):
        if not titulo or not isinstance(titulo, str):
            raise ErrorLibroInvalido("El título del libro es inválido")
        if not autor or not isinstance(autor, str):
            raise ErrorLibroInvalido("El autor del libro es inválido")
        if not isbn or not isinstance(isbn, str):
            raise ErrorLibroInvalido("El ISBN del libro es inválido")
        if not isinstance(copias_disponibles, int) or copias_disponibles < 0:
            raise ErrorLibroInvalido("Las copias disponibles deben ser un número entero positivo")

        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.copias_disponibles = copias_disponibles

    def prestar(self):
        if self.copias_disponibles > 0:
            self.copias_disponibles -= 1
            return True
        raise ErrorPrestamo("No hay copias disponibles para préstamo")

    def devolver(self):
        self.copias_disponibles += 1


class Usuario:
    def __init__(self, id_usuario, nombre):
        if not id_usuario or not isinstance(id_usuario, str):
            raise ErrorUsuarioInvalido("El ID de usuario es inválido")
        if not nombre or not isinstance(nombre, str):
            raise ErrorUsuarioInvalido("El nombre de usuario es inválido")

        self.id_usuario = id_usuario
        self.nombre = nombre
        self.libros_prestados = []

    def tomar_prestado(self, libro):
        if not isinstance(libro, Libro):
            raise ErrorLibroInvalido("El objeto proporcionado no es un libro válido")

        if libro.prestar():
            self.libros_prestados.append(libro.titulo)
            return True
        return False

    def devolver_libro(self, libro):
        if not isinstance(libro, Libro):
            raise ErrorLibroInvalido("El objeto proporcionado no es un libro válido")

        if libro.titulo not in self.libros_prestados:
            raise ErrorDevolucion("El usuario no tiene prestado este libro")

        libro.devolver()
        self.libros_prestados.remove(libro.titulo)
        return True


class Biblioteca:
    def __init__(self):
        self.catalogo = []
        self.usuarios = []

    def agregar_libro(self, libro):
        if not isinstance(libro, Libro):
            raise ErrorLibroInvalido("Solo se pueden agregar objetos de tipo Libro")
        self.catalogo.append(libro)

    def registrar_usuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ErrorUsuarioInvalido("Solo se pueden registrar objetos de tipo Usuario")

        for u in self.usuarios:
            if u.id_usuario == usuario.id_usuario:
                raise ErrorUsuarioInvalido("Ya existe un usuario con este ID")

        self.usuarios.append(usuario)

    def buscar_libro(self, titulo):
        if not titulo or not isinstance(titulo, str):
            raise ErrorLibroInvalido("El título de búsqueda es inválido")

        for libro in self.catalogo:
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def prestar_libro(self, id_usuario, titulo_libro):
        try:
            if not id_usuario or not isinstance(id_usuario, str):
                raise ErrorUsuarioInvalido("ID de usuario inválido")
            if not titulo_libro or not isinstance(titulo_libro, str):
                raise ErrorLibroInvalido("Título de libro inválido")

            usuario = None
            for u in self.usuarios:
                if u.id_usuario == id_usuario:
                    usuario = u
                    break

            if not usuario:
                raise ErrorUsuarioInvalido("Usuario no encontrado")

            libro = self.buscar_libro(titulo_libro)
            if not libro:
                raise ErrorLibroInvalido("Libro no encontrado")

            return usuario.tomar_prestado(libro)
        except ErrorPrestamo as e:
            raise e
