#!/usr/bin/env python
'''
  11/30/2016
  Author: Makerbro
  Language: Python
  File: app.py
  ------------------------------------------------------------------------------
  Description:
  Code for YouTube video demonstrating how to use Python to send data to a
  webserver running on an ESP8266.
  https://youtu.be/CpWhlJXKuDg
  ------------------------------------------------------------------------------
  Please consider buying products from ACROBOTIC to help fund future
  Open-Source projects like this! We'll always put our best effort in every
  project, and release all our design files and code for you to use.

  https://acrobotic.com/
  ------------------------------------------------------------------------------
  License:
  Please see attached LICENSE.txt file for details.
'''
import sys, os, json, time


import httplib2



http = httplib2.Http()

if 0:
        url = 'http://192.168.1.103/'
        response, content = http.request(url, 'GET')
        print (response)
        print (content)

if 1:
        url_json = 'http://192.168.1.103/jblink'
        data = {'times': '1', 'pause': '1'}
        headers={'Content-Type': 'application/json; charset=UTF-8'}
        response, content = http.request(url_json, 'POST', headers=headers, body=json.dumps(data))
        http.request(url_json, 'POST', headers=headers, body=json.dumps(data))

        print (response)
        print (content)

if 0:
        import urllib
        url_query = 'http://192.168.1.103/qblink'
        data = {'times': '10', 'pause': '300'}
        headers={'Content-Type': 'application/json; charset=UTF-8'}
        response, content = http.request(url_query, 'POST', headers=headers, body=urllib.encode(data))
        print (response)
        print (content)
