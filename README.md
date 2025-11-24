# WhatsApp Conversation Formatter

Un outil Python pour formater les exports de conversations WhatsApp afin de les rendre plus lisibles pour les assistants IA comme ChatGPT, Claude et Gemini.

## Fonctionnalités

- **Formatage des timestamps** : Conversion des horodatages en format HH:MM:SS plus lisible
- **Séparateurs de jours** : Division automatique des conversations par jour avec des séparateurs visuels
- **Détection de médias** : Identification et marquage des images, vidéos, audios et autres médias
- **Détection de réponses** : Identification des messages qui sont des réponses à d'autres messages
- **Support multiformat** : Compatible avec différents formats d'export WhatsApp (DD/MM/YYYY, MM/DD/YYYY, avec AM/PM, etc.)
- **Messages multilignes** : Gestion correcte des messages sur plusieurs lignes

## Installation

Aucune dépendance externe n'est requise ! Le programme utilise uniquement la bibliothèque standard Python.

```bash
git clone https://github.com/MothixExe/Whatsapp-Conversation-Formater.git
cd Whatsapp-Conversation-Formater
```

## Utilisation

### Exporter votre conversation WhatsApp

1. Ouvrez WhatsApp sur votre téléphone
2. Ouvrez la conversation que vous souhaitez exporter
3. Appuyez sur les trois points (⋮) en haut à droite
4. Sélectionnez "Plus" > "Exporter la discussion"
5. Choisissez "Sans médias" (recommandé)
6. Envoyez le fichier .txt vers votre ordinateur

### Formater la conversation

```bash
# Afficher le résultat dans le terminal
python3 whatsapp_formatter.py votre_chat.txt

# Sauvegarder dans un fichier
python3 whatsapp_formatter.py votre_chat.txt -o sortie_formatee.txt
```

### Exemple

Fichier d'entrée (`chat.txt`) :
```
15/01/2024, 09:30:15 Alice: Salut ! Comment ça va ?
15/01/2024, 09:32:45 Bob: Très bien merci !
15/01/2024, 09:33:10 Alice: ‎image omitted
16/01/2024, 08:00:00 Alice: Bonjour !
```

Fichier de sortie formaté :
```
================================================================================
CONVERSATION WHATSAPP - FORMATÉE
================================================================================

📅 lundi, 15 January 2024
────────────────────────────────────────────────────────────────────────────────

[09:30:15] Alice: Salut ! Comment ça va ?
[09:32:45] Bob: Très bien merci !
[09:33:10] Alice: [📎 image omitted]

────────────────────────────────────────────────────────────────────────────────

📅 mardi, 16 January 2024
────────────────────────────────────────────────────────────────────────────────

[08:00:00] Alice: Bonjour !

================================================================================
FIN DE LA CONVERSATION
================================================================================
```

## Utilisation avec des IA

Une fois votre conversation formatée, vous pouvez l'utiliser avec des assistants IA :

### ChatGPT / Claude / Gemini

```
Voici une conversation WhatsApp formatée. Peux-tu l'analyser et me donner un résumé ?

[Coller le contenu du fichier formaté ici]
```

### Avantages du format

- **Séparateurs de jour** : Permet à l'IA de comprendre facilement le contexte temporel
- **Timestamps simplifiés** : Réduit le bruit tout en gardant l'information temporelle
- **Marqueurs visuels** : Les emojis (📅, 📎, ↪️) aident l'IA à identifier rapidement le type de contenu
- **Structure claire** : En-têtes et pieds de page délimitent clairement la conversation

## Formats supportés

Le programme supporte plusieurs formats d'export WhatsApp :

- `[DD/MM/YYYY, HH:MM:SS]` (format européen)
- `[DD/MM/YY, HH:MM:SS]` (format européen court)
- `[MM/DD/YYYY, H:MM AM/PM]` (format américain)
- `[DD-MM-YYYY HH:MM]` (format avec tirets)

## Fonctionnalités avancées

### Détection de médias

Le programme détecte automatiquement les types de médias suivants :
- Images
- Vidéos
- Audios
- Stickers
- GIFs
- Documents
- Cartes de contact
- Localisations

### Messages multilignes

Les messages sur plusieurs lignes sont correctement gérés :
```
[15/01/2024, 09:30:15] Alice: Voici un message
qui continue sur plusieurs lignes
et qui sera correctement parsé
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## Auteur

Développé par MothixExe

## Support

Si vous rencontrez des problèmes :
1. Vérifiez que votre fichier d'export est au format texte (.txt)
2. Assurez-vous que Python 3.6+ est installé
3. Ouvrez une issue sur GitHub avec un exemple de votre fichier

## Remerciements

Merci à tous les contributeurs et utilisateurs de cet outil !
