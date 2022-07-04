from datetime import datetime
import sys
import csv


def _verify_dni(dni):
    return dni.isdigit()


def _check_rango(rango):
    fechas = rango.split(":")
    try:
        datetime.strptime(fechas[0], '%d-%m-%Y')
        datetime.strptime(fechas[1], '%d-%m-%Y')
        return True
    except ValueError:
        return False


def _check_salida(salida):
    """Check if the output is a valid option"""
    if salida.upper() in ["PANTALLA", "CSV"]:
        return True
    else:
        print('Parametro invalido')
        exit


def _check_tipo(tipo):
    """Check if the type of output is correct"""
    if tipo.upper() in ["EMITIDO", "DEPOSITADO"]:
        return True
    else:
        print('Parametro invalido')
        exit


def _check_estado(estado):
    """Verify if the state is valid"""
    if estado.upper() in ["PENDIENTE", "APROBADO", "RECHAZADO"]:
        return True
    else:
        print('Parametro invalido')
        exit


def _check_estado(estado):
    """Verify if the state is valid"""
    if estado.upper() in ["PENDIENTE", "APROBADO", "RECHAZADO"]:
        return True
    else:
        print('Parametro invalido')
        exit


def _verify_parameters(parametros):

    if len(parametros) < 4:
        # if the user doesn't enter the parameters
        print("Faltan parametros")
        return False
    else:
        # if the user enters the parameters
        if not _verify_dni(parametros[1]) or not _check_salida(parametros[2]) or not _check_tipo(parametros[3]):
            return False
        match len(parametros):
            case 5:
                if not _check_estado(parametros[4]):
                    return False
            case 6:
                if not _check_estado(parametros[4]) and not _check_rango(parametros[5]):
                    return False
        return True


def _getting_data(archivo):
    """Open the CSV and return a list with the data"""
    try:
        with open(f"{archivo}.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            return list(reader)
    except FileNotFoundError:
        return None


def _searching_dni(data, dni, tipo, estado=None, rango=None):
    """Search the DNI in the list and add the coincidences to list"""
    cheques = [line for line in data if line[8] == dni and line[9] == tipo and (estado is None or line[10] == estado) and (rango is None or (datetime.strptime(
        line[11], '%d-%m-%Y') >= datetime.strptime(rango[0], '%d-%m-%Y') and datetime.strptime(line[11], '%d-%m-%Y') <= datetime.strptime(rango[1], '%d-%m-%Y')))]
    # Create a list with the chequesID
    cheques_id = [line[0] for line in cheques]
    if len(cheques_id) != len(set(cheques_id)):
        print("Hay cheques repetidos")
        return None
    return cheques


def __main__():
    parametros = sys.argv[1:]
    if _verify_parameters(parametros):
        data = _getting_data(parametros[0])
        if data is not None:
            match len(parametros):
                case 4:
                    cheques_dni = _searching_dni(
                        data, parametros[1], parametros[3])
                case 5:
                    cheques_dni = _searching_dni(
                        data, parametros[1], parametros[3], parametros[4])
                case 6:
                    cheques_dni = _searching_dni(
                        data, parametros[1], parametros[3], parametros[4], parametros[5])
            if cheques_dni is not None:
                if len(cheques_dni) == 0:
                    print("No se encontraron cheques")
                    return
                else:
                    if parametros[2].upper() == "PANTALLA":
                        for line in cheques_dni:
                            print(line)
                    elif parametros[2].upper() == "CSV":
                        with open(f"-{parametros[1]}-{int(datetime.timestamp(datetime.now()))}-.csv", 'w', newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(
                                ["FechaOrigen", "FechaPago", "Valor", "Cuenta"])
                            match parametros[3].upper():
                                case "EMITIDO":
                                    for line in cheques_dni:
                                        writer.writerow(
                                            [line[6], line[7], line[5], line[3]])
                                case "DEPOSITADO":
                                    for line in cheques_dni:
                                        writer.writerow(
                                            [line[6], line[7], line[5], line[4]])
                    else:
                        print("Parametro invalido")
                        return
        else:
            print("File not found")
            return


if __name__ == "__main__":
    __main__()
    exit()
