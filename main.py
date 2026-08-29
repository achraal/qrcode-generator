import qrcode
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import re


def nettoyer_nom(nom):
    """Transforme le titre en nom de fichier propre."""
    nom = re.sub(r'[<>:"/\\|?*]', '', nom)
    nom = re.sub(r'\s+', '_', nom.strip())
    return nom[:100]


def charger_police(taille):
    """Essaie de charger une police Windows."""
    chemins = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]

    for chemin in chemins:
        if Path(chemin).exists():
            return ImageFont.truetype(chemin, taille)

    return ImageFont.load_default()


def generer_qr():
    print("=" * 60)
    print("       GENERATEUR DE QR CODE")
    print("=" * 60)

    lien = input("\nLien Google Drive de l'image : ").strip()

    if not lien:
        print("❌ Aucun lien fourni.")
        return

    titre = input("Titre de l'image : ").strip()

    if not titre:
        titre = "Diagramme"

    # Dossier de sortie
    dossier = Path("qr_codes")
    dossier.mkdir(exist_ok=True)

    # Nom du fichier
    nom_fichier = nettoyer_nom(titre) + "_QR.png"
    chemin_sortie = dossier / nom_fichier

    # Génération du QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )

    qr.add_data(lien)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    # Dimensions
    largeur = qr_image.width
    hauteur_titre = 100

    image_finale = Image.new(
        "RGB",
        (largeur, qr_image.height + hauteur_titre),
        "white"
    )

    # QR
    image_finale.paste(qr_image, (0, 0))

    # Texte
    draw = ImageDraw.Draw(image_finale)
    font = charger_police(32)

    # Centrage du titre
    bbox = draw.textbbox((0, 0), titre, font=font)
    texte_largeur = bbox[2] - bbox[0]

    x = (largeur - texte_largeur) // 2
    y = qr_image.height + 25

    draw.text(
        (x, y),
        titre,
        fill="black",
        font=font
    )

    # Sauvegarde
    image_finale.save(chemin_sortie, quality=100)

    print("\n✅ QR CODE GÉNÉRÉ !")
    print(f"📁 Fichier : {chemin_sortie}")
    print(f"🏷️  Titre   : {titre}")
    print(f"🔗 Lien    : {lien}")


if __name__ == "__main__":
    generer_qr()