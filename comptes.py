# comptes.py - GÈRE PAIEMENT, ENCAISSEMENT, REMBOURSEMENT
import sqlite3
from datetime import datetime
import random

DB_NAME = "cosec_microfinance.db"

def generer_numero_recu(type_op):
    # RC-P = Paiement, RC-E = Encaissement, RC-R = Remboursement
    prefix = {"PAIEMENT":"RC-P", "ENCAISSEMENT":"RC-E", "REMBOURSEMENT":"RC-R"}[type_op]
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"

def operation_microfinance(compte_id, type_operation, montant, mode="ESPECES", agent_id=1):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 1. Récupère le compte
    cur.execute("SELECT solde_actuel, jours_payes FROM comptes_microfinance WHERE id=?", (compte_id,))
    compte = cur.fetchone()
    ancien_solde = compte[0]
    jours_payes = compte[1]

    # 2. Calcule nouveau solde
    if type_operation == "PAIEMENT": # Tontine journalière
        nouveau_solde = ancien_solde + montant
        nouveau_jours = jours_payes + 1
        cur.execute("UPDATE comptes_microfinance SET solde_actuel=?, jours_payes=? WHERE id=?", 
                    (nouveau_solde, nouveau_jours, compte_id))
    else: # ENCAISSEMENT ou REMBOURSEMENT
        nouveau_solde = ancien_solde + montant if type_operation=="ENCAISSEMENT" else ancien_solde - montant
        cur.execute("UPDATE comptes_microfinance SET solde_actuel=? WHERE id=?", 
                    (nouveau_solde, compte_id))

    # 3. Crée la transaction + reçu
    numero_recu = generer_numero_recu(type_operation)
    qr_code = f"cosec.bj/verify/{numero_recu}"
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO transactions (compte_id, type_operation, montant, numero_recu, ancien_solde, nouveau_solde, mode_paiement, agent_id, date_operation, qr_code)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (compte_id, type_operation, montant, numero_recu, ancien_solde, nouveau_solde, mode, agent_id, date_now, qr_code))

    transaction_id = cur.lastrowid
    conn.commit()
    conn.close()

    print(f"✅ {type_operation} de {montant}F - Reçu: {numero_recu}")
    
    # 4. ICI ON APPELLERA LA GÉNÉRATION DU REÇU PDF + WHATSAPP A,B,C
    # generer_pdf_et_envoyer_whatsapp(transaction_id, numero_recu)
    
    return numero_recu

# TEST RAPIDE
# operation_microfinance(compte_id=1, type_operation="PAIEMENT", montant=1000)
# operation_microfinance(compte_id=1, type_operation="ENCAISSEMENT", montant=50000)
# operation_microfinance(compte_id=1, type_operation="REMBOURSEMENT", montant=10000)