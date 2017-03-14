import ReadFrame
from spyre import server
import pandas as pd


frame = ReadFrame.read_to_frame('doc/')
provinces = {
        1: 'Cherkasy', 2: 'Chernihiv', 3: 'Chernivtsi', 4: 'Crimea', 5: 'Dnipropetrovs`k', 6: 'Donets`k',
        7: 'Ivano-Frankivs`k', 8: 'Kharkiv', 9: 'Kherson', 10: 'Khmel`nyts`kyy', 11: 'Kiev', 12: 'Kiev City',
        13: 'Kirovohrad', 14: 'Luhans`k', 15: 'Lviv', 16: 'Mykolayiv', 17: 'Odessa', 18: 'Poltava', 19: 'Rivne',
        20: 'Sevastopol`', 21: 'Sumy', 22: 'Ternopil`', 23: 'Transcarpathia', 24: 'Vinnytsya', 25: 'Volyn`',
        26: 'Zaporizhzhya', 27: 'Zhytomyr'
}

class WebApplication(server.App):
    title = "Visual Analysis"
    inputs = [{
            "input_type":'dropdown',
            "label":'Province',
            "options":[
                {'label':i,'value':j } for j,i in provinces.items() #list generator
                         ],
            "variable_name":'province',
            "control_id":'list'
                },

        {
            "input_type": 'dropdown',
            "label": 'Index',
            "options": [
                {'label':'VHI', 'value':'VHI'},
                {'label':'VCI', 'value':'VCI'},
                {'label':'TCI', 'value':'TCI'}
                ],
            "variable_name": 'index',
            "control_id": 'list'
        },

        {
            "input_type": 'dropdown',
            "label": 'Year',
            "options": [
                {'label': i, 'value': i} for i in range(1981,2018) # list generator
                        ],
            "variable_name": 'with_year',
            "control_id": 'list'},

        {
            "input_type": 'dropdown',
            "label": 'With: (week)',
            "options": [
                {'label': i, 'value': i} for i in range(1, 53)  # list generator
                ],
            "variable_name": 'with_week',
            "control_id": 'list'},

        {
            "input_type": 'dropdown',
            "label": 'To: (week)',
            "options": [
                {'label': i, 'value': i} for i in range(1, 53)  # list generator
                ],
            "variable_name": 'to_week',
            "control_id": 'list'
        }

    ]

    controls = [{
        "control_type": 'button',
        "label": 'Update!',
        "control_id": 'list'
                }]

    tabs = ["Table", "Plot"]  # add tabs

    outputs = [
        {
            "output_type": 'table',
            "control_id": 'list',
            "output_id": 'getData',
            "tab": 'Table',
            "on_page_load": True
        },

        {
            "output_type": 'plot',
            "output_id": 'plot_id',
            "control_id": 'list',
            "tab": 'Plot',
            "on_page_load": True
        }

    ]

    def getData(self, params):
        province_id = int(params['province'])
        index = params['index']
        with_year = int(params['with_year'])
        with_week = int(params['with_week'])
        to_week = int(params['to_week'])

        df = frame[frame['province_id']==province_id]
        df = df[df['year'] == with_year]
        df = df[df['week'] >= with_week]
        df = df[df['week'] <= to_week]
        if index=='VHI':
            df = df.drop(['province_id', 'SMN', 'SMT', 'VCI', 'TCI','year'], axis=1)
        if index=='VCI':
            df = df.drop(['province_id', 'SMN', 'SMT', 'VHI', 'TCI','year'], axis=1)
        if index=='TCI':
            df = df.drop(['province_id', 'SMN', 'SMT', 'VCI', 'VHI','year'], axis=1)
        return df

    def getPlot(self, params):
        data = params['index']
        df_1 = self.getData(params)
        plt_obj_1 = df_1.plot(x='week', y=data, kind='scatter')
        fig = plt_obj_1.get_figure()
        return fig
app = WebApplication()
app.launch()



