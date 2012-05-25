# -*- coding: utf-8 -*-


#                   ,%%%,
#                 ,%%%` %
#                ,%%`( '|             ..:[ OptiPwney ]:..
#               ,%%@ /\_/
#     ,%.-"""--%%% "@@__              Teh Pau HackerSpace
#    %%/             |__`\                    
#   .%'\     |   \   /  //             
#   ,%' >   .'----\ |  [/               
#      < <<`       ||      
#       `\\\       ||                                   with pwnies !
#         )\\      )\
# ^^^^^^^^"""^^^^^^""^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


try: 
    import irclib, ircbot, ConfigParser
except:
    print 'Missing dependancies, please install irclib, ircbot and ConfigParser'
    system.exit(True)


class BotPoney(ircbot.SingleServerIRCBot):
    """Simple irc bot. Can set op mode to someone"""


    def __init__(self):
        self.config = ConfigParser.RawConfigParser(allow_no_value=False)
        self.config.read("maitrePwney.conf")
        self.botPassword = self.config.get('config','password')
        self.channel = self.config.get('config','channel')
        self.serverAdress = self.config.get('config','adress')
        self.serverPort = self.config.getint('config','port')
        self.botName = self.config.get('config','name')
        self.usersAllowed = self.config.get('config','usersAllowed').strip().split(', ')
        ircbot.SingleServerIRCBot.__init__(self, [(self.serverAdress, self.serverPort)],
                                           self.botName, "Bot")

    def on_welcome(self, serv, ev):
        serv.privmsg("nickserv", "identify {0}".format(self.botPassword))
        serv.join(self.channel)


    def on_privmsg(self, serv, ev):
        self.config.read("maitrePwney.conf")
        self.usersAllowed = self.config.get('config','usersAllowed').strip().split(', ')
        request = irclib.nm_to_n(ev.source())
        if ev.arguments()[0]=="op" and request in self.usersAllowed:
            query = "+o {0}".format(request)
            serv.mode(self.channel,query)


    def on_pubmsg(self, serv, ev):
        request = irclib.nm_to_n(ev.source())
        if ev.arguments()[0]=="dessine-moi un poney" and request in self.usersAllowed:
            self.draw_poney(serv)
        if ev.arguments()[0].split(' ')[0] == '!add':
            self.add_bookmark(serv, ev.arguments()[0].strip().split(' '))


    def add_bookmark(self, serv,  bookmarkWords):
        bookmarkWords.remove("!add")
        if bookmarkWords[0].find('http',0,5)==0:
            bookmarkFormat = ConfigParser.RawConfigParser()
            bookmarkFormat.read('bookmarks')
            try: bookmarkFormat.get(bookmarkWords[0],'tag1')
            except ConfigParser.NoSectionError:
                bookmarkFormat.add_section(bookmarkWords[1])
                category=bookmarkWords[1]
                bookmarkWords.remove(bookmarkWords[1])
                number = 1
                for tag in bookmarkWords:
                    bookmarkFormat.set(category,"tag{0}".format(number),tag)
                    number += 1
                with open('bookmarks', 'wb') as bookmarkFile:
                    bookmarkFormat.write(bookmarkFile)
                serv.privmsg(self.channel, "Bookmark enregistré.")
            else:
                serv.privmsg(self.channel, "Url déjà bookmarkée.")
        else:
            serv.privmsg(self.channel, "Veuillez bien respecter la syntaxe suivante: !add <url> <tag1> <tag2> <tag3> ...")
            


    def draw_poney(self, serv):
        poneyAsciiArt = ['                   ,%%%,', '                 ,%%%` %', "                ,%%`( '|             ..:[ OptiPwney ]:..", '               ,%%@ /\\_/', '     ,%.-"""--%%% "@@__              Teh Pau HackerSpace', '    %%/             |__`\\                    ', "   .%'\\     |   \\   /  //             ", "   ,%' >   .'----\\ |  [/               ", '      < <<`       ||      ', '       `\\\\\\       ||                                   with pwnies !', '         )\\\\      )\\', ' ^^^^^^^^"""^^^^^^""^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^', '']

        for line in poneyAsciiArt:
            serv.privmsg(self.channel, line)


if __name__ == "__main__":
    BotPoney().start()
