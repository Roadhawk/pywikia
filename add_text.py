#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This is a Bot written by Filnik to add a text at the end of the page but above
categories, interwiki and template for the stars of the interwiki (default).

Alternatively it may also add a text at the top of the page.
These command line parameters can be used to specify which pages to work on:

&params;

Furthermore, the following command line parameters are supported:

-page             Use a page as generator

-talkpage         Put the text onto the talk page instead the generated on
-talk

-text             Define which text to add. "\n" are interpreted as newlines.

-textfile         Define a texfile name which contains the text to add

-summary          Define the summary to use

-except           Use a regex to check if the text is already in the page

-excepturl        Use the html page as text where you want to see if there's
                  the text, not the wiki-page.

-newimages        Add text in the new images

-untagged         Add text in the images that don't have any license template

-always           If used, the bot won't ask if it should add the text
                  specified

-up               If used, put the text at the top of the page

--- Example ---
1.
# This is a script to add a template to the top of the pages with
# category:catname
# Warning! Put it in one line, otherwise it won't work correctly.

python add_text.py -cat:catname -summary:"Bot: Adding a template"
-text:"{{Something}}" -except:"\{\{([Tt]emplate:|)[Ss]omething" -up

2.
# Command used on it.wikipedia to put the template in the page without any
# category.
# Warning! Put it in one line, otherwise it won't work correctly.

python add_text.py -excepturl:"class='catlinks'>" -uncat
-text:"{{Categorizzare}}" -except:"\{\{([Tt]emplate:|)[Cc]ategorizzare"
-summary:"Bot: Aggiungo template Categorizzare"

--- Credits and Help ---
This script has been written by Botwiki's staff, if you want to help us
or you need some help regarding this script, you can find us here:

* http://botwiki.sno.cc

"""

#
# (C) Filnik, 2007-2008
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: add_text.py,v 1.5 2008/04/25 17:08:30 filnik Exp$'
#

import re, pagegenerators, urllib2, urllib
import wikipedia
import codecs, config

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;':     pagegenerators.parameterHelp,
}

msg = {
    'ar': u'بوت: إضافة %s',
    'cs': u'Robot přidal %s',
    'de': u'Bot: "%s" hinzugefügt',
    'en': u'Bot: Adding %s',
    'fr': u'Robot : Ajoute %s',
    'he': u'בוט: מוסיף %s',
    'fa': u'ربات: افزودن %s',
    'it': u'Bot: Aggiungo %s',
    'ja': u'ロボットによる: 追加 %s',
    'ksh': u'Bot: dobeijedonn: %s',
    'nds': u'Bot: tofoiegt: %s',
    'nn': u'Robot: La til %s',
    'pl': u'Robot dodaje: %s',
    'pt': u'Bot: Adicionando %s',
    'ru': u'Бот: добавление %s',
    'sv': u'Bot: Lägger till %s',
    'szl': u'Bot dodowo: %s',
    'vo': u'Bot: Läükon vödemi: %s',
    'zh': u'機器人: 正在新增 %s',
    }

nn_iw_msg = u'<!--interwiki (no, sv, da first; then other languages alphabetically by name)-->'

class NoEnoughData(wikipedia.Error):
    """ Error class for when the user doesn't specified all the data needed """

class NothingFound(wikipedia.Error):
    """ An exception indicating that a regex has return [] instead of results."""

# Useful for the untagged function
def pageText(url):
    """ Function to load HTML text of a URL """
    try:
        request = urllib2.Request(url)
        request.add_header("User-Agent", wikipedia.useragent)
        response = urllib2.urlopen(request)
        text = response.read()
        response.close()
        # When you load to many users, urllib2 can give this error.
    except urllib2.HTTPError:
        wikipedia.output(u"Server error. Pausing for 10 seconds... " + time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime()) )
        response.close()
        time.sleep(10)
        return pageText(url)
    return text

def untaggedGenerator(untaggedProject, limit = 500):
    """ Function to get the pages returned by this tool:
    http://toolserver.org/~daniel/WikiSense/UntaggedImages.php """
    lang = untaggedProject.split('.', 1)[0]
    project = '.' + untaggedProject.split('.', 1)[1]
    if lang == 'commons':
        link = 'http://toolserver.org/~daniel/WikiSense/UntaggedImages.php?wikifam=commons.wikimedia.org&since=-100d&until=&img_user_text=&order=img_timestamp&max=100&order=img_timestamp&format=html'
    else:
        link = 'http://toolserver.org/~daniel/WikiSense/UntaggedImages.php?wikilang=' + lang + '&wikifam=' + project + '&order=img_timestamp&max=' + str(limit) + '&ofs=0&max=' + str(limit)
    text = pageText(link)
    #print text
    regexp = r"""<td valign='top' title='Name'><a href='http://.*?\.org/w/index\.php\?title=(.*?)'>.*?</a></td>"""
    results = re.findall(regexp, text)
    if results == []:
        print link
        raise NothingFound(
'Nothing found! Try to use the tool by yourself to be sure that it works!')
    else:
        for result in results:
            yield wikipedia.Page(wikipedia.getSite(), result)

