#!/usr/bin/env python3
"""
WhatsApp Conversation Formatter.

Formats WhatsApp exported chats to be more readable for AI assistants.
"""

import re
import sys
import argparse
import locale
from datetime import datetime
from typing import List, Optional, Dict, Any

# Set locale to French
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'French_France.1252')
    except locale.Error:
        pass  # Fallback to default locale if French is not available

# Regex pattern for WhatsApp message format
MOTIF = re.compile(
    r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\s*([^:]+?):\s*(.+)',
    re.DOTALL
)

# Media keywords to detect media messages
MEDIAS = ['image omitted', 'video omitted', 'audio omitted',
          'sticker omitted', 'GIF omitted', 'document omitted',
          'Médias omis']  # Added French variant

# Date and time formats
FORMATS_DATE = ["%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", "%m/%d/%y", "%d-%m-%Y", "%d-%m-%y"]
FORMATS_TIME = ["%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"]


def analyser_temps(date_str: str, time_str: str) -> Optional[datetime]:
    """Analyse le timestamp.
    
    Parameters
    ----------
    date_str : str
        Chaîne contenant la date.
    time_str : str
        Chaîne contenant l'heure.
    
    Returns
    -------
    Optional[datetime]
        Objet datetime ou None si le parsing échoue.
    """
    for fmt_d in FORMATS_DATE:
        for fmt_t in FORMATS_TIME:
            try:
                return datetime.strptime(f"{date_str} {time_str}", f"{fmt_d} {fmt_t}")
            except ValueError:
                pass
    return None


def est_media(contenu: str) -> bool:
    """Vérifie si c'est un message média.
    
    Parameters
    ----------
    contenu : str
        Contenu du message.
    
    Returns
    -------
    bool
        True si le message contient un média, False sinon.
    """
    return any(m in contenu for m in MEDIAS)


def est_reponse(contenu: str) -> bool:
    """Vérifie si c'est une réponse.
    
    Parameters
    ----------
    contenu : str
        Contenu du message.
    
    Returns
    -------
    bool
        True si le message est une réponse, False sinon.
    """
    return contenu.startswith('‎') or '»' in contenu


def formater_message(contenu: str) -> str:
    """Formate le contenu du message.
    
    Parameters
    ----------
    contenu : str
        Contenu brut du message.
    
    Returns
    -------
    str
        Message formaté avec les symboles appropriés.
    """
    texte = contenu.strip().replace('‎', '')
    
    if est_media(texte):
        return f"[📎 {texte}]"
    if est_reponse(texte):
        return f"↪️ {texte}"
    return texte


def lire_fichier(filepath: str) -> List[str]:
    """Lit le fichier de chat.
    
    Parameters
    ----------
    filepath : str
        Chemin vers le fichier.
    
    Returns
    -------
    List[str]
        Lignes du fichier.
    
    Raises
    ------
    SystemExit
        Si le fichier n'existe pas.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().split('\n')
    except FileNotFoundError:
        print(f"Erreur: Fichier '{filepath}' non trouvé.")
        sys.exit(1)


def extraire_messages(lignes: List[str]) -> List[Dict[str, Any]]:
    """Extrait les messages du fichier.
    
    Parameters
    ----------
    lignes : List[str]
        Lignes du fichier de chat.
    
    Returns
    -------
    List[Dict[str, Any]]
        Liste des messages avec timestamp, sender et content.
    """
    messages = []
    message_courant = None

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue

        correspondance = MOTIF.match(ligne)

        if correspondance:
            if message_courant:
                messages.append(message_courant)

            date_str, time_str, sender, contenu = correspondance.groups()
            timestamp = analyser_temps(date_str, time_str)

            if timestamp:
                message_courant = {
                    'timestamp': timestamp,
                    'sender': sender.strip(),
                    'content': contenu.strip()
                }
            else:
                print(f"Attention: Impossible de parser {date_str} {time_str}")
        else:
            if message_courant:
                message_courant['content'] += "\n" + ligne

    if message_courant:
        messages.append(message_courant)

    return messages


def former_conversation(messages: List[Dict[str, Any]]) -> str:
    """Formate la conversation.
    
    Parameters
    ----------
    messages : List[Dict[str, Any]]
        Liste des messages à formater.
    
    Returns
    -------
    str
        Conversation formatée avec séparateurs de jours.
    """
    if not messages:
        return "Aucun message à formater."

    lignes = []
    date_courant = None

    lignes.append("=" * 80)
    lignes.append("CONVERSATION WHATSAPP - FORMATÉE")
    lignes.append("=" * 80)
    lignes.append("")

    for message in messages:
        timestamp = message['timestamp']
        sender = message['sender']
        contenu = message['content']
        
        date_msg = timestamp.date()

        if date_courant != date_msg:
            if date_courant is not None:
                lignes.append("")
                lignes.append("─" * 80)
                lignes.append("")

            date_courant = date_msg
            jour = timestamp.strftime('%A, %d %B %Y')
            lignes.append(f"📅 {jour}")
            lignes.append("─" * 80)
            lignes.append("")

        heure = timestamp.strftime("%H:%M:%S")
        contenu_formate = formater_message(contenu)
        lignes.append(f"[{heure}] {sender}: {contenu_formate}")

    lignes.append("")
    lignes.append("=" * 80)
    lignes.append("FIN DE LA CONVERSATION")
    lignes.append("=" * 80)

    return "\n".join(lignes)


def main():
    """Fonction principale.
    
    Analyse un fichier de chat WhatsApp exporté et le formate.
    Les arguments peuvent être passés via la ligne de commande.
    
    Raises
    ------
    SystemExit
        Si le fichier d'entrée n'existe pas ou si aucun message n'est trouvé.
    """
    parser = argparse.ArgumentParser(description="Formate les conversations WhatsApp")
    parser.add_argument("fichier_entree", help="Fichier de chat exporté")
    parser.add_argument("-o", "--sortie", help="Fichier de sortie (optionnel)")
    
    args = parser.parse_args()
    
    print(f"Analyse du chat WhatsApp depuis '{args.fichier_entree}'...")
    lignes = lire_fichier(args.fichier_entree)
    print(f"✓ {len(lignes)} lignes lues.")
    messages = extraire_messages(lignes)

    if not messages:
        print("Aucun message trouvé.")
        sys.exit(1)

    print(f"✓ {len(messages)} messages trouvés.")
    print("Formatage de la conversation...")
    
    texte_formate = former_conversation(messages)

    if args.sortie:
        try:
            with open(args.sortie, 'w', encoding='utf-8') as f:
                f.write(texte_formate)
            print(f"✓ Conversation sauvegardée dans '{args.sortie}'")
        except Exception as e:
            print(f"Erreur: {e}")
            sys.exit(1)
    else:
        print("\n" + texte_formate)

    print(f"\n✓ {len(messages)} messages formatés avec succès!")


if __name__ == "__main__":
    main()
