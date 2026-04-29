from configparser import ConfigParser
import psycopg2
from psycopg2.extensions import connection as Connection
from typing import Any

class ConexionDB:
    def __init__(self, host: str, database: str, user: str, password: str, port: int = 5432) -> None:
        """
        Inicializa los parámetros de conexión.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn: Connection | None = None

    # ----------------------------
    # Conexión
    # ----------------------------
    def abrir_conexion(self) -> None:
        """
        Abre la conexión a la base de datos.
        """
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise e

    def cerrar_conexion(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        if self.conn is not None:
            self.conn.close()
            print("Conexión cerrada.")
        else:
            print("No hay conexión abierta.")

    def _validar_conexion(self) -> None:
        """
        Verifica que la conexión esté abierta.
        """
        if self.conn is None:
            raise RuntimeError("La conexión no está abierta. Llama a abrir_conexion() primero.")

    # ----------------------------
    # CRUD
    # ----------------------------
    def insertar_empleado(
        self,
        id_empleado: int,
        nombre: str,
        fecha_nacimiento: str,
        puesto: int,
        sueldo: float
    ) -> None:
        """
        Inserta un empleado en la base de datos.
        """
        self._validar_conexion()
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO empleados (id, nombre, fecha_nacimiento, puesto, sueldo) VALUES (%s, %s, %s, %s, %s)",
                (id_empleado, nombre, fecha_nacimiento, puesto, sueldo)
            )
            self.conn.commit()
            print(f"Empleado {nombre} insertado correctamente.")
            cur.close()
        except Exception as e:
            self.conn.rollback()
            print(f"Error al insertar empleado: {e}")
            raise e

    def actualizar_sueldo(
        self,
        id_empleado: int,
        nuevo_sueldo: float
    ) -> None:
        """
        Actualiza el sueldo de un empleado.
        """
        self._validar_conexion()
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE empleados SET sueldo = %s WHERE id = %s",
                (nuevo_sueldo, id_empleado)
            )
            self.conn.commit()
            print(f"Sueldo del empleado {id_empleado} actualizado a {nuevo_sueldo}.")
            cur.close()
        except Exception as e:
            self.conn.rollback()
            print(f"Error al actualizar sueldo: {e}")
            raise e

    def eliminar_empleado(self, id_empleado: int) -> None:
        """
        Elimina un empleado por ID.
        """
        self._validar_conexion()
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM empleados WHERE id = %s", (id_empleado,))
            self.conn.commit()
            print(f"Empleado {id_empleado} eliminado correctamente.")
            cur.close()
        except Exception as e:
            self.conn.rollback()
            print(f"Error al eliminar empleado: {e}")
            raise e

    def consultar_empleados(self) -> list[tuple]:
        """
        Retorna una lista de empleados.
        """
        self._validar_conexion()
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM empleados")
            empleados = cur.fetchall()
            cur.close()
            return empleados
        except Exception as e:
            print(f"Error al consultar empleados: {e}")
            raise e

