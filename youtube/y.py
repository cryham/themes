#!/usr/bin/python3
# -*- coding: utf-8 -*-

#  Script creates web.html with list of playlists
#  for my website: https://cryham.org/entertainment/playlists/
#  From y.html file, which is saved from:
#  https://www.youtube.com/channel/UCzFcqUTGAUqpaNk4k7BQg6w/playlists?view=1&sort=lad
#  Keep PgDn to bottom until all playlists are loaded.

import os
import re
import datetime
from operator import itemgetter, attrgetter
import string
printable = set(string.printable)


#  const
#------------------------
groups = [
    # keyword,  group name,  title in html
    ['----', 'other', 'Other'],  # default
    ['drift', 'car', 'Car 🚗🚀'],
    ['offroad', 'car', ''],
    ['rally', 'car', ''],

    ['movie','movies', 'Movies 🎥🎬📺'],
    ['fun',  'fun',   'Fun 😂😀😜'],
    ['tiktok', 'fun', ''],
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
    ['black met','black ⬛️', ''],
    ['melodic',  'melodic 🌀', ''],
    ['symphonic','symphonic 🌌', ''],
    ['gothic',   'gothic 🎻', ''],
    ['power',    'power 🌋', ''],
    ['metal',    'Heavy 💣', ''],

    ['poppunk', 'popPunk 🍀', 'PopPunk 🍀'],
    ['punk',    'popPunk 🍀', ''],

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
    print('%02d' % i + ' - ' + g[0] + ' - ' + g[1])


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

typ = 0
vids = 0  # count of videos in playlist

#  foreach line  --------
for line in lines:

# type 1: first 30:
#     __text">204 videos</div>
#     title="Fun 😂 - Various, Internet 🌎"><a href="https://www.youtube.com/watch?v=xa94N7rcHfs&amp;list=PLF7rhUP3syrYmUY1sFCk_VxUku8EqkBMs&amp;pp=gAQB" class="yt-

# type 2: later, more 160:
#     ">41 videos</yt-formatted-string>
#     ytd-grid-playlist-renderer" href="https://www.youtube.com/watch?v=M8uPvX2te0I&amp;list=PLF7rhUP3syrbtvog6yaC0uxb0bMUxN6ZW&amp;pp=gAQB" title="🎈Pop">

    #  get videos count, is before title and url  ----
    r = re.match(r'.*>(\d+) videos</div>', line)
    if r:
        vids = r.groups()[0]
        #print('type 1: '+ vids)
        typ = 1
    else:
        r = re.match(r'.*>(\d+) videos</yt-formatted-string>', line)
        if r:
            vids = r.groups()[0]
            #print('type 2: '+ vids)
            typ = 2
    
    #  get title and url  ----
    if typ == 1:
        r = re.match(r'.*title="(.*)"><a href="(.*)" class.*', line)
        if r:
            # print(line)
            playlists += 1
            title = r.groups()[0]
            url = r.groups()[1]
            #print(title+' '+line)
            pls.append(Plist(title, url, vids))
            typ = 0
            vids = 0
    elif typ == 2:
        r = re.match(r'.*<a id="video-title".*href="(.*)".*title="(.*)".*', line)
        if r:
            # print(line)
            playlists += 1
            title = r.groups()[1]
            url = r.groups()[0]
            #print(title+' '+line)
            pls.append(Plist(title, url, vids))
            typ = 0
            vids = 0

spls = sorted(pls, key=attrgetter('group'))


#  print  ------------------------
date_str = datetime.datetime.today().strftime('%Y-%m-%d') # %H:%M')

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
print('Last updated on: {}'.format(date_str))


#  export html to file  ------------------------

expfile = open('web.html', 'w')
#expfile.write('<h1>Overview</h1>\n')
expfile.write('This page gathers my playlists from my <a href="https://www.youtube.com/channel/UCzFcqUTGAUqpaNk4k7BQg6w/playlists?view=1&sort=lad" target="_blank" rel="noopener">youtube channel.</a>\n')
expfile.write('<em>Because browsing them all there is hopeless. Grouping and sorting by name is impossible, etc.</em>\n\n')
expfile.write('Total playlists: {}\n'.format(playlists))
expfile.write('Total videos: {}\n\n'.format(videos))
expfile.write('Last updated on: {}\n'.format(date_str))
expfile.write('&nbsp;\n<hr />\n\n')
expfile.write('<h1>Movies, Fun, Games, Nature</h1>\n')
g = ''
for p in spls:
    if g != p.group2:
        g = p.group2
        gg = p.group3
        if gg != '':
            if gg[0:3] == 'Cov':  # Covers - start of Music
                expfile.write('<h1>Music</h1>\n')
            expfile.write('<h2>{}</h2>\n'.format(gg))
        expfile.write('<h3>{}</h3>\n'.format(g))

    #expfile.write('<a href="{}">{}</a>\n'.format(p.url, p.title))
    expfile.write('<a href="{}">{} - ({})</a>\n'.format(p.url, p.title, p.videos))
expfile.close()
