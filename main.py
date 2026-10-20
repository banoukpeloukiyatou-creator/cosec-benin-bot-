from database import creer_base
import os

# Ça installe la base automatiquement au démarrage si elle n'existe pas
if not os.path.exists("cosec_microfinance.db"):
    creer_base()
    print("Base COSEC installée avec succès au démarrage !")