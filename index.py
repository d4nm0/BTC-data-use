import locale
import seaborn as sns

from flask import Flask, render_template
from helper import Helper

app = Flask(__name__)
helper = Helper()
color = sns.color_palette()

app.config.from_object('config')


@app.route('/')
def index():
    bitcoin_price   = helper.get_data_csv('input/bitcoin_price.csv', ";", '%b %d, %Y')
    bitcoin_dataset = helper.get_data_csv('input/bitcoin_dataset.csv', ";", '%d/%m/%Y 00:00')

    bitcoin_data = bitcoin_dataset.merge(bitcoin_price, on='Date')
    bitcoin_data['moving_avg'] = bitcoin_data['Close'].rolling(window=30).mean()

    bitcoin_graph = helper.create_graph({
        'title': "Bitcoin Price overtime",
        'xlabel': "Date",
        'ylabel': "Bitcoin Price",
        'size': {'width': 5, 'heigth': 4},
        'data': bitcoin_data,
        'xaxis': bitcoin_data.Date,
        'plots': {
            'moving_avg': {
                'color': 'red',
                'label': 'moving average(close price)'
            },
            'Close': {
                'color': 'blue',
                'label': 'closing price'
            }
        }
    })

    bitcoin_data = helper.get_rsi_data(bitcoin_data)

    rsi_graph = helper.create_graph({
        'title': "Bitcoin RSI overtime",
        'xlabel': "Date",
        'ylabel': "RSI Percent",
        'size': {'width': 5, 'heigth': 4},
        'data': bitcoin_data,
        'xaxis': bitcoin_data.index,
        'plots': {
            'rsi': {
                'color': 'green',
                'label': 'RSI'
            }
        }
    })

    resume_graph = helper.create_graph({
        'title': "Bitcoin price overtime (with RSI)",
        'xlabel': "",
        'ylabel': "",
        'size': {'width': 12, 'heigth': 3},
        'data': bitcoin_data,
        'xaxis': bitcoin_data.index,
        'plots': {
            'moving_avg': {
                'color': 'red',
                'label': 'moving average(close price)'
            },
            'close': {
                'color': 'blue',
                'label': 'closing price'
            },
            'rsi': {
                'color': 'green',
                'label': 'RSI'
            }
        }
    })

    twenty_graph = helper.create_graph({
        'title': "Bitcoin price 2020",
        'xlabel': "",
        'ylabel': "",
        'size': {'width': 12, 'heigth': 3},
        'data': bitcoin_data,
        'xaxis': bitcoin_data.index,
        'plots': {
            'moving_avg': {
                'color': 'red',
                'label': 'moving average(close price)'
            },
            'close': {
                'color': 'blue',
                'label': 'closing price'
            },
            'rsi': {
                'color': 'green',
                'label': 'RSI'
            }
        },
        'year': '2020'
    })
    
    return render_template('index.html', 
                            bitcoin_graph=bitcoin_graph,
                            rsi_graph=rsi_graph,
                            resume_graph=resume_graph,
                            twenty_graph=twenty_graph)

@app.route('/datatables')
def datatables():
    bitcoin_price   = helper.get_data_csv('input/bitcoin_price.csv', ";", '%b %d, %Y')
    bitcoin_dataset = helper.get_data_csv('input/bitcoin_dataset.csv', ";", '%d/%m/%Y 00:00')
    columns = {'btc_market_price': 'Market Price', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'moving_avg': 'Moving Average', 'rsi': 'RSI'}

    bitcoin_data = bitcoin_dataset.merge(bitcoin_price, on='Date')
    bitcoin_data['moving_avg'] = bitcoin_data['Close'].rolling(window=30).mean()
    bitcoin_data = helper.get_rsi_data(bitcoin_data)

    datatable = bitcoin_data[columns.keys()]
    datatable = datatable.rename_axis(None)
    datatable = datatable.rename(columns=columns)

    return render_template('tables/datatables.html', 
                            bitcoin_datatable=datatable.to_html())
    
if __name__ == "__main__":
    app.run()