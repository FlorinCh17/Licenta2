from blockchain import Blockchain
from wallet import Wallet

def populate_identity_dict(private_key, nume, data_nasterii, cnp, cazier, nationalitate):
    identity = {
        "name": nume,
        "date_of_b": data_nasterii,
        "CNP": cnp,
        "criminal_records": cazier,
        "nationality": nationalitate,
    }

    if private_key not in Blockchain.Identity_dict:
        Blockchain.Identity_dict[private_key] = []

    Blockchain.Identity_dict[private_key].append(identity)

        # Salvăm datele actualizate
    Blockchain.save_data(Blockchain.Identity_dict, "identity_data.json")

# Exemple de utilizare:
private_key = Wallet.generatePrivateKey()
nume = "Popescu Ion"
data_nasterii = "1975-01-05"
cnp = "76372856391"
cazier = "clean"
nationalitate = "romanian"

populate_identity_dict(private_key, nume, data_nasterii, cnp, cazier, nationalitate)

private_key = Wallet.generatePrivateKey()
nume = "Jane Doe"
data_nasterii = "1980-01-01"
cnp = "12349878923"
cazier = "curat"
nationalitate = "maghiar"

populate_identity_dict(private_key, nume, data_nasterii, cnp, cazier, nationalitate)






print(Blockchain.Identity_dict)