def add_text(page = None, addText = None, summary = None, regexSkip = None,
             regexSkipUrl = None, always = False, up = False, putText = True,
             oldTextGiven = None, create=False):
    if not addText:
        raise NoEnoughData('You have to specify what text you want to add!')
    if not summary:
        summary = wikipedia.translate(wikipedia.getSite(), msg) % addText[:200]

    # When a page is tagged as "really well written" it has a star in the
    # interwiki links. This is a list of all the templates used (in regex
    # format) to make the stars appear.
    starsList = [
        u'bueno',
        u'cyswllt[ _]erthygl[ _]ddethol', u'dolen[ _]ed',
        u'destacado', u'destaca[tu]',
        u'enllaç[ _]ad',
        u'enllaz[ _]ad',
        u'leam[ _]vdc',
        u'legătură[ _]a[bcf]',
        u'liamm[ _]pub',
        u'lien[ _]adq',
        u'lien[ _]ba',
        u'liên[ _]kết[ _]bài[ _]chất[ _]lượng[ _]tốt',
        u'liên[ _]kết[ _]chọn[ _]lọc',
        u'ligam[ _]adq',
        u'ligoelstara',
        u'ligoleginda',
        u'link[ _][afgu]a', u'link[ _]adq', u'link[ _]f[lm]', u'link[ _]km',
        u'link[ _]sm', u'linkfa',
        u'na[ _]lotura',
        u'nasc[ _]ar',
        u'tengill[ _][úg]g',
        u'ua',
        u'yüm yg',
        u'רא',
        u'وصلة مقالة جيدة',
        u'وصلة مقالة مختارة',
    ]

    errorCount = 0
    site = wikipedia.getSite()
    # /wiki/ is not always the right path in non-wiki projects
    pathWiki = site.family.nicepath(site.lang)

    if putText:
        wikipedia.output(u'Loading %s...' % page.title())
    if oldTextGiven == None:
        try:
            text = page.get()
        except wikipedia.NoPage:
            if create:
                wikipedia.output(u"%s doesn't exist, creating it!"
                                 % page.title())
                text = u''
            else:
                wikipedia.output(u"%s doesn't exist, skip!" % page.title())
                return (False, False, always) # continue
        except wikipedia.IsRedirectPage:
            wikipedia.output(u"%s is a redirect, skip!" % page.title())
            return (False, False, always) # continue
    else:
        text = oldTextGiven
    # Understand if the bot has to skip the page or not
    # In this way you can use both -except and -excepturl
    if regexSkipUrl != None:
        url = '%s%s' % (pathWiki, page.urlname())
        result = re.findall(regexSkipUrl, site.getUrl(url))
        if result != []:
            wikipedia.output(
u'Exception! regex (or word) used with -exceptUrl is in the page. Skip!')
            return (False, False, always) # continue
    if regexSkip != None:
        result = re.findall(regexSkip, text)
        if result != []:
            wikipedia.output(
u'Exception! regex (or word) used with -except is in the page. Skip!')
            return (False, False, always) # continue
    # If not up, text put below
    if not up:
        newtext = text
        # Getting the categories
        categoriesInside = wikipedia.getCategoryLinks(newtext, site)
        # Deleting the categories
        newtext = wikipedia.removeCategoryLinks(newtext, site)
        # Getting the interwiki
        interwikiInside = wikipedia.getLanguageLinks(newtext, site)
        # Removing the interwiki
        newtext = wikipedia.removeLanguageLinks(newtext, site)
        #nn got a message between the categories and the iw's and they want to keep it there, first remove it
        if (site.language()==u'nn'):
            newtext = newtext.replace(nn_iw_msg, '')
        # Translating the \\n into binary \n
        addText = addText.replace('\\n', '\n')
        # Adding the text
        newtext += u"\n%s" % addText
        # Reputting the categories
        newtext = wikipedia.replaceCategoryLinks(newtext, categoriesInside, site, True)
        #Put the nn iw message back
        if (site.language()==u'nn'):
            newtext = newtext + u'\n' + nn_iw_msg
        # Dealing the stars' issue
        allstars = []
        starstext = wikipedia.removeDisabledParts(text)
        for star in starsList:
            regex = re.compile('(\{\{(?:template:|)%s\|.*?\}\}[\s]*)' % star,
                               re.I)
            found = regex.findall(starstext)
            if found != []:
                newtext = regex.sub('', newtext)
                allstars += found
        if allstars != []:
            newtext = newtext.strip()+'\r\n\r\n'
            allstars.sort()
            for element in allstars:
                newtext += '%s\r\n' % element.strip()
        # Adding the interwiki
        newtext = wikipedia.replaceLanguageLinks(newtext, interwikiInside, site)
    # If instead the text must be added above...
    else:
        newtext = addText + '\n' + text
    if putText and text != newtext:
        wikipedia.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                         % page.title())
        wikipedia.showDiff(text, newtext)
    # Let's put the changes.
    while True:
        # If someone load it as module, maybe it's not so useful to put the
        # text in the page
        if putText:
            if not always:
                choice = wikipedia.inputChoice(
                    u'Do you want to accept these changes?',
                    ['Yes', 'No', 'All'], ['y', 'N', 'a'], 'N')
                if choice == 'a':
                    always = True
                elif choice == 'n':
                    return (False, False, always)
            if always or choice == 'y':
                try:
                    if always:
                        page.put(newtext, summary)
                    else:
                        page.put_async(newtext, summary)
                except wikipedia.EditConflict:
                    wikipedia.output(u'Edit conflict! skip!')
                    return (False, False, always)
                except wikipedia.ServerError:
                    errorCount += 1
                    if errorCount < 5:
                        wikipedia.output(u'Server Error! Wait..')
                        time.sleep(5)
                        continue
                    else:
                        raise wikipedia.ServerError(u'Fifth Server Error!')
                except wikipedia.SpamfilterError, e:
                    wikipedia.output(
                        u'Cannot change %s because of blacklist entry %s'
                        % (page.title(), e.url))
                    return (False, False, always)
                except wikipedia.PageNotSaved, error:
                    wikipedia.output(u'Error putting page: %s' % error.args)
                    return (False, False, always)
                except wikipedia.LockedPage:
                    wikipedia.output(u'Skipping %s (locked page)'
                                     % page.title())
                    return (False, False, always)
                else:
                    # Break only if the errors are one after the other...
                    errorCount = 0
                    return (True, True, always)
        else:
            return (text, newtext, always)

