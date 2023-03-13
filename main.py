from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
# start_date = "2021-12-31"
# city = "610116"
# city_name = "西安"
# pig_city = "110000"
# pig_city_name = "北京"
# birthday = "10-23"
# pig_birthday = "10-15"
#
# app_id = "wx4ca6f71d78aab518"
# app_secret = "1749a84a2c89036d57b13b1de24c107b"
#
# user_id = "oX1sI6GC9r8M1aYW9ucfGMUC9JxA"
# user_id_pig = "oX1sI6OG8ib14dv5Fzj3Dv2Xd1n4"
# template_id = "dvRvriBJD1hT7YeR6-MQHh74wwN2rgMi5ODGRCV8wZw"

start_date = os.environ['START_DATE']
city = os.environ['CITY']
city_name = os.environ['CITY_NAME']
pig_city = os.environ['PIG_CITY']
pig_city_name = os.environ['PIG_CITY_NAME']
birthday = os.environ['BIRTHDAY']
pig_birthday = os.environ['PIG_BIRTHDAY']

app_id = os.environ['APP_ID']
app_secret = os.environ['APP_SECRET']

user_id = os.environ['USER_ID']
user_id_pig = os.environ['USER_ID_PIG']
template_id = os.environ['TEMPLATE_ID']


def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=d38b5352dc107824ff7a345e210f55cf&city=" + city
    res = requests.get(url).json()
    weather = res['lives'][0]['weather']
    temperature = res['lives'][0]['temperature']
    wind = res['lives'][0]['winddirection']
    wind_power = res['lives'][0]['windpower']
    return weather, temperature, wind, wind_power


def get_pig_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=d38b5352dc107824ff7a345e210f55cf&city=" + pig_city
    res = requests.get(url).json()
    pig_weather = res['lives'][0]['weather']
    pig_temperature = res['lives'][0]['temperature']
    pig_wind = res['lives'][0]['winddirection']
    pig_wind_power = res['lives'][0]['windpower']
    return pig_weather, pig_temperature, pig_wind, pig_wind_power


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_pig_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + pig_birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, wind, wind_power = get_weather()
pig_wea, pig_temperature, pig_wind, pig_wind_power = get_pig_weather()
data = {"city": {"value": city_name, "color": get_random_color()},
        "weather": {"value": wea, "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "wind": {"value": wind, "color": get_random_color()},
        "wind_power": {"value": wind_power, "color": get_random_color()},
        "pig_city": {"value": pig_city_name, "color": get_random_color()},
        "pig_weather": {"value": pig_wea, "color": get_random_color()},
        "pig_temperature": {"value": pig_temperature, "color": get_random_color()},
        "pig_wind": {"value": pig_wind, "color": get_random_color()},
        "pig_wind_power": {"value": pig_wind_power, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "birthday_right": {"value": get_pig_birthday(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res_pig = wm.send_template(user_id_pig, template_id, data)
print(res)
print(res_pig)
