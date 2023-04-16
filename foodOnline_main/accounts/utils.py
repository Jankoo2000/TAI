def detectUser(user):
    if user.role == 1:
        return 'vendorDashboard'
    elif user.role == 2:
        return 'custDashboard'
    elif user.role == None or user.is_admin:
        return '/admin'

"""„/site” odnosi się do katalogu głównego katalogu lub lokalizacji „site”. 
    Nie ma końcowego ukośnika, a adres URL wskazuje określony zasób lub plik w katalogu głównym katalogu „site”.

    „/site/” odnosi się do tej samej lokalizacji co „/site”, ale z końcowym ukośnikiem. Jest to zwykle używane do 
    wskazania, że URL wskazuje katalog lub zbiór zasobów, a nie konkretny zasób lub plik."""