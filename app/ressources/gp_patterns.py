""" Expressions régulières utilisées pour analyser l'input utilisateur et construire les réponses de GrandPy """

HELLO = r"^[Bb]onjour$|^[Bb]jr$|^[Ss]a?lu?t$|^[Yy]o$|^[Hh]i$"
OC = r"^[oO]pen[cC]las.{1,2}rooms?$|^[oO][cC]$"
ADDRESS = r"^[Aa]d{1,2}res{1,2}e?$"
KNOW = r"^[Cc]on{1,2}ai(tre|[ts]?|sai[ts]?)(-tu)?$"