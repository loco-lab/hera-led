#!/usr/bin/env python3
#Author: Mickey Horn
#Live status script for HERA LED model. Ran automatically at startup via systemd.

import time
from neopixel import *
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import math
import random
#import matplotlib.pyplot as plt
#import matplotlib.colors as clr

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# LED strip configuration:
LED_COUNT      = 350     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# antenna number : LED number
scheme = {
    0:10, 1:9, 2:8, 3:7, 4:6, 5:5, 6:4, 7:3, 8:2, 9:1, 10:0,
    11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19, 20:20, 21:21,
    22:119,
    23:32, 24:31, 25:30, 26:29, 27:28, 28:27, 29:26, 30:25, 31:24, 32:23, 33:22,
    34:118, 35:120,
    36:33, 37:34, 38:35, 39:36, 40:37, 41:38, 42:39, 43:40, 44:41, 45:42, 46:43,
    47:117, 48:121, 49:139,
    50:54, 51:53, 52:52, 53:51, 54:50, 55:49, 56:48, 57:47, 58:46, 59:45, 60:44,
    61:116, 62:122, 63:138, 64:140,
    65:55, 66:56, 67:57, 68:58, 69:59, 70:60, 71:61, 72:62, 73:63, 74:64, 75:65,
    76:115, 77:123, 78:137, 79:141, 80:159,
    81:76, 82:75, 83:74, 84:73, 85:72, 86:71, 87:70, 88:69, 89:68, 90:67, 91:66,
    92:114, 93:124, 94:136, 95:142, 96:158, 97:160,
    98:77, 99:78, 100:79, 101:80, 102:81, 103:82, 104:83, 105:84, 106:85, 107:86, 108:87,
    109:113, 110:125, 111:135, 112:143, 113:157, 114:161, 115:179,
    116:98, 117:97, 118:96, 119:95, 120:94, 121:93, 122:92, 123:91, 124:90, 125:89, 126:88,
    127:112, 128:126, 129:134, 130:144, 131:156, 132:162, 133:178, 134:180,
    135:99, 136:100, 137:101, 138:102, 139:103, 140:104, 141:105, 142:106, 143:107, 144:108, 145:109,
    146:111, 147:127, 148:133, 149:145, 150:155, 151:163, 152:177, 153:181, 154:199,
    155:309, 156:310, 157:311, 158:312, 159:313, 160:314, 161:315, 162:316, 163:317, 164:318, 165:319,
    166:110, 167:128, 168:132, 169:146, 170:154, 171:164, 172:176, 173:182, 174:198, 175:200,
    176:308, 177:307, 178:306, 179:305, 180:304, 181:303, 182:302, 183:301, 184:300, 185:299, 186:298,
    187:129, 188:131, 189:147, 190:153, 191:165, 192:175, 193:183, 194:197, 195:201,
    196:287, 197:288, 198:289, 199:290, 200:291, 201:292, 202:293, 203:294, 204:295, 205:296, 206:297,
    207:130, 208:148, 209:152, 210:166, 211:174, 212:184, 213:196, 214:202,
    215:286, 216:285, 217:284, 218:283, 219:282, 220:281, 221:280, 222:279, 223:278, 224:277, 225:276,
    226:149, 227:151, 228:167, 229:173, 230:185, 231:195, 232:203,
    233:265, 234:266, 235:267, 236:268, 237:269, 238:270, 239:271, 240:272, 241:273, 242:274, 243:275,
    244:150, 245:168, 246:172, 247:186, 248:194, 249:204,
    250:264, 251:263, 252:262, 253:261, 254:260, 255:259, 256:258, 257:257, 258:256, 259:255, 260:254,
    261:169, 262:171, 263:187, 264:193, 265:205,
    266:243, 267:244, 268:245, 269:246, 270:247, 271:248, 272:249, 273:250, 274:251, 275:252, 276:253,
    277:170, 278:188, 279:192, 280:206,
    281:242, 282:241, 283:240, 284:239, 285:238, 286:237, 287:236, 288:235, 289:234, 290:233, 291:232,
    292:189, 293:191, 294:207,
    295:221, 296:222, 297:223, 298:224, 299:225, 300:226, 301:227, 302:228, 303:229, 304:230, 305:231,
    306:190, 307:208,
    308:220, 309:219, 310:218, 311:217, 312:216, 313:215, 314:214, 315:213, 316:212, 317:211, 318:210,
    319:209
}

