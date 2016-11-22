# -*- coding: UTF-8 -*-
import sys, os
import urllib, urlparse
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import urllib2, re

main_menu = ([['play', 'Прямой эфир', 'live', 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/master.m3u8',
               'Круглосуточный телеканал Настоящее Время - прямая трасляция онлайн'
              ],
              ['last_vids_fldr', 'Час Тимура Олевского', 'olevski', '/z/20333.html',
               'Ежедневная телепередача \"Час Тимура Олевского\".\n'
               'Час Тимура Олевского – это самые интересные и важные события, за которыми следит команда наших журналистов. Мы не бежим за новостями, а находим их для вас. Мы показываем все точки зрения и рассказываем обо всем, что случилось в конце рабочего дня. С понедельника по пятницу.\n'
              ],
              ['last_vids_fldr', 'Настоящее Время', 'nv', '/z/18657.html',
               'Ежедневная телепередача \"Настоящее Время\".'
               ],
              ['last_vids_fldr', 'Настоящее Время – Азия', 'nvasia', '/z/17642.html',
               'Ежедневная телепередача \"Настоящее Время – Азия\".'
               ],
              ['last_vids_fldr', 'Настоящее Время – Америка', 'nvamerica', '/z/20347.html',
               'Ежедневная телепередача \"Настоящее Время – Америка\".'
               ],
              ['last_vids_fldr', 'Смотри в оба', 'oba', '/z/20366.html',
               'Еженедельная передача \"Смотри в оба\".'
               ],
              ['last_vids_fldr', 'Итоги', 'itogi', '/z/17499.html',
               'Еженедельная итоговая телепередача \"Итоги\" (по субботам).'
               ],
              ['last_vids_fldr', 'Неделя', 'week', '/z/17498.html',
               'Еженедельная итоговая телепередача \"Неделя\" (по воскресеньям).'
               ],
              ['last_vids_fldr', 'Балтия. Неделя', 'baltia', '/z/20350.html',
               'Еженедельная итоговая передача \"Балтия. Неделя\" (по субботам).'
               ],
              ['last_vids_fldr', 'Бизнес-план', 'bisplan', '/z/20354.html',
               'Еженедельная передача \"Бизнес-план\".'
               ],
              ['last_vids_fldr', 'Неизвестная Россия', 'unknownrus', '/z/20331.html',
               'Цикл \"Неизвестная Россия\".'
               ]])

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'tvshows')
xbmcplugin.setPluginCategory(int(sys.argv[1]), 'tv')

site_url = 'http://www.currenttime.tv'
ptv = xbmcaddon.Addon('plugin.video.currenttime.tv')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def img_link(name, type):
    if type == 'fanart' or type == 'poster': ext = '.jpg'
    else:                             ext = '.png'
    image = os.path.join(ptv.getAddonInfo('path'), "resources/media/"+name+'_'+type+ext)
    return image

def addDir(arg):
    li = xbmcgui.ListItem(label=arg['title'], iconImage=img_link('default','icon'))
    if arg['mode'] != 'play':
        arg['url'] = build_url({'mode': arg['mode'],'title': arg['title'], 'folderurl': arg['url']})
        isFolder = True
    else:
        isFolder = False
        #li.setProperty("IsPlayable", "true")
    info = {
        'plot': arg['plot'],
    }
    li.setInfo('video', info)

    li.setArt({'thumb': arg['thumb'], 'fanart': arg['fanart']})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=arg['url'], listitem=li, isFolder=isFolder)
    return ok

def readPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page

mode = args.get('mode', None)
furl = args.get('folderurl', None)
ftitle = args.get('title', None)

if mode is None:
    for mode, title, name, url, plot in main_menu:
        arg = {
            'thumb': img_link(name, 'thumb'),
            'fanart': img_link(name, 'fanart'),
            'mode': mode,
            'title': title,
            'plot': plot,
            'url': url
        }
        addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'last_vids_fldr':
    page = readPage(site_url + furl[0])
    match1 = re.compile('<div class="thumb listThumb thumb16_9">\n'
                       '<img data-src="" src="(.+?_tv.+?jpg)" alt="(.+?)">\n'
                       '</div>\n<i class="ico ico-video"></i>\n'
                       '</a>\n<div class="content">\n'
                       '<span class="date" >(.+?)</span>\n'
                       '<a href="(.+?)" >\n<h4>\n'
                       '<span class="title">(.+?)</span>\n'
                       '</h4>\n<p>(.+?)</p>').findall(page)
    for img, altname, date, url, title, plot in match1:
        page = readPage(site_url + url)
        match2 = re.compile('<a class="html5PlayerImage" href="(.+?)"').findall(page)
        arg = {
            'thumb': re.sub(r'_w\w+', '_w512_r1.jpg', img),
            'fanart': re.sub(r'_w\w+', '_w1920_r1.jpg', img),
            'mode': 'video',
            'title': title,
            'plot': plot,
            'url': match2[0]
        }
        addDir(arg)

    arg = {
        'thumb': img_link('live', 'thumb'),
        'fanart': img_link('live', 'fanart'),
        'mode': 'all_vids_fldr',
        'title': '>>>... Архив. '+ ftitle[0],
        'plot': 'Видео за все даты',
        'url': furl[0]
    }
    addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'all_vids_fldr':
    page = readPage(site_url + re.sub(r'.html', '/pc1000.html', furl[0]))
    match1 = re.compile('</a>\n<div class="content">\n'
                       '<span class="date" >(.+?)</span>\n'
                       '<a href="(.+?)" >\n<h4>\n').findall(page)
    for date, url in match1:
        arg = {
            'thumb': img_link('live', 'thumb'),
            'fanart': img_link('live', 'fanart'),
            'mode': 'video',
            'title': date+' | '+ftitle[0],
            'plot': '',
            'url': url
        }
        addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'video':
    page = readPage(site_url + furl[0])
    match1 = re.compile('<a class="html5PlayerImage" href="(.+?)">\n'
                       '<img src="(.+?)"').findall(page)
    match2 = re.compile('<meta name="title" content="(.+?)" />\n'
                        '<meta name="description" content="(.+?)"').findall(page)
    arg = {
            'thumb': re.sub(r'_w\w+', '_w512_r1.jpg', match1[0][1]),
            'fanart': re.sub(r'_w\w+', '_w1920_r1.jpg', match1[0][1]),
            'mode': 'play',
            'title': match2[0][0],
            'plot': match2[0][1],
            'url': match1[0][0]
        }
    addDir(arg)
    xbmcplugin.endOfDirectory(addon_handle)

