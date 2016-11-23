# -*- coding: UTF-8 -*-
import sys, os
import urllib, urlparse
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import urllib2, re

main_menu = ([['play', 'Прямой эфир', 'live', 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/master.m3u8',
               'Круглосуточный телеканал Настоящее Время - прямая трасляция онлайн'
              ],
              ['last_vids_fldr', 'Последние эфиры', 'lastall', '/z/17317.html',
               'Эфиры телепередач за последние несколько деней.'
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

mode = args.get('mode', None)
furl = args.get('folderurl', None)
ftitle = args.get('title', None)

site_url = 'http://www.currenttime.tv'
ptv = xbmcaddon.Addon('plugin.video.currenttime.tv')

xbmcplugin.setContent(addon_handle, 'tvshows')
xbmcplugin.setPluginCategory(int(sys.argv[1]), 'tv')


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

def addVideoDir(url):
    page = readPage(site_url + url)
    match1 = re.compile('<a class="html5PlayerImage" href="(.+?)">\n'
                        '<img src="(.+?)"').findall(page)
    match_title = re.compile('<meta name="title" content="(.+?)" />').findall(page)
    match_plot = re.compile('<meta name="description" content="(.+?)" />', re.DOTALL).findall(page)
    if len(match_plot) < 1: match_plot = [' ']
    arg = {
        'thumb': re.sub(r'_w\w+', '_w512_r1.jpg', match1[0][1]),
        'fanart': re.sub(r'_w\w+', '_w1920_r1.jpg', match1[0][1]),
        'mode': 'play',
        'title': re.sub('&quot;', '"', match_title[0]),
        'plot': re.sub('&quot;', '"', match_plot[0]),
        'url': match1[0][0]

    }
    addDir(arg)


def readPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page



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
    match = re.compile('width-img size-[2|3]">\n'
                       '<a href="(.+?)"\n'
                       'class="img-wrapper"').findall(page)
    for url in match:
        addVideoDir(url)

    if ftitle[0] != 'Последние эфиры':
        arg = {'thumb': img_link('live', 'thumb'),
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
    addVideoDir(furl[0])

    xbmcplugin.endOfDirectory(addon_handle)

