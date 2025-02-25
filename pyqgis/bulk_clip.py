import os
import geopandas as gpd


def orez_vrstvy(vstupni_adresar, resene_uzemi_path, vystupni_adresar, encoding="utf-8"):
    # Načteme vrstvu řešeného území (ReseneUzemi_p)
    resene_uzemi = gpd.read_file(resene_uzemi_path)

    # Projdeme všechny soubory v adresáři vstup
    for soubor in os.listdir(vstupni_adresar):
        # Zpracováváme pouze soubory s příponou .shp, vynecháme "ReseneUzemi_p.shp"
        if soubor.endswith(".shp") and soubor != os.path.basename(resene_uzemi_path):
            vstup_path = os.path.join(vstupni_adresar, soubor)

            try:
                # Načteme vstupní shapefile
                vstupni_vrstva = gpd.read_file(vstup_path)

                # Ověříme, zda vrstva zasahuje do řešeného území
                if vstupni_vrstva.intersects(resene_uzemi.unary_union).any():
                    # Ořízneme vrstvu podle řešeného území
                    orezana_vrstva = gpd.overlay(
                        vstupni_vrstva, resene_uzemi, how="intersection"
                    )

                    # Zachováme pouze atributy vstupní vrstvy, nikoliv ReseneUzemi_p
                    orezana_vrstva = orezana_vrstva[vstupni_vrstva.columns]

                    # Vytvoříme název pro výstupní soubor
                    vystup_file = os.path.join(vystupni_adresar, soubor)

                    # Uložíme oříznutou vrstvu s požadovaným kódováním
                    orezana_vrstva.to_file(vystup_file, encoding=encoding)
                    print(f"Vrstva {soubor} byla oříznuta a uložena do {vystup_file}")
                else:
                    print(f"Vrstva {soubor} nezasahuje do řešeného území, přeskočeno.")
            except Exception as e:
                print(f"Chyba při zpracování souboru {soubor}: {e}")
        else:
            if soubor.endswith(".shp"):
                print(f"Vrstva {soubor} je vrstva ReseneUzemi_p, přeskočeno.")
            else:
                print(f"Soubor {soubor} není shapefile, přeskočeno.")


# Příklad použití
# MacOS path format: /path/to/output_directory
# Windows path format: H:/path/to/output_directory
vstupni_adresar = (
    "/Users/zwarott/Desktop/stazena_uap"  # Zadej cestu k adresáři s vrstevami
)
resene_uzemi_path = "/Users/zwarott/Desktop/resene_uzemi/resene_uzemi.shp"  # Zadej cestu k vrstvě řešeného území
vystupni_adresar = (
    "/Users/zwarott/Desktop/orezana_uap"  # Zadej cestu k adresáři pro výstup
)
encoding = (
    "utf-8"  # Nastavení kódování pro výstupní soubory (např. 'utf-8', 'windows-1250')
)

# Zavolání funkce pro oříznutí vrstev
orez_vrstvy(vstupni_adresar, resene_uzemi_path, vystupni_adresar, encoding)
