""" Expressions régulières utilisées pour analyser l'input utilisateur et construire les réponses de GrandPy """

HELLO = r"^[Bb](on)?j(ou)?r$|^[Ss]lt$|^[Ss]alut(ations?)?$|^[Yy]o$|^[Hh]i$|^👋$"
OC = r"^[oO](pen)?[cC](las{1,2}rooms?)?$"
ADDRESS = r"^[Aa]d{1,2}res{1,2}e?$"
KNOW = r"^[Cc]on{1,2}ai(tre|[ts]?|sai[ts]?)(-tu)?$"
HOW = r"^[Cc]om{1,2}ent$"
GO = r"^[Vv]as?(-tu)?$|^[Aa]l{1,2}ez(-vous)?$"
AT = r"^[àÀaA]$" # [aA] = dangereux
QUESTION = r"^\?{1,3}\!{0,2}$"
WHAT = r"^[Qq]uel(le)?$"
TIME = r"[Hh]eure"