#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AMIU copyleft 2021
# Roberto Marzocchi

'''
Lo script interroga il WS di Aebi Schmidt per recuperare i messaggi per ciascun serial number 
'''


import os, sys, getopt, re  # ,shutil,glob

import argparse
import requests
from requests.exceptions import HTTPError




import json


import inspect, os.path

import datetime


import psycopg2
import sqlite3


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

sys.path.append('../')
from credenziali import *

#import requests
import datetime

import logging

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

#tmpfolder=tempfile.gettempdir() # get the current temporary directory
logfile='{}/messaggi.log'.format(path)
errorfile='{}/error_messaggi.log'.format(path)
#if os.path.exists(logfile):
#    os.remove(logfile)

'''logging.basicConfig(
    #handlers=[logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')],
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    #filemode='w', # overwrite or append
    #fileencoding='utf-8',
    #filename=logfile,
    level=logging.DEBUG)
'''


# Create a custom logger
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
    ]
)

logger = logging.getLogger()

# Create handlers
c_handler = logging.FileHandler(filename=errorfile, encoding='utf-8', mode='w')
f_handler = logging.StreamHandler()
#f_handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')


c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.DEBUG)


# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


cc_format = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')

c_handler.setFormatter(cc_format)
f_handler.setFormatter(cc_format)




def main():


    #################################################################
    logger.info('Connessione al db SIT')
    conn = psycopg2.connect(dbname=db,
                        port=port,
                        user=user,
                        password=pwd,
                        host=host)

    curr = conn.cursor()
    #conn.autocommit = True
    #################################################################

    query_select="SELECT id FROM spazz_schmidt.serialnumbers"
    try:
        curr.execute(query_select, ())
        serialnumbers=curr.fetchall()
    except Exception as e:
        logger.error(e)

    for sn in serialnumbers:
        logging.debug(sn[0])

        #################################################################
        logger.info("Mi connetto al WS {0} per leggere i messaggi della spazzatrice con SN {1}". format(url_schmidt, sn[0]))
        api_url='{0}SerialNumbers/{1}/Messages'.format(url_schmidt, sn[0])
        from requests.auth import HTTPBasicAuth
        auth=HTTPBasicAuth(user_schmidt, pwd_schmidt)
        response = requests.get(api_url, auth=auth, headers={'accept': 'text/json'})
        logger.info("Status code: {0}".format(response.status_code))
        try:      
            response.raise_for_status()
            # access JSOn content
            #jsonResponse = response.json()
            #print("Entire JSON response")
            #print(jsonResponse)
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
            check=500
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
            logger.error(response.json())
            check=500
        letture = response.json()
        i=0
        while i<len(letture):
            colonne=letture[i]
            #logger.debug(len(colonne))
            #logger.debug(colonne)
            logger.debug(letture[i])
            id=letture[i]['id']
            header=letture[i]['header']
            if header==None:
                logger.debug('Non leggo nulla')
            else: 
                #"driverId": "string",
                #"driver2Id": "string",
                #"routeId": "string",
                driverid=letture[i]['header']['driverId']
                driver2id=letture[i]['header']['driver2Id']
                routeId=letture[i]['header']['routeId']
            logger.debug('***************************************************')
            vehicleRoute=letture[i]['vehicleRoute']
            logger.debug(vehicleRoute)
            lat=letture[i]['vehicleRoute']['geoLat']
            #DD = int(float(lat)/100)
            #SS = float(lat) - DD * 100
            #latdec=DD + SS/60
            # valido per latitudini positive
            if lat[-1]=='N':
                lat=lat.replace('N','')
                latdec=int(float(lat)/100) + (float(lat) - int(float(lat)/100) * 100)/60
            elif lat[-1]=='S':
                lat=lat.replace('S','')
                latdec=-int(float(lat)/100) + (float(lat) - int(float(lat)/100) * 100)/60
            else:
                logger.error('Problem with latitude')
            lon=letture[i]['vehicleRoute']['geoLon'].replace('E', '')
            londec=int(float(lon)/100) + (float(lon) - int(float(lon)/100) * 100)/60
            logger.debug('lat = {0}, lon = {1}'.format(latdec, londec))
            print(datetime.datetime.now())
            data=letture[i]['vehicleRoute']['sysDate']
            ora=letture[i]['vehicleRoute']['sysTime']
            sweepermode=letture[i]['sweeper']['swprMode']
            
            
            """ query_select="SELECT * FROM spazz_schmidt.serialnumbers where id = %s"
            try:
                curr.execute(query_select, (id,))
                serialnumbers=curr.fetchall()
            except Exception as e:
                logger.error(e)
            curr.close()
            curr = conn.cursor()
            # se c'è già la entry faccio 
            if len(serialnumbers)>0: 
                query_update='''UPDATE spazz_schmidt.serialnumbers
                set manuf_id=%s, equip_id=%s
                WHERE id=%s;'''
                try:
                    curr.execute(query_update, (letture[i]['manufId'], letture[i]['equipId'], letture[i]['id']))
                except Exception as e:
                    logger.error(e)
            else:
                query_insert='''INSERT INTO spazz_schmidt.serialnumbers
    (manuf_id, equip_id, id)
    VALUES(%s, %s, %s);'''
                try:
                    curr.execute(query_insert, (letture[i]['manufId'], letture[i]['equipId'], letture[i]['id']))
                except Exception as e:
                    logger.error(e)
            ########################################################################################
            # da testare sempre prima senza fare i commit per verificare che sia tutto OK
            conn.commit()
            ######################################################################################## """
            logger.debug('Mode = {}'.format(sweepermode))
            exit()
            i+=1
    

    
   
    logger.info("Chiudo definitivamente la connesione al DB")
    curr.close()
    conn.close()
    
    
    #while i
    
    
    
    
if __name__ == "__main__":
    main() 