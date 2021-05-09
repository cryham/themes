#!/usr/bin/python3
# -*- coding: utf-8 -*-

#  Script creates web.html with list of playlists
#  for my website: https://cryham.tuxfamily.org/playlists/
#  From y.html file, which is saved from:
#  https://www.youtube.com/channel/UCzFcqUTGAUqpaNk4k7BQg6w/playlists?view=1&sort=lad
#  Keep PgDn to bottom until all playlists are loaded.

import os
import re
from operator import itemgetter, attrgetter
import string
printable = set(string.printable)


#  const
#------------------------
groups = [
    # keyword,  group name,  title in html
    ['----', 'other', 'Other 🚗🚀'],  # default
    ['fun',  'fun',   'Fun 😂😀😜'],
    ['games','games', 'Games 🖥️🕹️'],

    ['birds', 'nature', 'Nature 🌺🍁🌳🌲🏔️🏝️'],
    ['flower','nature', ''],
    ['nature','nature', ''],
    ['travel','nature', ''],

    ['full',    'full 🎚️', 'Covers &nbsp; 🎸🥁🎚️🎹'],
    ['original','original 🎚️', ''],
    ['metal cov','original 🎚️',''],
    ['drum',  'drum 🥁', ''],
    ['guitar','guitar 🎸', ''],
    ['covers','piano 🎹', ''],

    ['folk',     'folk 🎻', 'Metal &nbsp; 🌀🌌🔮⬛️🌋🎻'],
    ['black',    'black ⬛️', ''],
    ['melodic',  'melodic 🌀', ''],
    ['symphonic','symphonic 🌌', ''],
    ['gothic',   'gothic 🎻', ''],
    ['power',    'power 🌋', ''],
    ['metal',    'Heavy 💣', ''],

    ['punkrock', 'punkRock 🍀', 'PunkRock 🍀'],
    ['punk',     'punkRock 🍀', ''],

    ['rock old',  'rock Old', 'Rock 🗻'],
    ['poprock',  'rock Old', ''],
    ['soundtracks','soundtracks', ''],
    ['rammst',   'rock 🇩🇪,🇵🇱', ''],
    ['deutsch',  'rock 🇩🇪,🇵🇱', ''],
    ['polish',   'rock 🇩🇪,🇵🇱', ''],
    ['rock',     'rock 🗻', ''],
    
    ['techno','trance Old ✨️🌜', 'Trance &nbsp; ✨️🌟🆕'],
    ['trance 199','trance Old ✨️🌜', ''],
    ['trance 200','trance Old ✨️🌜', ''],
    ['trance','trance 🌟🆕', ''],

    ['eurodance','eurodance', 'Eurodance 💃, Other 🎈'],
    ['pop',      'other', ''],
    ['dubstep',  'other', ''],
    ['classical','other', ''],
    ['keygen',   'other', '']]
#------------------------

#  groups test
i = 0
for g in groups:
    i += 1
    #print('%02d' % i + ' - ' + g[0] + ' - ' + g[1])


#  item  title, url, group
#------------------------------------------------
class Plist:
    def __init__(self, title, url, vids):
        self.title = title
        self.url = url
        #  cleaned title from unicode chars
        t = "".join(filter(lambda x: x in printable, title))
        self.clean = t
        self.videos = vids
        
        i = 0  # default
        self.group = '%02d' % i + groups[0][1] + '| '
        self.group2 = groups[0][1].capitalize()
        self.group3 = groups[0][2]
        for g in groups:
            i += 1  # find group by keyword
            if g[0] in t.lower():
                self.group = '%02d' % i + g[1] + '| '
                self.group2 = g[1].capitalize()
                self.group3 = g[2]
                break
        self.group = self.group + t

    def get_name(self):
        return self.url


#  open file  ------------------------
file = open('y.html', 'r')
lines = file.readlines()

playlists = 0
pls = []
vids = 0  # count of videos in playlist
for line in lines:
    r = re.match(r'.*yt-formatted-string class="style-scope ytd-thumbnail-overlay-side-panel-renderer.*>(\d+)<', line)
    if r:
        vids = r.groups()[0]
        #print(vids)
    r = re.match(r'.*<a id="video-title".*title="(.*)".*href="(.*)".*', line)
    if r:
        playlists += 1
        title = r.groups()[0]
        url = r.groups()[1]
        pls.append(Plist(title, url, vids))

spls = sorted(pls, key=attrgetter('group'))


#  print  ------------------------
g = ''
videos = 0  # all count
for p in spls:
    if g != p.group2:
        g = p.group2
        if p.group3 != '':
            print('\n=== {}'.format(p.group3))
        print('\n--- {}'.format(p.group2))
    #print('{}\n{}\n{}'.format(p.group, p.title, p.url))
    #print('{}\n{}'.format(p.title, p.url))
    print('{} - ({})'.format(p.title, p.videos))
    videos += int(p.videos)
    #print('{}'.format(p.clean))
    
print('\nTotal playlists: {}'.format(playlists))
print('Total videos: {}'.format(videos))


#  export html to file  ------------------------
expfile = open('web.html', 'w')
expfile.write('<h1>Overview</h1>\n')
expfile.write('<p>Total playlists: {}</p>\n'.format(playlists))
expfile.write('<p>Total videos: {}</p>\n'.format(videos))
expfile.write('<h1>Fun, Games, Nature</h1><br />\n')
g = ''
for p in spls:
    if g != p.group2:
        g = p.group2
        gg = p.group3
        if gg != '':
            if gg[0:3] == 'Cov':  # Covers - start of Music
                expfile.write('<h1>Music</h1><br />\n')
            expfile.write('<h2>{}</h2><br />\n'.format(gg))
        expfile.write('<h3>{}</h3><br />\n'.format(g))

    #expfile.write('<a href="{}">{}</a><br />\n'.format(p.url, p.title))
    expfile.write('<a href="{}">{} - ({})</a><br />\n'.format(p.url, p.title, p.videos))
expfile.close()
