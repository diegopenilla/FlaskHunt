import numpy as np
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')

def z_hunt(sequence, name):
    print('cwd')
    print(os.getcwd())
    # some preprocessing here
    DNA = sequence
    windowsize = 8
    minsize = 6
    maxsize = 8

    cwd = os.getcwd()
    nombre = '{}/results/{}'.format(cwd, name)
    #nombre = 'results/{}'.format(name)
    filename = '{}.txt'.format(nombre)

    output = "{}.Z-SCORE".format(filename)
    f = open(filename,"w+")
    f.write(DNA)
    f.close()
    # Defino los argumentos de z-hunt:
    zhunt_cmd = "{}/zhunt4.dms {} {} {} {}".format(cwd, windowsize, minsize, maxsize, filename)
    print(zhunt_cmd)
    zhunt_res = os.system(zhunt_cmd)
    print(zhunt_res)
    #Execute zhunt with the arguments windowsize, minsize, maxsize and datafile...


    #NOTE: LOAD RESULTS CSV FILE:
    data = pd.read_csv(output, names=['Unclear1','Unclear2','Z-Score','Conformation'], skiprows=1, sep='\s+')
    # Extracting Z-Scores
    y = list(np.array(data['Z-Score'])/1000) # Z-Scores in kb
    data['Z-Score'] = y # Replacing the column Z-Scores from data to y
    data.index = np.arange(1, len(data) + 1)
    data['DNA'] = DNA
    indexes = [i+1 for i in range(len(y))]
    data.round({'Unclear1':2, 'Unclear2':2, 'Z-Score':4})

    # ADD INFO TO SESSIONS => WHEN DATABASE
    def plot(name):
        plt.style.use('default')
        plt.figure(figsize = (8,8))
        indexes = [i for i in range(len(y))] # ! change it for df abstraction
        plt.xlabel(r"Position in DNA")
        plt.ylabel(r"Z-Score [kb]")
        p = plt.plot(indexes, y)
        plt.title('Score for {} DNA'.format(name))
        plt.savefig("./static/images/{}.png".format(name))
        plt.title('Z-Scores for {} DNA'.format(name))
        print('Plot saved in static/images')
        return None

    # makes a normal, requires to change arguments from results.html
    #plot(name)

    def plotlyb(name):
        import plotly.plotly as py
        import plotly.graph_objs as go
        import plotly
        plotly.tools.set_credentials_file(username='Chipichapes', api_key='L6ti8JP4PGxm4gkOqizP')

        datos = []
        # data of graph
        datos.append(go.Scattergl(x= indexes, y=list(data['Z-Score']), mode='lines+markers', name = name))


        layout = dict(title = 'Z-Scores for {}'.format(name),
                      xaxis = dict(title = 'Position in DNA'),
                      yaxis = dict(title = 'Z-Score [kb]'),
                      width=1000,
                    height=500
                      )

        fig = dict(data=datos, layout=layout)
        # returns URL of graph
        return py.plot(fig, filename='test', auto_open=False)

    plot(name='temp')
    url_image = plotlyb(name)
    return data, url_image