# clock hands
hourhand01 = [319,298,297,276,275,254,253,232,231]
hourhand02 = [110,131,152,173,194]
hourhand03 = [110,128,132,146,154,164,176,182,198]
hourhand04 = [110,127,134,143,158]
hourhand05 = [110,111,112,113,114,115,116,117,118]
hourhand06 = [109,86,63,40,17]
hourhand07 = [109,89,85,69,61,49,37,29,13]
hourhand08 = [109,90,83,72,57]
hourhand09 = [109,108,107,106,105,104,103,102,101,100]
hourhand10 = [319,300,293,282,267]
hourhand11 = [319,299,295,279,271,259,247,239,223]
hourhand12 = [319,296,273,250,227]
hourhands = [hourhand01,hourhand02,hourhand03,hourhand04,hourhand05,hourhand06,hourhand07,hourhand08,hourhand09,hourhand10,hourhand11,hourhand12]

sec_ring = [214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,180,179,160,159,140,139,120,119,0,1,2,3,4,5,6,7,8,9,10,11,32,33,54,55,76,77,98,99,309,308,287,286,265,264,243,242,221,220,219,218,217,216,215]

secs_dict = { # correlates the second with a point on the edge
    '00':214, '01':213, '02':212, '03':211, '04':210,
    '05':209, '06':208, '07':207, '08':206, '09':205,
    '10':204, '11':203, '12':202, '13':201, '14':200,
    '15':199, '16':180, '17':179, '18':160, '19':159,
    '20':140, '21':139, '22':120, '23':119, '24':0,
    '25':1, '26':2, '27':3, '28':4, '29':5,
    '30':6, '31':7, '32':8, '33':9, '34':10,
    '35':11, '36':32, '37':33, '38':54, '39':55,
    '40':76, '41':77, '42':98, '43':99, '44':309,
    '45':308, '46':287, '47':286, '48':265, '49':264,
    '50':243, '51':242, '52':221, '53':220, '54':219,
    '55':218, '56':217, '57':216, '58':215, '59':215
}

def clear():
# Turns off all LEDs.
    for i in range(LED_COUNT): strip.setPixelColorRGB(i,0,0,0)
    strip.show()

def colorscale(mag,cmin,cmax):
# Returns a tuple of floats between 0 and 255 for RGB, scaling from green to yellow.
    try: x = float(mag-cmin)/(cmax-cmin) # scales from 0 to 1
    except ZeroDivisionError: x=0.5 # cmax==cmin
    r = int(x*255)
    g = 255
    b = int(75-(x*75))
    return r,g,b

def ant_status_scaling():
# Reads the live antenna status csv from HERAnow and outputs appropriate colors for each antenna. The worst dipole is always shown.
    status = np.array(pd.read_csv('http://heranow.reionization.org/media/ant_stats.csv', header=0, names=['Ant','Pol','Constructed','Node','Fem Switch','Apriori','Spectra','PAM Power','ADC Power','ADC RMS','FEM IMU Theta','FEM IMU Phi','EQ Coeffs']))
    e_status = np.empty((0,13))
    n_status = np.empty((0,13))
    
    for i in status:
        antnum = i[0]
        antpol = i[1]
        if antpol=='e' and -1<antnum<320: e_status = np.append(e_status,[i],axis=0)
        elif antpol=='n' and -1<antnum<320: n_status = np.append(n_status,[i],axis=0)
    
    for j in range(320):
        e_constructed = e_status[j][2]
        n_constructed = n_status[j][2]
        e_spectra = e_status[j][6]
        n_spectra = n_status[j][6]

        if e_constructed==False or n_constructed==False: strip.setPixelColorRGB(scheme[j],0,0,0) # not built, off
        else:
            if pd.isnull(e_spectra)==True or pd.isnull(n_spectra)==True: strip.setPixelColorRGB(scheme[j],0,127,255) # offline, blue
            elif int(float(e_spectra))>=-45 and int(float(n_spectra))>=-45:
                avg_spectra = (float(e_spectra)+float(n_spectra))/2
                r,g,b = colorscale(avg_spectra,-100,-10)
                print(r,g,b)
                strip.setPixelColorRGB(scheme[j],r,g,b) #good, scaled green to yellow
            elif int(float(e_spectra))<-45 or int(float(n_spectra))<-45: strip.setPixelColorRGB(scheme[j],255,50,0) # bad, red
            elif int(float(e_spectra))>-20 or int(float(n_spectra))>-20: strip.setPixelColorRGB(scheme[j],255,50,0) # bad, red
            #else: strip.setPixelColorRGB(scheme[j],0,0,0) # not in csv, off

    strip.show()
    seconds = str(datetime.now().time())[6:8]
    for k in sec_ring: strip.setPixelColorRGB(secs_dict[seconds],200,200,200)
    strip.show()    
    time.sleep(.75)

# main code
print('Starting')
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

try:
    while True:
        ant_status_scaling()

except KeyboardInterrupt:
    if args.clear:
        print('Clear')
        clear()
