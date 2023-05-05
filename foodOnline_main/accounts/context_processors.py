from foodOnline_main import settings
from vendor.models import Vendor

"""
Context processor w Django działa jako funkcja, która dodaje zmienne do kontekstu dla wszystkich szablonów w aplikacji Django. 
Są to zmienne, które mają być dostępne dla wszystkich szablonów w aplikacji.
Aby utworzyć procesor kontekstu, należy utworzyć funkcję, która zwraca słownik z danymi, które mają być dodane do kontekstu
"""
def get_vendor(request): # 60, 61
    try:
        vendor = Vendor.objects.get(user=request.user) # w sytacji gdy jestesmy zalogowani
    except:
        vendor = None
    return dict(vendor=vendor)  # vendor=vendor oznacza, że klucz w słowniku będzie miał nazwę vendor, a wartość
                                # będzie zmienną vendor. Innymi słowy, tworzymy słownik, który ma tylko jeden klucz vendor i jego wartość jest
                                # przypisana do zmiennej vendor.


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID' : settings.PAYPAL_CLIENT_ID}