# -*- coding: UTF-8 -*-
import sys, os
import urllib, urlparse, urllib2, re
import xbmcgui, xbmc, xbmcaddon, xbmcplugin

stream_url = {
    '1080p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_1080_av-p.m3u8',
    '720p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0720_av-p.m3u8',
    '540p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0540_av-p.m3u8',
    '404p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0404_av-p.m3u8',
    '288p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0288_av-p.m3u8'
}
video_url = {
    '720p': '/index_2_av.m3u8',
    '360p': '/index_1_av.m3u8',
    '270p': '/index_0_av.m3u8'
}
main_menu = ([[30003, 30004, 'lastvids+next', 	'folder', '/z/17317.html'],	#Broadcasts
              [30005, 30006, 'tvshows',			'folder', ''],				#TV Shows
              [30007, 30008, 'lastvids+next', 	'folder', '/z/17192.html'],	#All Videos
              [30009, 30010, 'lastvids+next', 	'folder', '/z/17226.html'],	#Daily Shoots
              [30011, 30012, 'lastvids+next', 	'folder', '/z/17318.html'],	#Reportages
              [30013, 30014, 'lastvids+next', 	'folder', '/z/17319.html']	#Interviews
             ])
tvshows =   ([[30031, 30032, 'lastvids+archive', 'olevski',		'/z/20333.html'],
              [30033, 30034, 'lastvids+archive', 'nveurope', 	'/z/18657.html'],
              [30035, 30036, 'lastvids+archive', 'nvasia', 		'/z/17642.html'],
              [30037, 30038, 'lastvids+archive', 'nvamerica',	'/z/20347.html'],
              [30039, 30040, 'lastvids+archive', 'oba', 		'/z/20366.html'],
              [30041, 30042, 'lastvids+archive', 'itogi', 		'/z/17499.html'],
              [30043, 30044, 'lastvids+archive', 'week', 		'/z/17498.html'],
              [30045, 30046, 'lastvids+archive', 'baltia', 		'/z/20350.html'],
              [30047, 30048, 'lastvids+archive', 'bisplan', 	'/z/20354.html'],
              [30049, 30050, 'lastvids+archive', 'unknownrus',	'/z/20331.html'],
              [30051, 30052, 'lastvids+archive', 'guests', 		'/z/20330.html']
             ])
default_view = {
    'skin.confluence': {'main_menu': '50', 'tvshows': '500', 'lastvids+next': '515', 'lastvids+archive': '515',
                        'allvids_archive': '51', 'video': '51'},
    'skin.aeon.nox.5': {'main_menu': '50', 'tvshows': '50', 'lastvids+next': '510', 'lastvids+archive': '510',
                        'allvids_archive': '50', 'video': '510'},
    'skin.estuary': {'main_menu': '55', 'tvshows': '500', 'lastvids+next': '502', 'lastvids+archive': '502',
                     'allvids_archive': '55', 'video': '502'}
}

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

mode = args.get('mode', None)
furl = args.get('folderurl', None)
ftitle = args.get('title', None)
flevel = int(args.get('level', '0')[0])
fname = args.get('name', None)
site_url = 'http://www.currenttime.tv'
addon = xbmcaddon.Addon('plugin.video.currenttime.tv')

xbmcplugin.setContent(addon_handle, 'tvshows')  # !!!

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def img_link(name, type):
    if type == 'fanart' or type == 'poster':
        ext = '.jpg'
    else:
        ext = '.png'
    image = os.path.join(addon.getAddonInfo('path'), "resources/media/" + name + '_' + type + ext)
    return image


def addDir(arg):
    li = xbmcgui.ListItem(label=arg['title'])
    if arg['mode'] != 'play':
        arg['url'] = build_url(
            {'mode': arg['mode'], 'title': arg['title'], 'name': arg['name'], 'level': str(flevel + 1),
             'folderurl': arg['url']})
        isFolder = True
        li.setProperty("IsPlayable", "false")  # !!!
    else:
        isFolder = False
        li.setProperty("IsPlayable", "true")  # !!!
    info = {
        'mediatype': 'tvshow',                 # !!!
        'plot': arg['plot']
    }
    li.setInfo('video', info)
    li.setArt({'thumb': arg['thumb'], 'fanart': arg['fanart']})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=arg['url'], listitem=li, isFolder=isFolder)
    return ok


