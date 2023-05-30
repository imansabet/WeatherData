import tkinter as tk
import requests
import time

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title('Weather app')
        width, height = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry(f'{width}x{height}')

        # create entry widget for city name
        self.city_entry = tk.Entry(master, font=('Century 12'), width=40)
        self.city_entry.insert(0, 'Enter city name then click button')
        self.city_entry.bind("<FocusIn>", lambda args: self.city_entry.delete('0', 'end'))
        self.city_entry.pack(pady=30)

        # create button to get weather data
        self.get_weather_btn = tk.Button(master, text="Get Data", fg="blue", command=self.show_data)
        self.get_weather_btn.pack()

    def show_data(self):
        city_name = self.city_entry.get()

        try:
            # Remove previously displayed labels
            for widget in self.master.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.destroy()

            # make API request and get weather data
            data = self.get_data(city_name)

            # update label widgets with weather data
            for k, v in self.process_data(data).items():
                tk.Label(self.master, text=f'{k}: {v}', font=('Century 15 bold')).pack(pady=15)

        except Exception as e:
            # if there is an error, show error message
            error_label = tk.Label(self.master, text=f"nothing found for : {city_name}", font=('Century 15 bold'))
            error_label.pack(pady=20)

    def process_data(self, data):
        city = data["name"]
        date_time = time.ctime(data['dt'])
        temp = int(data["main"]["temp"] - 273.15)
        humidity = data["main"]["humidity"]
        return {"city": city, "date & time": date_time, "temp °C": temp, "humidity": humidity}

    def get_data(self, city='tehran', API_KEY='e0d7468c1d5cf1c1b75133f7a80a02d7'):
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        res = requests.get(url=URL)
        return res.json()


if __name__ == '__main__':
    root = tk.Tk()
    weather_app = WeatherApp(root)
    root.mainloop()