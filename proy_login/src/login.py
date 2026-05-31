class ErrorAcceso(Exception):
    """Excepción base del sistema"""
    pass


class UsuarioInvalido(ErrorAcceso):
    """Error de usuario inválido"""
    pass


class PasswordInvalido(ErrorAcceso):
    """Error de contraseña inválida"""
    pass


class UsuarioBloqueado(ErrorAcceso):
    """Error de usuario bloqueado"""
    pass


class Usuario:
    def __init__(self, username: str, password: str, activo: bool = True) -> None:
        if not username or not isinstance(username, str):
            raise UsuarioInvalido("Nombre de usuario inválido")

        if not password or not isinstance(password, str):
            raise PasswordInvalido("Contraseña inválida")

        self.username = username
        self.password = password
        self.activo = activo
        self.intentos = 0

    def login(self, username: str, password: str) -> bool:
        if not self.activo:
            raise UsuarioBloqueado("Usuario bloqueado")

        if username != self.username:
            raise UsuarioInvalido("Usuario incorrecto")

        if password != self.password:
            self.intentos += 1

            if self.intentos >= 3:
                self.activo = False
                raise UsuarioBloqueado("Usuario bloqueado por intentos fallidos")

            raise PasswordInvalido("Contraseña incorrecta")

        self.intentos = 0
        return True
