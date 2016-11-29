# -*- coding: UTF-8 -*-
import sys, os
import urllib, urlparse
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import urllib2, re

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
main_menu = ([['lastvids+next', '[B]Эфиры [/B]', 'folder', '/z/17317.html', 'Эфиры телепередач'],
              ['tvshows', '[B]Телепередачи[/B]', 'folder', '', 'Все телепередачи'],
              ['lastvids+next', '[B]Все видео[/B]', 'folder', '/z/17192.html', 'Все видео'],
              ['lastvids+next', '[B]Видео: Кадры дня[/B]', 'folder', '/z/17226.html', 'Кадры дня'],
              ['lastvids+next', '[B]Видео: Репортажи[/B]', 'folder', '/z/17318.html', 'Репортажи'],
              ['lastvids+next', '[B]Видео: Интервью[/B]', 'folder', '/z/17319.html', 'Мнения']
              ])
tvshows = ([['lastvids+archive', 'Час Тимура Олевского', 'olevski', '/z/20333.html',
             'Ежедневная телепередача \"Час Тимура Олевского\".\n'
             'Час Тимура Олевского – это самые интересные и важные события, за которыми следит команда наших журналистов. Мы не бежим за новостями, а находим их для вас. Мы показываем все точки зрения и рассказываем обо всем, что случилось в конце рабочего дня. С понедельника по пятницу.\n'
             ],
            ['lastvids+archive', 'Настоящее Время - Европа', 'nveurope', '/z/18657.html',
             'Ежедневная телепередача \"Настоящее Время\".'
             ],
            ['lastvids+archive', 'Настоящее Время – Азия', 'nvasia', '/z/17642.html',
             'Ежедневная телепередача \"Настоящее Время – Азия\".'
             ],
            ['lastvids+archive', 'Настоящее Время – Америка', 'nvamerica', '/z/20347.html',
             'Ежедневная телепередача \"Настоящее Время – Америка\".'
             ],
            ['lastvids+archive', 'Смотри в оба', 'oba', '/z/20366.html',
             'Еженедельная передача \"Смотри в оба\".'
             ],
            ['lastvids+archive', 'Итоги', 'itogi', '/z/17499.html',
             'Еженедельная итоговая телепередача \"Итоги\" (по субботам).'
             ],
            ['lastvids+archive', 'Неделя', 'week', '/z/17498.html',
             'Еженедельная итоговая телепередача \"Неделя\" (по воскресеньям).'
             ],
            ['lastvids+archive', 'Балтия. Неделя', 'baltia', '/z/20350.html',
             'Еженедельная итоговая передача \"Балтия. Неделя\" (по субботам).'
             ],
            ['lastvids+archive', 'Бизнес-план', 'bisplan', '/z/20354.html',
             'Еженедельная передача \"Бизнес-план\".'
             ],
            ['lastvids+archive', 'Неизвестная Россия', 'unknownrus', '/z/20331.html',
             'Цикл \"Неизвестная Россия\".'
             ],
            ['lastvids+archive', 'Ждем в гости', 'guests', '/z/20330.html',
             'Ждем в гости с Зурабом Двали.'
             ]
            ])
default_view = {
    'skin.confluence': {'main_menu': '50', 'tvshows': '500', 'lastvids+next': '515', 'lastvids+archive': '515',
                        'allvids_archive': '51', 'video': '51'},
    'skin.aeon.nox.5': {'main_menu': '50', 'tvshows': '50', 'lastvids+next': '510', 'lastvids+archive': '510',
                        'allvids_archive': '50', 'video': '510'},
    'skin.estuary': {'main_menu': '502', 'tvshows': '500', 'lastvids+next': '502', 'lastvids+archive': '502',
                     'allvids_archive': '55', 'video': '502'}
}
# Confuence ('51') "BigList" FullWidthList view,
# Confuence ('50') "BigList" FullWidthList view
# Confuence ('500'  "Thumbnails" view
# Confuence ('515') "MediInfo3" MediaListView4 view


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

mode = args.get('mode', None)
furl = args.get('folderurl', None)
ftitle = args.get('title', None)
flevel = int(args.get('level', '0')[0])
fname = args.get('name', None)
site_url = 'http://www.currenttime.tv'
ptv = xbmcaddon.Addon('plugin.video.currenttime.tv')

xbmcplugin.setContent(addon_handle,
                      'tvshows')  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# xbmcplugin.setPluginCategory(addon_handle), 'tv') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def img_link(name, type):
    if type == 'fanart' or type == 'poster':
        ext = '.jpg'
    else:
        ext = '.png'
    image = os.path.join(ptv.getAddonInfo('path'), "resources/media/" + name + '_' + type + ext)
    return image


