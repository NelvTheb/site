import os
import re
import shutil

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_DIR = "."  # Le dossier à scanner (actuel)
HTML_FILE = "index.html"  # Le fichier HTML à mettre à jour

# Noms de fichiers exacts à exclure
EXCLUDED_FILES = {'.DS_Store', '.gitignore', 'LICENSE'}

# Extensions exclues
EXCLUDED_EXTENSIONS = {'.html', '.py', '.css', '.bak', '.md', '.js'}

# Dossiers exclus
EXCLUDED_DIRS = {'.git', '__pycache__'}

# Mappage des icônes de ta charte graphique
ICON_PDF = "fa-solid fa-file-pdf icon-tree-pdf"
ICON_MATLAB = "fa-solid fa-file-code icon-tree-matlab"
ICON_IMAGE = "fa-solid fa-file-image icon-tree-image"
ICON_GENERIC = "fa-solid fa-file icon-generic"
ICON_TEX = "fa-solid fa-file-lines icon-tree-tex"


def get_file_icon(filename):
    """Retourne la bonne classe d'icône FontAwesome selon l'extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    # 1. Gestion des fichiers PDF
    if ext == '.pdf':
        return ICON_PDF
    
    # 2. Traitement MATLAB : scripts (.m, .mlx), données (.mat) et Simulink (.slx)
    elif ext in ['.m', '.mlx', '.mat', '.slx']:
        return ICON_MATLAB
        
    # 3. Traitement des images
    elif ext in ['.png', '.jpg', '.jpeg', '.svg', '.eps']:
        return ICON_IMAGE

    elif ext == '.tex':
        return ICON_TEX
        
    # 4. Autres fichiers génériques
    return ICON_GENERIC


def build_html_tree(path):
    """Génère récursivement le code HTML de l'arborescence."""
    html = ""
    try:
        items = sorted(os.listdir(path), key=lambda x: (
            not os.path.isdir(os.path.join(path, x)), x.lower()))
    except PermissionError:
        return ""

    for item in items:
        full_path = os.path.join(path, item)
        relative_url = os.path.relpath(full_path, TARGET_DIR).replace("\\", "/")

        if os.path.isdir(full_path):
            if item in EXCLUDED_DIRS:
                continue

            # On vérifie si le dossier contient des fichiers valides avant de créer la balise
            sub_tree = build_html_tree(full_path)
            if not sub_tree.strip():
                continue

            html += "<li>\n"
            html += "  <details>\n"
            html += f"    <summary><i class='fa-solid fa-folder icon-folder'></i> {item}</summary>\n"
            html += "    <div class='folder-content'>\n"
            html += "      <ul class='tree-view'>\n"
            html += sub_tree
            html += "      </ul>\n"
            html += "    </div>\n"
            html += "  </details>\n"
            html += "</li>\n"
        else:
            # 1. Exclusion par nom exact de fichier (.DS_Store, .gitignore, etc.)
            if item in EXCLUDED_FILES:
                continue

            # 2. Exclusion par extension
            ext = os.path.splitext(item)[1].lower()
            if ext in EXCLUDED_EXTENSIONS:
                continue

            icon_class = get_file_icon(item)
            html += "<li>\n"
            html += f"  <a class='file-item' href='{relative_url}' target='_blank'>\n"
            html += f"    <i class='{icon_class}'></i> {item}\n"
            html += "  </a>\n"
            html += "</li>\n"

    return html


def update_html_file():
    """Injecte l'arborescence générée entre les tags du fichier HTML."""
    if not os.path.exists(HTML_FILE):
        print(f"Erreur : Le fichier {HTML_FILE} est introuvable.")
        return

    # SÉCURITÉ : Création d'un backup automatique avant modification
    backup_file = f"{HTML_FILE}.bak"
    shutil.copy2(HTML_FILE, backup_file)

    # 1. Générer le bloc HTML de l'arborescence
    print(f"Scanning du dossier '{TARGET_DIR}' en cours...")
    generated_tree_html = build_html_tree(TARGET_DIR)

    # 2. Lire le fichier HTML existant
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Remplacement sécurisé via Regex avec groupes nommés
    pattern = r'(?P<start><span style="display:none;" id="START_KEY"></span>)(.*?)(?P<end><span style="display:none;" id="END_KEY"></span>)'
    
    if not re.search(pattern, content, flags=re.DOTALL):
        print("Erreur : Impossible de trouver les balises START_KEY et END_KEY.")
        os.replace(backup_file, HTML_FILE)
        return

    # Reconstruction propre du fichier
    def replace_content(match):
        return f"{match.group('start')}\n{generated_tree_html}{match.group('end')}"

    new_content = re.sub(pattern, replace_content, content, flags=re.DOTALL)

    # 4. Écriture du fichier mis à jour
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Nettoyage du backup
    if os.path.exists(backup_file):
        os.remove(backup_file)

    print("Structure HTML mise à jour avec succès et en toute sécurité ! ✓")


if __name__ == "__main__":
    update_html_file()
