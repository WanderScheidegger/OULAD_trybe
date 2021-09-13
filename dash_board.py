# http://127.0.0.1:8050/

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#dataset studentInfo.csv
studentInfo = pd.read_csv('data/studentInfo.csv', sep=',', encoding='ISO-8859-1')

studentInfo['final_result_2'] = studentInfo['final_result'].apply(lambda x: 'Reprovado' if \
(x == 'Withdrawn' or x == 'Fail') else 'Aprovado')

# -----------------------------------------------------------------------------------------------------------------------------------

modulo = studentInfo.groupby('code_module').agg({'id_student':'count'}).reset_index().\
    rename(columns={"code_module": "Modulo", 'id_student': 'Qtde'})

modulo['Percentual'] = modulo.apply(lambda x: round(100 * (x['Qtde'] / modulo['Qtde'].sum()),2), axis=1)
    
fig_modulo = px.bar(modulo, x='Modulo', y='Qtde', \
    text='Percentual', color='Modulo',  hover_data=['Qtde'],\
        template="seaborn")

fig_modulo.update_layout(
    margin=dict(l=20, r=50, t=50, b=20),
    title = 'Distribuição - Módulo Cursado',
    xaxis_title="Módulo Cursado",
    yaxis_title="Quantidade [Alunos]",
    legend_title="Módulo Cursado",
    width=600, 
    height=400,
    uniformtext_minsize=10, 
    uniformtext_mode='hide',
)

# -----------------------------------------------------------------------------------------------------------------------------------

df = studentInfo.groupby(['code_module', 'final_result']).agg({'id_student':'count'}).reset_index().\
    rename(columns={"code_module": "Modulo", "final_result": 'Resultado','id_student': 'Qtde'})

df['Percentual'] = df.apply(lambda x:  round(100 * (x['Qtde'] / df[df['Resultado'] == x['Resultado']]['Qtde'].sum()),2), axis=1)

fig_modulo_2 = px.bar(df, x="Resultado", y="Percentual", text="Percentual", color="Modulo",
            hover_data=['Percentual'], barmode = 'stack', template="seaborn")

fig_modulo_2.update_layout(
    margin=dict(l=20, r=50, t=50, b=20),
    title = 'Resultados por Módulo Cursado',
    xaxis_title="Resultado",
    yaxis_title="Percentual [%]",
    legend_title="Módulo Cursado",
    width=700, 
    height=500,
    uniformtext_minsize=9, 
    uniformtext_mode='hide',
)

# -----------------------------------------------------------------------------------------------------------------------------------


app.layout = html.Div(children=[
    html.H1(children='OULAD Dataset'),

    html.Div(children='''
        Análise Exploratória dos dados.
    '''),

    dcc.Graph(
        id='modulo-curso',
        figure=fig_modulo
    ),

    dcc.Graph(
        id='modulo_2-curso',
        figure=fig_modulo_2
    )

])


if __name__ == '__main__':
    app.run_server(debug=True)

