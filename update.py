import requests
import os
import pandas
import json

url = "http://api.openweathermap.org/data/2.5/forecast?id=<OpenWeatherMap ID)&units=imperial&zip=<zip code>,us"

# Make a get request to get the latest position of the international space station from the opennotify api.
print(url)

response = requests.get(url)
print("Response: " + str(response.status_code))

patterns = pandas.read_csv('weather_patterns.csv', index_col='ID')
forecast = response.json()

outfile = open('latest_weather.json', "w+")
json.dump(forecast, outfile)

def get_temp_color():
    if (temp < 60):
        return "AQUA"
    elif (temp > 60 and temp < 80):
        return "BLUE"
    elif (temp >= 70 and temp < 80):
        return "YELLOW"
    elif (temp >= 80 and temp < 90):
        return "ORANGE"
    elif (temp >= 90 and temp < 100):
        return "RED"


weather = int(forecast["list"][0]["weather"][0]["id"])
temp = forecast["list"][0]["main"]["temp"]

print(forecast["list"][0]["dt_txt"])
print(patterns.loc[weather])
report_file = open(os.path.join("f:", "latest.txt"), "w+")
report_file.write(forecast["list"][0]["dt_txt"] + "\n")
report_file.writelines(str(patterns.loc[weather]) + "\n")
report_file.write("Temperature: %f\n" % temp)
report_file.write("Temp Color: " + get_temp_color() + "\n")

# report_file.writelines(str(patterns.loc[dt_txt]))
report_file.close()

animation_file = open(os.path.join("f:", "animation.txt"), "w+")
if weather == 999:
    animation_file.write("test_pattern()\r\n")
elif weather == 800:
    color = get_temp_color()
    animation_file.write("fill_up(" + color + ", " + str(patterns.loc[weather]["Speed"]) + ")\r\n")
    animation_file.write("erase_down(" + color + ", " + str(patterns.loc[weather]["Speed"]) + ")\r\n")
else:
    pattern = patterns.loc[weather]["Pattern"]
    color = patterns.loc[weather]["Color"]
    speed = str(patterns.loc[weather]["Speed"])
    animation_file.write(patterns.loc[weather]["Pattern"] + "(" + color + ", " + speed + ")\r\n")

animation_file.close()
