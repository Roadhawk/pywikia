# -*- coding: utf-8  -*-
import family

__version__ = '$Id$'

# The Wikimedia family that is known as Wikinews

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikinews'

        self.languages_by_size = [
            'sr', 'en', 'pl', 'de', 'fr', 'it', 'pt', 'es', 'zh', 'ja', 'sv',
            'ru', 'fi', 'he', 'cs', 'bg', 'ar', 'ro', 'sd', 'ta', 'hu', 'no',
            'uk', 'ca', 'tr', 'bs', 'th',
        ]

        if family.config.SSL_connection:
            self.langs = dict([(lang, None) for lang in self.languages_by_size])
        else:
            self.langs = dict([(lang, '%s.wikinews.org' % lang) for lang in self.languages_by_size])

        # Override defaults
        self.namespaces[2]['cs'] = u'Redaktor'
        self.namespaces[2]['pl'] = u'Wikireporter'
        self.namespaces[3]['cs'] = u'Diskuse s redaktorem'
        self.namespaces[3]['pl'] = u'Dyskusja Wikireportera'


        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': [u'Wikinews', self.namespaces[4]['_default']],
            'ar': u'ويكي الأخبار',
            'bg': u'Уикиновини',
            'bs': u'Wikivijesti',
            'ca': u'Viquinotícies',
            'cs': u'Wikizprávy',
            'es': u'Wikinoticias',
            'fi': u'Wikiuutiset',
            'he': u'ויקיחדשות',
            'hu': u'Wikihírek',
            'it': u'Wikinotizie',
            'ja': u'ウィキニュース',
            'no': u'Wikinytt',
            'pt': u'Wikinotícias',
            'ro': u'Wikiştiri',
            'ru': u'Викиновости',
            'sr': u'Викивести',
            'th': u'วิกิข่าว',
            'tr': u'Vikihaber',
            'uk': u'ВікіНовини',
            'zh': [u'Wikinews', u'维基新闻'],
        }
        self.namespaces[5] = {
            '_default': [u'Wikinews talk', self.namespaces[5]['_default']],
            'ar': u'نقاش ويكي الأخبار',
            'bg': u'Уикиновини беседа',
            'bs': u'Razgovor s Wikivijestima',
            'ca': u'Viquinotícies Discussió',
            'cs': u'Diskuse k Wikizprávám',
            'de': u'Wikinews Diskussion',
            'es': u'Wikinoticias Discusión',
            'fi': u'Keskustelu Wikiuutisista',
            'fr': u'Discussion Wikinews',
            'he': u'שיחת ויקיחדשות',
            'hu': u'Wikihírek-vita',
            'it': u'Discussioni Wikinotizie',
            'ja': u'ウィキニュース・トーク',
            'nl': u'Overleg Wikinews',
            'no': u'Wikinytt-diskusjon',
            'pl': u'Dyskusja Wikinews',
            'pt': u'Wikinotícias Discussão',
            'ro': u'Discuție Wikiştiri',
            'ru': u'Обсуждение Викиновостей',
            'sd': u'Wikinews بحث',
            'sr': u'Разговор о Викивестима',
            'sv': u'Wikinewsdiskussion',
            'ta': u'Wikinews பேச்சு',
            'th': u'คุยเรื่องวิกิข่าว',
            'tr': u'Vikihaber tartışma',
            'uk': u'Обговорення ВікіНовини',
            'zh': [u'Wikinews talk', u'维基新闻讨论'],
        }

        self.namespaces[90] = {
            'en': u'Thread',
        }
        
        self.namespaces[91] = {
            'en': u'Thread talk',
        }
        
        self.namespaces[92] = {
            'en': u'Summary',
        }
        
        self.namespaces[93] = {
            'en': u'Summary talk',
        }
        
        self.namespaces[100] = {
            'ar': u'بوابة',
            'cs': u'Portál',
            'de': u'Portal',
            'en': u'Portal',
            'es': u'Comentarios',
            'he': u'פורטל',
            'it': u'Portale',
            'ja': u'ポータル',
            'no': u'Kommentarer',
            'pl': u'Portal',
            'pt': u'Portal',
            'ru': u'Портал',
            'sv': u'Portal',
            'tr': u'Portal',
            'zh': u'频道',
        }

        self.namespaces[101] = {
            'ar': u'نقاش البوابة',
            'cs': u'Diskuse k portálu',
            'de': u'Portal Diskussion',
            'en': u'Portal talk',
            'es': u'Comentarios Discusión',
            'he': u'שיחת פורטל',
            'it': u'Discussioni portale',
            'ja': [u'ポータル・トーク', u'ポータル‐ノート'],
            'no': u'Kommentarer-diskusjon',
            'pl': u'Dyskusja portalu',
            'pt': u'Portal Discussão',
            'ru': u'Обсуждение портала',
            'sv': u'Portaldiskussion',
            'tr': u'Portal tartışma',
            'zh': u'频道 talk',
        }

        self.namespaces[102] = {
            'ar': u'تعليقات',
            'bg': u'Мнения',
            'de': u'Meinungen',
            'en': u'Comments',
            'fr': u'Transwiki',
            'hu': u'Portál',
            'pt': u'Efeméride',
            'ru': u'Комментарии',
            'sr': u'Коментар',
        }

        self.namespaces[103] = {
            'ar': u'نقاش التعليقات',
            'bg': u'Мнения беседа',
            'de': u'Meinungen Diskussion',
            'en': u'Comments talk',
            'fr': u'Discussion Transwiki',
            'hu': u'Portálvita',
            'pt': u'Efeméride Discussão',
            'ru': u'Обсуждение комментариев',
            'sr': u'Разговор о коментару',
        }

        self.namespaces[104] = {
            'fr': u'Page',
        }

        self.namespaces[105] = {
            'fr': u'Discussion Page',
        }

        self.namespaces[106] = {
            'fr': u'Dossier',
            'no': u'Portal',
        }

        self.namespaces[107] = {
            'fr': u'Discussion Dossier',
            'no': u'Portal-diskusjon',
        }

        self.namespaces[108] = {
            'ja': u'短信',
        }

        self.namespaces[109] = {
            'ja': u'短信‐ノート',
        }


        self.obsolete = {
            'jp': 'ja',
            'nb': 'no',
            'nl': None, # https://bugzilla.wikimedia.org/show_bug.cgi?id=20325
            'zh-tw': 'zh',
            'zh-cn': 'zh'
        }

        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are put
        # after those, in code-alphabetical order.
        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'fi': self.alphabetic,
            'fr': self.alphabetic,
            'he': ['en'],
            'pl': self.alphabetic,
        }

        # Global bot allowed languages on http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = ['cs', 'hu',]
        # CentralAuth cross avaliable projects.
        self.cross_projects = [
            'wikipedia', 'wiktionary', 'wikibooks', 'wikiquote', 'wikisource', 'wikiversity', 
            'meta', 'mediawiki', 'test', 'incubator', 'commons', 'species'
        ]

    def code2encoding(self, code):
        return 'utf-8'

    def version(self, code):
        return '1.16wmf4'

    def shared_image_repository(self, code):
        return ('commons', 'commons')

    if family.config.SSL_connection:
        def hostname(self, code):
            return 'secure.wikimedia.org'

        def protocol(self, code):
            return 'https'

        def scriptpath(self, code):
            return '/%s/%s/w' % (self.name, code)

        def nicepath(self, code):
            return '/%s/%s/wiki/' % (self.name, code)
