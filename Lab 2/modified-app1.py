from spyre import server
import pickle
import math

dict_month = {
    1: '01 Січень', 2: '02 Лютий', 3: '03 Березень', 4: '04 Квітень', 5: '05 Травень', 6: '06 Червень',
    7: '07 Липень', 8: '08 Серпень', 9: '09 Вересень', 10: '10 Жовтень', 11: '11 Листопад', 12: '12 Грудень'}



class Lab2App(server.App):
    title = "Vegetation Data"

    inputs = [{"type": 'dropdown',
               "label": 'Company',
               "options": [{"label": "VHI", "value": "VHI"},
                           {"label": "TCI", "value": "TCI"},
                           {"label": "VCI", "value": "VCI"}],
               "key": 'col',
               },
              {"type": 'dropdown',
               "label": 'Region',
               "options": [{"label": "Вінницька область", "value": "Вінницька область"},
                           {"label": "Волинська область", "value": "Волинська область"},
                           {"label": "Дніпропетровська область", "value": "Дніпропетровська область"},
                           {"label": "Донецька область", "value": "Донецька область"},
                           {"label": "Житомирська область", "value": "Житомирська область"},
                           {"label": "Закарпатська область", "value": "Закарпатська область"},
                           {"label": "Запорізька область", "value": "Запорізька область"},
                           {"label": "Івано-Франківська область", "value": "Івано-Франківська область"},
                           {"label": "Київська область", "value": "Київська область"},
                           {"label": "Кіровоградська область", "value": "Кіровоградська область"},
                           {"label": "Луганська область", "value": "Луганська область"},
                           {"label": "Львівська область", "value": "Львівська область"},
                           {"label": "Миколаївська область", "value": "Миколаївська область"},
                           {"label": "Одеська область", "value": "Одеська область"},
                           {"label": "Полтавська область", "value": "Полтавська область"},
                           {"label": "Рівенська область", "value": "Рівенська область"},
                           {"label": "Сумська область", "value": "Сумська область"},
                           {"label": "Тернопільська область", "value": "Тернопільська область"},
                           {"label": "Харківська область", "value": "Харківська область"},
                           {"label": "Херсонська область", "value": "Херсонська область"},
                           {"label": "Хмельницька область", "value": "Хмельницька область"},
                           {"label": "Черкаська область", "value": "Черкаська область"},
                           {"label": "Чернівецька область", "value": "Чернівецька область"},
                           {"label": "Чернігівська область", "value": "Чернігівська область"},
                           {"label": "Республіка Крим", "value": "Республіка Крим"},
                           {"label": "ALL", "value": "ALL"}],
               "key": 'reg',
               },
              {
                  "type": 'text',
                  "label": 'Weeks from',
                  "value": '1',
                  "key": 'wf',
              },
              {
                  "type": 'text',
                  "label": 'Weeks to',
                  "value": '52',
                  "key": 'wt',
              }
              ]

    controls = [{"type": "button",
                 "label": "refresh",
                 "id": "update_data"}]

    tabs = ["Table", "Plot", "AverageWeekPlot", "AverageMonthPlot"]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": False,
                "sortable": True},
               {
                   "type": "plot",
                   "id": "plot1",
                   "control_id": "update_data",
                   "tab": "Plot",
                   "on_page_load": False},
               {
                   "type": "plot",
                   "id": "plot2",
                   "control_id": "update_data",
                   "tab": "AverageWeekPlot",
                   "on_page_load": False,
               },
               { "type": "plot",
                   "id": "plot3",
                   "control_id": "update_data",
                   "tab": "AverageMonthPlot",
                   "on_page_load": False}
               ]
    @staticmethod
    def mont(x):
        m = math.ceil(x / 4.34)  # округляем вверх
        t = dict_month[m]
        y = t
        return y

    def getData(self, params):
        col = str(params['col'])
        with open('pickledata.p', 'rb') as fh:  # you need to use 'rb' to read
            df1 = pickle.load(fh)
        df = df1[['Year', 'Week', 'Region', f'{col}']]
        df['Month'] = df['Week'].apply(Lab2App.mont)
        reg = str(params['reg'])
        wf = float(params['wf'])
        wt = float(params['wt'])
        if reg != 'ALL':
            df = df.loc[df['Region'] == f'{reg}']
        self.df = df.loc[(df['Week'] >= wf) & (df['Week'] <= wt)]
        print("df finished")
        return self.df

    def plot1(self, params):
        reg = str(params['reg'])
        col = str(params['col'])
        df = self.getData(params)
        df1 = df[['Year', 'Region', f'{col}']]
        fig = df1.set_index('Year').plot()
        fig.set_ylabel(f'{col}')
        fig.set_title(f'{reg}')
        return fig

    def plot2(self, params):
        reg = str(params['reg'])
        col = str(params['col'])
        df = self.getData(params)
        df1 = df[['Year', 'Week', 'Region', f'{col}']]
        df1 = df1.groupby(['Week']).mean()
        print(df1)
        fig = df1.plot()
        fig.set_ylabel(f'{col}')
        fig.set_title(f'{reg}')
        return fig

    def plot3(self, params):
        reg = str(params['reg'])
        col = str(params['col'])
        df = self.getData(params)
        df1 = df[['Year', 'Month', 'Region', f'{col}']]
        df1 = df1.groupby(['Month']).mean()
        print(df1)
        fig = df1.plot()
        fig.set_ylabel(f'{col}')
        fig.set_title(f'{reg}')
        return fig


app = Lab2App()
app.launch(port=8087)
