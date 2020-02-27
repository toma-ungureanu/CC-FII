#!C:/Users/Tomy/AppData/Local/Programs/Python/Python37/python.exe
# coding=utf-8
import calendar
import time

print("Content-Type: text/html")
print()

import cgi, cgitb, requests, json

cgitb.enable()  # for debugging
form = cgi.FieldStorage()

CITY_NAME = "cityName"
CACHED_INFO = "cachedInfo"
CITY_ID = "cityID"
LAST_DATE = "last_date"
FULL_RESPONSE = "fullResponse"


def get_service_info():
    info = str(form.getvalue('info')).replace("\"", "")
    if int(form.getvalue('serviceID')) == 1:
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        first_service_handler(base_url, info)
    elif int(form.getvalue('serviceID')) == 2:
        base_url = f"https://restcountries-v1.p.rapidapi.com/name/{info}"
        second_service_handler(base_url, info)


def second_service_handler(base_url, info):
    json_response = create_request_second_service(base_url)
    if json_response.find(b"\"status\":404") != -1:
        print("<p>Country not found!</p>")
        return

    start = json_response.find(b",\"ja\":\"")
    end = json_response.find(b",\"it")
    json_response = newdata = json_response[:start] + json_response[end:]
    decoded = json.loads(json_response.decode())[0]
    print("<p>")
    print("Capital: " + decoded["capital"])
    print("</p>")

    print("<p>")
    print("Population: " + str(decoded["population"]))
    print("</p>")

    print("<p>")
    print("Region: " + str(decoded["region"]))
    print("</p>")

    print("<p>")
    print("Timezones: " + str(decoded["timezones"]))
    print("</p>")

    print("<p>")
    print("Borders: " + str(decoded["borders"]))
    print("</p>")

    print("<p>")
    print("Latitude & longitude: " + str(decoded["latlng"]))
    print("</p>")


def create_request_second_service(base_url):

    headers = {
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
        'x-rapidapi-key': "d2eebe0e8dmshb06f545ce899f3fp152b22jsn392f1f1323d7"
    }

    response = requests.get(url=base_url, headers=headers)

    return response.content


def first_service_handler(base_url, info):
    # read api key
    fd = open("../config/weatherApiKey.txt", "r")
    api_key = fd.read()

    fd = open("../config/city.list.json", "r", encoding="utf8", errors='ignore')
    city_list = json.load(fd)
    # print(city_list[0])

    elem_index = check_cache(info)
    cached_fd = open("../config/cached.json", encoding="utf8", errors='ignore', mode="r+")
    cached_list = json.load(cached_fd)
    cached_fd.close()

    if elem_index is not -1 and elem_index is not -2:
        now = calendar.timegm(time.gmtime())
        if now > int(cached_list[elem_index][CACHED_INFO][LAST_DATE]):
            response_json = create_request_first_service(info, api_key, base_url)
            list.remove(cached_list, cached_list[elem_index])
            cache_response(info, response_json)
            pretty_print(cached_list, elem_index)
        else:
            pretty_print(cached_list, elem_index)
    elif elem_index is -1:
        response_json = create_request_first_service(info, api_key, base_url)
        cache_response(info, response_json)
        pretty_print(cached_list, elem_index)

    else:
        print(info)
        print("City not found!")


def pretty_print(cached_list, elem_index):
    i = 0
    print("<div class=weatherParent>")
    for index in range(0, int(len(cached_list[elem_index][CACHED_INFO][FULL_RESPONSE]) / 2), 3):
        i += 1
        elem = cached_list[elem_index][CACHED_INFO][FULL_RESPONSE][index]
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(elem['dt'])))
        print(f"<div class=weather{i}>")
        print("<p>")
        print("Time: " + str(date_time))
        print("</p>")

        print("<p>")
        print("Feels like: " + str(elem['main']['feels_like']) + "&#176C", end='')
        print("</p>")

        print("<p>")
        print("Minimum temperature: " + str(elem['main']['temp_min']) + "&#176C", end='')
        print("</p>")

        print("<p>")
        print("Maximum temperature: " + str(elem['main']['temp_max']) + "&#176C", end='')
        print("</p>")

        print("<p>")
        print("Humidity: " + str(elem['main']['humidity']) + "%", end='')
        print("</p>")

        print("<br></br>")
        print("</div>")

    print("")
    print("</div>")


def check_cache(info):
    city_list_fd = open("../config/city.list.json", "r", encoding="utf8", errors='ignore')
    city_list = json.load(city_list_fd)
    city_list_fd.close()

    found_in_city_list = False
    for elem in city_list:
        if str.lower(elem['name']) == str.lower(info):
            found_in_city_list = True
            break

    if found_in_city_list:
        cached_fd = open("../config/cached.json", encoding="utf8", errors='ignore', mode="r+")
        cached_list = json.load(cached_fd)
        cached_fd.close()

        for index in range(len(cached_list)):
            if info == cached_list[index][CITY_NAME]:
                return index
        return -1
    else:
        return -2


def create_request_first_service(info, api_key, base_url):
    params = {'q': info, 'units': 'metric', 'appid': api_key}

    response = requests.get(url=base_url, params=params)
    return response.json()


def cache_response(info, response_json):
    cached_fd = open("../config/cached.json", encoding="utf8", errors='ignore', mode="r+")
    cached_list = json.load(cached_fd)
    to_cache = {
        CITY_NAME: info,
        CACHED_INFO:
            {
                CITY_ID: response_json['city']['id'],
                LAST_DATE: response_json['list'][-1]['dt'],
                FULL_RESPONSE: response_json['list']
            }
    }

    cached_fd.seek(0)
    cached_fd.truncate()
    cached_list.append(to_cache)
    cached_fd.write(json.dumps(cached_list))
    cached_fd.write("\n")
    cached_fd.close()


get_service_info()