def addDir(arg):
    li = xbmcgui.ListItem(label=arg['title'])
    if arg['mode'] != 'play':
        arg['url'] = build_url(
            {'mode': arg['mode'], 'title': arg['title'], 'name': arg['name'], 'level': str(flevel + 1),
             'folderurl': arg['url']})
        isFolder = True
        li.setProperty("IsPlayable",
                       "false")  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    else:
        isFolder = False
        li.setProperty("IsPlayable",
                       "false")  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    info = {
        'mediatype': 'tvshow',
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
    arg = {
        'name': fname[0],
        'thumb': re.sub(r'_w\w+', '_w512_r1.jpg', match1[0][1]),
        'fanart': re.sub(r'_w\w+', '_w1280_r1.jpg', match1[0][1]),
        'mode': 'play',
        'title': re.sub('&quot;', '"', match_title[0]),
        'plot': re.sub('&quot;', '"', match_plot[0]),
        'url': re.sub('/master.m3u8', video_url[xbmcplugin.getSetting(addon_handle, 'res_video')], match1[0][0])
    }
    addDir(arg)


def readPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page


def showMenu(menu):
    for mode, title, name, url, plot in menu:
        arg = {
            'name': name,
            'thumb': img_link(name, 'thumb'),
            'fanart': img_link(name, 'fanart'),
            'mode': mode,
            'title': title,
            'plot': plot,
            'url': url
        }
        addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)


if mode is None:  # Main menu
    mode = ['main_menu']
    arg = {
        'name': 'live',
        'thumb': img_link('live', 'thumb'),
        'fanart': img_link('live', 'fanart'),
        'mode': 'play',
        'title': '[B][COLOR blue]Прямой эфир[/COLOR][/B]',
        'plot': 'Круглосуточный телеканал "Настоящее Время" - прямая трасляция онлайн',
        'url': stream_url[xbmcplugin.getSetting(addon_handle,'res_stream')],
    }
    addDir(arg)
    showMenu(main_menu)

elif mode[0] == 'tvshows':
    showMenu(tvshows)

elif mode[0] == 'lastvids+next':
    page = readPage(site_url + re.sub(r'.html', '/pc30.html', furl[0]))
    match = re.compile('<span class="date" >.+</span>\n'
                       '<a href="(.+?)"').findall(page)
    llast = flevel * 12
    if llast > len(match): llast = len(match)
    for lnum in range(llast - 12, llast):
        addVideoDir(match[lnum])
    if llast < len(match):
        arg = {
            'name': fname[0],
            'thumb': img_link('folder', 'thumb'),
            'fanart': img_link(fname[0], 'fanart'),
            'mode': 'lastvids+next',
            'title': '[B][COLOR blue]>> Дальше... (' + str(flevel + 1) + ')[/COLOR][/B]',
            'plot': '',
            'url': furl[0]
            }
        addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'lastvids+archive':
    page = readPage(site_url + furl[0])
    match = re.compile('<span class="date" >.+</span>\n'
                       '<a href="(.+?)"').findall(page)

    for url in match:
        addVideoDir(url)
    arg = {
        'name': fname[0],
        'thumb': img_link('folder', 'thumb'),
        'fanart': img_link(fname[0], 'fanart'),
        'mode': 'allvids_archive',
        'title': '[B][COLOR blue]Архив. ' + ftitle[0] + '[/COLOR][/B]',
        'plot': 'Видео за все даты',
        'url': furl[0]
    }
    addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'allvids_archive':
    page = readPage(site_url + re.sub(r'.html', '/pc1000.html', furl[0]))
    match1 = re.compile('</a>\n<div class="content">\n'
                        '<span class="date" >(.+?)</span>\n'
                        '<a href="(.+?)" >\n<h4>\n').findall(page)
    for date, url in match1:
        arg = {
            'name': fname[0],
            'thumb': img_link('folder', 'thumb'),
            'fanart': img_link(fname[0], 'fanart'),
            'mode': 'video',
            'title': date,  # +' | '+ftitle[0],
            'plot': ftitle[0],
            'url': url
        }
        addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'video':
    addVideoDir(furl[0])
    xbmcplugin.endOfDirectory(addon_handle)

if xbmcplugin.getSetting(addon_handle, 'default_view') == 'true':
    try:
        xbmc.executebuiltin('Container.SetViewMode(' + default_view[xbmc.getSkinDir()][mode[0]] + ')')
    except:
        pass
