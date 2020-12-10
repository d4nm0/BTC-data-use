
import base64
import pandas as pd

from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from stockstats import StockDataFrame as Sdf
from datetime import datetime, date

class Helper():

    def get_data_csv(self, file, separator, date_format):
        csv_file = pd.read_csv(file, sep=separator)

        for i, row in csv_file.iterrows():
            dt = datetime.strptime(row['Date'], date_format)        
            dt = dt.strftime('%Y-%m-%d')
            row['Date'] = dt
            csv_file.at[i, 'Date'] = dt

        return csv_file

    def create_graph(self, config):
        twentytwenty = None
        fig = Figure(figsize=(config["size"]["width"], config["size"]["heigth"]))
        axis = fig.subplots()

        if 'year' in config:
            x3 = [datetime.strptime(d,'%Y-%m-%d').date() for d in config['xaxis'] if date(int(config['year']), 1, 1) <= datetime.strptime(d,'%Y-%m-%d').date() <= date(int(config['year']), 12, 31)]
            twentytwenty = pd.DataFrame([config['data'].loc[x.strftime("%Y-%m-%d")] for x in x3])
        else:
            x3 = [datetime.strptime(d,'%Y-%m-%d').date() for d in config['xaxis']]

        for plot in config['plots']:
            if 'year' in config:
                yaxis = twentytwenty[plot]
            else:
                yaxis = config['data'][plot]

            axis.plot(x3, yaxis, color=config['plots'][plot]['color'], label=config['plots'][plot]['label'])

        axis.set_xlabel(config['xlabel'], fontsize=12)
        axis.set_ylabel(config['ylabel'], fontsize=12)
        axis.set_title(config['title'], fontsize=20)
        axis.legend(loc='best')

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return base64.b64encode(buf.getbuffer()).decode("ascii")

    def get_rsi_data(self, data):
        stock_df = Sdf.retype(data)
        data['rsi'] = stock_df['rsi_14']

        del data['close_-1_s']
        del data['close_-1_d']
        del data['rs_14']
        del data['rsi_14']

        return data