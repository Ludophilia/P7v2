import random

from app.grandpy.skills.heads_tails import speech

def play_heads_or_tails(matches, message):

    # Si une réponse est attendue, autant gérer ça ici non ? Non ?

    """Gère tout ce qui a à voir avec le jeu pile ou face proposé par grandpy. Retourne le paramètre message modifié."""

    if "play" in matches: #and not self.isWaitingForAnAnswer:

        #self.isWaitingForAnAnswer.add("#HT")
        #ADD DATABASE OP HERE

        message += speech.HT_EXPLAIN_RULES

    elif False: #Add database-related RULE here
    #ADD DATABASE OP HERE

        if ("heads" in matches) ^ ("tails" in matches):

            playerschoice = 0 if "heads" in matches else 1
            gamesresult = random.randint(0,1)
            gr_readable = ["pile", "face"][gamesresult]

            bravo, shame = speech.HT_PLAYER_VICTORY(gr_readable),speech.HT_PLAYER_DEFEAT(gr_readable)

            message += speech.HT_TOSS_COIN
            message += bravo if playerschoice == gamesresult else shame
            #ADD DATABASE OP HERE
            if self.memory.get("HT_ERROR"): self.memory.pop("HT_ERROR")
            self.isWaitingForAnAnswer.remove("#HT")

        else:
            #Les lignes fautives ?
            #ADD DATABASE OP HERE
            if self.memory.get("HT_ERROR") == None:
                self.memory["HT_ERROR"] = 1  
            else:
                    self.memory["HT_ERROR"] + 1
            
            remaining = 3 - self.memory["HT_ERROR"]

            #ADD DATABASE OP HERE
            if remaining == 0:
                message += speech.HT_OUT_OF_TRIES
                self.memory.pop("HT_ERROR")
                self.isWaitingForAnAnswer.remove("#HT")

            else:
                message += speech.HT_ERROR(remaining)

    return message