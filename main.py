def main() -> None:
    # Crear instancia de conexión
    db = ConexionDB(
        host="localhost",
        database="empleados",
        user="uacm",
        password="uacm1",
        port=5432
    )

    # Conectar a la base de datos
    db.conectar()
    # ----------------------------
    # Insertar empleados (ID manual)
    # ----------------------------
    #db.insertar_empleado(1, "Juan Pérez", "1990-05-10", 1, 15000.50)
    #db.insertar_empleado(2, "Ana López", "1985-08-20", 2, 18000.75)
    # ----------------------------
    # Consultar empleados
    # ----------------------------
    #empleados = db.consultar_empleados()
    #for emp in empleados:
    #    print(emp)
    # ----------------------------