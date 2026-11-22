#!/bin/bash
# Usage : telecharger.sh NOM_FICHIER URL "description"
# Télécharge une pièce dans ../../donnees/D05/sources, extrait le texte (PDF), ajoute une ligne au manifeste.
D="$(cd "$(dirname "$0")/../../donnees/D05" && pwd)"
S="$D/sources"; M="$D/MANIFESTE_PIECES.csv"
[ -f "$M" ] || echo "fichier;url;date_acces;sha256;description" > "$M"
f="$1"; u="$2"; desc="$3"
code=$(curl -sL -A "Mozilla/5.0" --max-time 120 -o "$S/$f" -w "%{http_code}" "$u")
sz=$(stat -c %s "$S/$f" 2>/dev/null)
if [ "$code" != "200" ] || [ "$sz" -lt 2000 ]; then echo "ECHEC $code $sz $u"; rm -f "$S/$f"; exit 1; fi
if head -c 5 "$S/$f" | grep -q "%PDF"; then pdftotext -enc UTF-8 -layout "$S/$f" "$S/${f%.*}.txt"; fi
h=$(sha256sum "$S/$f" | cut -d' ' -f1)
echo "$f;$u;$(date +%Y-%m-%d);$h;$desc" >> "$M"
echo "OK $code $sz $f"
