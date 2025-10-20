# chatbot/tools.py
from apps.assets.models import Asset
from apps.loans.models import Loan
from apps.maintenance.models import Maintenance

def get_available_assets():
    """
    Consulta la base de datos para obtener una lista de activos disponibles.

    Returns:
        list: Una lista de nombres de activos cuyo estado es 'disponible'.
              Devuelve una lista vacía si ocurre un error.
    """
    try:
        activos = Asset.objects.filter(status='disponible')
        return [asset.name for asset in activos]
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return []

def count_assets_by_status(status: str):
    """
    Cuenta el número de activos que se encuentran en un estado específico.

    Args:
        status (str): El estado a consultar (ej: 'en uso', 'mantenimiento').
                      Es flexible y normaliza algunas variaciones comunes.

    Returns:
        int: El número de activos en el estado especificado.
             Devuelve 0 si no se proporciona un estado o si ocurre un error.
    """
    if not status:
        return 0
    try:
        # Mapea sinónimos o variaciones del estado a los valores exactos de la BD.
        status_map = {
            "mantenimiento": "En mantenimiento",
            "en mantenimiento": "En mantenimiento",
            "uso": "En uso",
            "en uso": "En uso",
            "disponible": "Disponible",
            "disponibles": "Disponible",
        }
        normalized_status = status_map.get(status.lower(), status)

        count = Asset.objects.filter(status=normalized_status).count()
        return count
    except Exception as e:
        print(f"Error al contar activos por estado: {e}")
        return 0

def get_most_recent_loan():
    """
    Busca en la base de datos el último préstamo registrado.

    Returns:
        dict: Un diccionario con información clave del préstamo más reciente
              (activo, usuario, fecha).
              Devuelve None si no hay préstamos o si ocurre un error.
    """
    try:
        recent_loan = Loan.objects.order_by('-loan_date').first()
        if recent_loan:
            return {
                "asset": recent_loan.asset.name,
                "user": recent_loan.user.username,
                "date": recent_loan.loan_date.strftime("%d/%m/%Y"),
            }
        else:
            return None
    except Exception as e:
        print(f"Error al buscar el préstamo más reciente: {e}")
        return None

def create_maintenance_request(asset_identifier: str, description: str):
    """
    Crea un nuevo registro de mantenimiento para un activo específico.

    Busca un activo por su ID (si el identificador es numérico) o por su nombre
    (si es una cadena de texto). Si lo encuentra, crea una solicitud de
    mantenimiento y actualiza el estado del activo a 'En mantenimiento'.

    Args:
        asset_identifier (str): El ID o el nombre exacto del activo.
        description (str): La descripción del problema o solicitud.

    Returns:
        int: El ID de la solicitud de mantenimiento creada.
             Devuelve None si el activo no se encuentra o si ocurre un error.
    """
    try:
        if asset_identifier.isdigit():
            # Si el identificador es numérico, búscalo por ID.
            asset = Asset.objects.get(pk=int(asset_identifier))
        else:
            # Si no, búscalo por nombre (ignorando mayúsculas/minúsculas).
            asset = Asset.objects.get(name__iexact=asset_identifier)
        
        maintenance = Maintenance.objects.create(
            asset=asset,
            description=description,
            status='pendiente'  # El estado inicial de toda nueva solicitud.
        )
        # Actualiza el estado del activo para reflejar que está en mantenimiento.
        asset.status = 'En mantenimiento'
        asset.save()
        return maintenance.id
    except (Asset.DoesNotExist, ValueError):
        print(f"Error al crear mantenimiento: No se encontró el activo '{asset_identifier}'")
        return None
    except Exception as e:
        print(f"Error al crear la solicitud de mantenimiento: {e}")
        return None