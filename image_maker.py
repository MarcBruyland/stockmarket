import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

FOLDER = "static/images/"



def create_image(name, sym, result, exchange, cur):
    # Data for plotting: {2023-03-22: {'close': 200.8, 'volume': 18656.0, 'exchange': 'XBRU'}, ..}
    keys = list(result.keys())
    start_eod = keys[0]
    last_eod = keys[-1]
    nr_of_points = len(keys)
    print(start_eod, last_eod, nr_of_points)

    lst_x = []
    lst_y = []
    i = 0
    for dt, dic in result.items():
        lst_x.append(dt)
        lst_y.append(dic['close'])
        i += 1
    x = np.array(lst_x)
    y = np.array(lst_y)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.xticks(rotation=30)  # rotates the x labels (otherwise they overlapped)
    ax.set(xlabel=f'date (from {start_eod} to {last_eod})', ylabel=f'EOD price in {cur}', title=f'{sym} - {name} on {exchange}')
    ax.grid()  #adds a grid to the chart

    # avoiding overlapping x labels: only show a label for i = 0, 10, 20, ..
    i = 0
    for label in ax.get_xaxis().get_ticklabels():
        if i % 10:
            label.set_visible(False)
        i += 1

    plt.tight_layout()  # solves issue that x labels were not completely visible

    filename = "chart.png"
    fig.savefig(FOLDER+filename)
    #plt.show()
    return filename



