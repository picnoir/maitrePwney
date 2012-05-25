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
    """Irc bot. Can set op mode to someone, draw a poney and save bookmarks"""


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
        if ev.arguments()[0].split(' ')[0]== '!search':
            self.search_bookmark(serv, ev.arguments()[0].split(' ')[1])


    def add_bookmark(self, serv,  bookmarkWords):
        bookmarkWords.remove("!add")
        if bookmarkWords[0].find('http',0,5)==0:
            bookmarkFormat = ConfigParser.RawConfigParser()
            bookmarkFormat.read('bookmarks')
            try: bookmarkFormat.get(bookmarkWords[0],'tag1')
            except ConfigParser.NoSectionError:
                bookmarkFormat.add_section(bookmarkWords[0])
                category=bookmarkWords[0]
                bookmarkWords.remove(bookmarkWords[0])
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


    def search_bookmark(self, serv, tag):
        bookmarks= ConfigParser.RawConfigParser()
        bookmarks.read('bookmarks')
        done = False
        for section in bookmarks.sections():
            for option in bookmarks.options(section):
                if bookmarks.get(section,option)==tag:
                    serv.privmsg(self.channel, "{0}".format(section))
                    done = True
        if done==False:
            serv.privmsg(self.channel, "Aucun bookmark n'a été taggé avec {0}".format(tag))


    def draw_poney(self, serv):
        poneyAsciiArt = ['                   ,%%%,', '                 ,%%%` %', "                ,%%`( '|             ..:[ OptiPwney ]:..", '               ,%%@ /\\_/', '     ,%.-"""--%%% "@@__              Teh Pau HackerSpace', '    %%/             |__`\\                    ', "   .%'\\     |   \\   /  //             ", "   ,%' >   .'----\\ |  [/               ", '      < <<`       ||      ', '       `\\\\\\       ||                                   with pwnies !', '         )\\\\      )\\', ' ^^^^^^^^"""^^^^^^""^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^', '']

        for line in poneyAsciiArt:
            serv.privmsg(self.channel, line)


if __name__ == "__main__":
    BotPoney().start()