def main():
    # If none, the var is setted only for check purpose.
    summary = None; addText = None; regexSkip = None; regexSkipUrl = None;
    generator = None; always = False
    textfile=None
    talkPage=False
    namespaces=[]
    # Load a lot of default generators
    genFactory = pagegenerators.GeneratorFactory()
    # Put the text above or below the text?
    up = False
    # Loading the arguments
    for arg in wikipedia.handleArgs():
        if arg.startswith('-textfile'):
            if len(arg) == 9:
                textfile = wikipedia.input(
                    u'Which textfile do you want to add?')
            else:
                textfile = arg[10:]
        elif arg.startswith('-text'):
            if len(arg) == 5:
                addText = wikipedia.input(u'What text do you want to add?')
            else:
                addText = arg[6:]
        elif arg.startswith('-summary'):
            if len(arg) == 8:
                summary = wikipedia.input(u'What summary do you want to use?')
            else:
                summary = arg[9:]
        elif arg.startswith('-page'):
            if len(arg) == 5:
                generator = [wikipedia.Page(
                    wikipedia.getSite(),
                    wikipedia.input(u'What page do you want to use?')
                    )]
            else:
                generator = [wikipedia.Page(wikipedia.getSite(), arg[6:])]
        elif arg.startswith('-excepturl'):
            if len(arg) == 10:
                regexSkipUrl = wikipedia.input(u'What text should I skip?')
            else:
                regexSkipUrl = arg[11:]
        elif arg.startswith('-except'):
            if len(arg) == 7:
                regexSkip = wikipedia.input(u'What text should I skip?')
            else:
                regexSkip = arg[8:]
        elif arg.startswith('-untagged'):
            if len(arg) == 9:
                untaggedProject = wikipedia.input(
                    u'What project do you want to use?')
            else:
                untaggedProject = arg[10:]
            generator = untaggedGenerator(untaggedProject)
        elif arg == '-up':
            up = True
        elif arg == '-always':
            always = True
        elif arg == '-talk' or arg == '-talkpage':
            talkPage = True
        else:
            genFactory.handleArg(arg)
    if textfile and not addText:
        f = codecs.open(textfile, 'r', config.textfile_encoding)
        addText = f.read()
        f.close()
    if not generator:
        generator = genFactory.getCombinedGenerator()
    # Check if there are the minimal settings
    if not generator:
        raise NoEnoughData(
            'You have to specify the generator you want to use for the script!')
    if talkPage:
        generator = pagegenerators.PageWithTalkPageGenerator(generator)
        site = wikipedia.getSite()
        for namespace in site.namespaces():
            index = site.getNamespaceIndex(namespace)
            if index%2==1 and index>0:
                namespaces += [index]
        generator = pagegenerators.NamespaceFilterPageGenerator(
            generator, namespaces)
    # Main Loop
    for page in generator:
        (text, newtext, always) = add_text(page, addText, summary, regexSkip,
                                           regexSkipUrl, always, up, True,
                                           create=talkPage)

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()
