class ErrorCajero(Exception):
    """Excepción base del cajero"""
    pass


class FondosInsuficientes(ErrorCajero):
    """Error por saldo insuficiente"""
    pass


class MontoInvalido(ErrorCajero):
    """Error por monto inválido"""
    pass



class CuentaBancaria:
    def __init__(self, saldo: float) -> None:

        if not isinstance(saldo, (int, float)):
            raise MontoInvalido("El saldo debe ser numérico")

        if saldo < 0:
            raise MontoInvalido("El saldo no puede ser negativo")

        self.saldo = saldo

    def retirar(self, monto: float) -> bool:

        if not isinstance(monto, (int, float)):
            raise MontoInvalido("El monto debe ser numérico")

        if monto <= 0:
            raise MontoInvalido("El monto debe ser mayor a cero")

        if monto > 5000:
            raise MontoInvalido("El retiro excede el límite permitido")

        if monto > self.saldo:
            raise FondosInsuficientes("Fondos insuficientes")

        self.saldo -= monto
        return True

    def consultar_saldo(self) -> float:
        return self.saldo
    