def addVideoDir(url):
    page = readPage(site_url + url)
    match1 = re.compile('<a class="html5PlayerImage" href="(.+?)">\n'
                        '<img src="(.+?)"').findall(page)
    match_title = re.compile('<meta name="title" content="(.+?)" />').findall(page)
    match_plot = re.compile('<meta name="description" content="(.+?)" />', re.DOTALL).findall(page)
    if len(match_plot) < 1: match_plot = [' ']
    addDir({
        'name':     fname[0],
        'thumb':    re.sub(r'_w\w+', '_w512_r1.jpg', match1[0][1]),
        'fanart':   re.sub(r'_w\w+', '_w1280_r1.jpg', match1[0][1]),
        'mode':     'play',
        'title':    re.sub('&quot;', '"', match_title[0]),
        'plot':     re.sub('&quot;', '"', match_plot[0]),
        'url':      re.sub('/master.m3u8', video_url[xbmcplugin.getSetting(addon_handle, 'res_video')], match1[0][0])
    })


def readPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page


def showMenu(menu):
    for title, plot, mode, name, url in menu:
        addDir({
            'name':    name,
            'thumb':   img_link(name, 'thumb'),
            'fanart':  img_link(name, 'fanart'),
            'mode':    mode,
            'title':   addon.getLocalizedString(title).encode('utf-8'),
            'plot':    addon.getLocalizedString(plot).encode('utf-8'),
            'url':     url
        })
    xbmcplugin.endOfDirectory(addon_handle)

# Main menu
if mode is None:
    mode = ['main_menu']
    addDir({
        'name':    'live',
        'thumb':   img_link('live', 'thumb'),
        'fanart':  img_link('live', 'fanart'),
        'mode':    'play',
        'title':   '[COLOR blue]' + addon.getLocalizedString(30001).encode('utf-8') + '[/COLOR]',
        'plot':    addon.getLocalizedString(30002).encode('utf-8'),
        'url':     stream_url[xbmcplugin.getSetting(addon_handle,'res_stream')],
    })
    showMenu(main_menu)

# TV Programmes menu
elif mode[0] == 'tvshows':
    showMenu(tvshows)

# List videos with NEXT link
elif mode[0] == 'lastvids+next':
    page = readPage(site_url + re.sub(r'.html', '/pc30.html', furl[0]))
    match = re.compile('<span class="date" >.+</span>\n'
                       '<a href="(.+?)"').findall(page)
    llast = flevel * 12
    if llast > len(match): llast = len(match)
    for lnum in range(llast - 12, llast):
        addVideoDir(match[lnum])
    if llast < len(match):
        addDir({
            'name':     fname[0],
            'thumb':    img_link('folder', 'thumb'),
            'fanart':   img_link(fname[0], 'fanart'),
            'mode':     'lastvids+next',
            'title':    '[B][COLOR blue]>> ' + addon.getLocalizedString(30101).encode('utf-8') + '... (' + str(flevel+1) + ')[/COLOR][/B]', # Next
            'plot':     addon.getLocalizedString(30102),
            'url':      furl[0]
        })
    xbmcplugin.endOfDirectory(addon_handle)

# List videos with ARCHIVE link
elif mode[0] == 'lastvids+archive':
    page = readPage(site_url + furl[0])
    match = re.compile('<span class="date" >.+</span>\n'
                       '<a href="(.+?)"').findall(page)

    for url in match:
        addVideoDir(url)
    addDir({
        'name':    fname[0],
        'thumb':   img_link('folder', 'thumb'),
        'fanart':  img_link(fname[0], 'fanart'),
        'mode':    'allvids_archive',
        'title':   '[B][COLOR blue]' + addon.getLocalizedString(30103).encode('utf-8') + '. ' + ftitle[0] + '[/COLOR][/B]', # Archive
        'plot':    addon.getLocalizedString(30104).encode('utf-8'),
        'url':     furl[0]
    })
    xbmcplugin.endOfDirectory(addon_handle)

# List ARCHIVE
elif mode[0] == 'allvids_archive':
    page = readPage(site_url + re.sub(r'.html', '/pc1000.html', furl[0]))
    match1 = re.compile('</a>\n<div class="content">\n'
                        '<span class="date" >(.+?)</span>\n'
                        '<a href="(.+?)" >\n<h4>\n').findall(page)
    for date, url in match1:
        addDir({
            'name':    fname[0],
            'thumb':   img_link('folder', 'thumb'),
            'fanart':  img_link(fname[0], 'fanart'),
            'mode':    'video',
            'title':   date,  # +' | '+ftitle[0],
            'plot':    ftitle[0],
            'url':     url
        })
    xbmcplugin.endOfDirectory(addon_handle)

# List ONE video from archive
elif mode[0] == 'video':
    addVideoDir(furl[0])
    xbmcplugin.endOfDirectory(addon_handle)

# Set default view
if xbmcplugin.getSetting(addon_handle, 'default_view') == 'true':
    try:
        xbmc.executebuiltin('Container.SetViewMode(' + default_view[xbmc.getSkinDir()][mode[0]] + ')')
    except:
        pass