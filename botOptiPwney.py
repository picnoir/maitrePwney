# -*- coding: utf-8 -*-

import irclib
import ircbot

class BotPoney(ircbot.SingleServerIRCBot):
    canal="#canal" """Canal sur lequel le bot doit se connecter"""
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6665)],
                                           "MaitrePwney", "Bot")
    def on_welcome(self, serv, ev):
        serv.privmsg("nickserv", "identify motDePasse") """Identification"""
        serv.join(self.canal)
    def on_privmsg(self, serv, ev):
        """Méthode appeée quand le bot reçoit un pm"""
        demandeur = irclib.nm_to_n(ev.source())
        if ev.arguments()[0]=="op" and demandeur in ["Utilisateurs","pouvant être op"]:
            commande="+o {0}".format(demandeur)
            serv.mode(self.canal,commande)

if __name__ == "__main__":
    BotPoney().start()
