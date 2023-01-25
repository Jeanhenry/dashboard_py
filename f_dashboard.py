# -*- coding:UTF-8 -*-

# https://dash.plotly.com/

from ssl import Options
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
import os
from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict
import base64


"""
    df_ano.reset_index(inplace=True, drop=True) # resetando o indice, mas sem que uma nova coluna seja adicionada ao dataframe

"""

############################################################################################
# BASE DE DADOS
# http://www.ispdados.rj.gov.br/estatistica.html
# Estatísticas de segurança: série histórica mensal por município desde 2014

############################################################################################
# VAMOS USAR A BASE ORIGINAL SEM SER PIVOT
caminho_pasta = os.getcwd()
caminho_pasta = f'C:\ESTUDOS\Dash02'
df_casos = pd.read_csv(f'{caminho_pasta}\\20220904_Jh_BaseMunicipioMensal.csv')

############################################################################################
# CRIA A LISTA
lt_anomes = sorted(df_casos['ANOMES'].unique().tolist(), key=int, reverse=True)
lt_municipio = sorted(df_casos['f_MUNICIPIO'].unique().tolist(), key=str, reverse=False)
lt_regiao = sorted(df_casos['REGIAO'].unique().tolist(), key=str, reverse=False)

lt_colunas = df_casos.columns.tolist()
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias
del lt_colunas[0] # remove as colunas desnecessarias

lt_casos_2 = sorted(lt_colunas, key=str, reverse=False)

lt_casos = {"AMEACA": "AMEACA","ESTELIONATO": "ESTELIONATO","ESTUPRO": "ESTUPRO",}
for item in lt_casos.values():
    primeiro_caso = f'{item}'
    break

############################################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#jean, nessa linha acima é um tema escolhido no site https://bootswatch.com/cyborg/

############################################################################################
# GRAFICO LINHAS ( VISÃO POR ANO )
df_casos_grafico = df_casos
df_casos_grafico = df_casos_grafico.groupby(["ANO"])[primeiro_caso].sum().reset_index()
fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_casos_grafico["ANO"], y=df_casos_grafico[primeiro_caso]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    #title_text = f'VISÃO ANO ACUMULADO | {primeiro_caso}', # adicionando titulo ao gráfico
    #title_x = 0.5
    )

############################################################################################
# GRAFICO COLUNAS ( VISÃO POR REGIAO )
#fig = px.bar(df_regiao, # data frame com os dados
#            x = 'Ano', # coluna para os dados do eixo x
#            y = 'Total', # coluna para os dados do eixo y
#            barmode = 'group', # setando que o gráfico é do tipo group
#            color = 'UF', # setando a coluna que irá serparar as colunas dentro do grupo
#            hover_name = 'UF', # coluna para setar o titulo do hover
#            )
#pyo.offline.plot(fig, filename = "bar-plot-01.html")


############################################################################################
# GRAFICO BARRAS ( REGIAO )
df_casos_regiao = df_casos
df_casos_regiao = df_casos_regiao.groupby(["REGIAO"])[primeiro_caso].sum().reset_index()
fig3 = go.Figure(layout={"template":"plotly_dark"})
fig3.add_trace(go.Bar(x=df_casos_regiao["REGIAO"], y=df_casos_regiao[primeiro_caso]))
fig3.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    title_text = f'VISÃO ANO ACUMULADO | {primeiro_caso}', # adicionando titulo ao gráfico
    title_x = 0.5, # reposicionando o titulo para que ele fique ono centro do gráfico
    ) 

image_filename = 'C:/ESTUDOS/Dash02/img/angra_dos_reis.svg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode() 

############################################################################################
# Layout 
app.layout = dbc.Container(
    children=[
        
        # CABEÇALHO
        dbc.Row(
            [
                dbc.Col(html.Div([html.Img(id="logo", src=app.get_asset_url("henry_analytics2.1.png"), height=50),],style={"background-color": "#1E1E1E",
                                                                                                                            "margin": "-25px",
                                                                                                                            "padding": "25px"}), md=4),
                dbc.Col(html.H3(children="BOLETIM de OCORRENCIAS | RIO DE JANEIRO"), md=6),
            ],align="start", className="g-0"        
        ),       

        # FILTRO
        dbc.Row(
            [
                #FILTRO POR ANOMES
                html.P("ANOMES", style={"margin-top": "20px"}),
                dbc.Col(html.Div(dcc.Dropdown(id="anomes-dropdown",
                                                options=lt_anomes,
                                                value=lt_anomes[0],
                                                style={'width' : '70%','height' : '20px',})), width=6, lg=4),
                
                #FILTRO POR MUNICIPIO
                html.P("MUNICIPIO", style={"margin-top": "20px"}),
                dbc.Col(html.Div(dcc.Dropdown(id="municipio-dropdown",
                                                options=lt_municipio,
                                                value=lt_municipio[0],
                                                style={'width' : '70%','height' : '20px',})), width=6, lg=4),
                
                #FILTRO OCORRENCIA ( casos )
                html.P("OCORRÊNCIA", style={"margin-top": "20px"}),
                dbc.Col(html.Div([dcc.Dropdown(id="casos-dropdown",
                                                options=[ {"label": j, "value": i} for i, j in lt_casos.items() ],
                                                value="AMEACA",
                                                style={'width' : '70%','height' : '20px',}),],), width=6, lg=4),

                #dbc.Carousel(
                #            items=[
                #                {"key": "1", "src": "C:/ESTUDOS/Dash02/img/img/angra_dos_reis.svg"},
                #                {"key": "2", "src": "C:/ESTUDOS/Dash02/img/img/angra_dos_reis.svg"},
                #                {"key": "3", "src": "C:/ESTUDOS/Dash02/img/img/angra_dos_reis.svg"},
                #            ],
                #            controls=False,
                #            indicators=False,
                #            interval=2000,
                #            ride="carousel",
                #        ),

            ]),
 
        # CARD 1
        dbc.Col(dbc.Col(dbc.Row([dbc.Card([dbc.CardBody([
            html.Span("OCORRÊNCIAS NO PERÍODO", className="card-text"),
            html.H2(style={"color": "#D2691E"}, id="qtd-ocorrencias-text"),
            html.Span("COMPARADO COM O MÊS ANTERIOR", className="card-text"),
            html.H5(style={"color": "#006400"}, id="perc-todos-casos-text"),
            ])]
                ,color="light"
                ,outline=True
                ,style={"height": "230px", #altura
                        "width": "230px", #largura
                        "margin-top": "-200px",
                        "margin-left": "310px",
                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "#FFFFFF"})]))),      

        #GRAFICO LINHAS (ano)
        dbc.Col(dbc.Col(dcc.Graph(id="graf_linhas",
                            figure=fig2,
                            style={"height": "190px", #altura
                                    "width": "230px", #largura
                                    "margin-top": "100px",
                                    "margin-left": "290px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "background-color": "#242424",
                                }),md=3)),

        #GRAFICO BARRAS
        dbc.Col(dbc.Col(dbc.Col(dcc.Graph(id="graf_colunas",
                            figure=fig3,
                            style={"height": "190px", #altura
                                    "width": "230px", #largura
                                    "margin-top": "100px",
                                    "margin-left": "450px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "background-color": "#242424",
                                }),md=3))),

    ], fluid=True, 
)

############################################################################################
# Interactivity

@app.callback([
        Output("qtd-ocorrencias-text", "children"),
        Output("perc-todos-casos-text", "children")
        ,], 
    [Input("anomes-dropdown", "value"), Input("casos-dropdown", "value"), Input("municipio-dropdown", "value")]
)

def display_status(anomes, casos, municipio):

    print(f'ANO: {str(anomes)[0:4]} || ANOMES: {anomes} || MUNICIPIO: {municipio} || CASOS: {casos}')

    quantidade_anomes_municipio_caso = df_casos[(df_casos["ANOMES"] == int(anomes)) & (df_casos["f_MUNICIPIO"] == municipio) ][casos].sum()
    quantidade_anomesAnterior_municipio_caso = df_casos[(df_casos["ANOMES"] == int(202206)) & (df_casos["f_MUNICIPIO"] == municipio) ][casos].sum()
    perc_anomesAtual_anomesAnterior = ( quantidade_anomes_municipio_caso / quantidade_anomesAnterior_municipio_caso ) * 100
    perc_anomesAtual_anomesAnterior = f'{str(round(perc_anomesAtual_anomesAnterior,1))}%' 

    #quantidade_ano_municipio_caso = df_casos[(df_casos["ANO"] == int(str(anomes)[0:4])) & (df_casos["f_MUNICIPIO"] == municipio) ][casos].sum()
    #percentual_anomes_municipio_caso = ( quantidade_anomes_municipio_caso / quantidade_ano_municipio_caso ) * 100
    #percentual_anomes_municipio_caso = f'{str(round(percentual_anomes_municipio_caso,1))}%' 

    return (quantidade_anomes_municipio_caso, perc_anomesAtual_anomesAnterior)

@app.callback(
        Output("graf_linhas", "figure"),
        Output("graf_barras", "figure1"),        
        [Input("casos-dropdown", "children"), Input("municipio-dropdown", "value"), Input("casos-dropdown", "value")]
            )

def plot_line_graph(plot_type, municipio, casos):
    
    df_casos_grafico = df_casos
    df_casos_grafico = df_casos_grafico.groupby(["ANO"])[str(casos)].sum().reset_index()

    fig2 = go.Figure(layout={"template":"plotly_dark"})
    bar_plots = ["AMEACA", "ESTUPRO"]   
   
    if plot_type in bar_plots:
        html.H1(children=f'VISÃO ANO | ????'),
        html.Div(children='''BASE DESTINADA AOS CASOS DE AMEACA'''),
        fig2.add_trace(go.Bar(x=df_casos_grafico["ANO"], y=df_casos_grafico[casos]))
    else:
        html.H1(children=f'VISÃO ANO | ????'),
        html.Div(children='''BASE DESTINADA AOS CASOS DE AMEACA'''),
        fig2.add_trace(go.Scatter(x=df_casos_grafico["ANO"], y=df_casos_grafico[casos]))
    
    fig2.update_layout(
        paper_bgcolor="#1C1C1C",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        #title_text = f'VISÃO ANO ACUMULADO | {casos.upper()}', # adicionando titulo ao gráfico
        #title_x = 0.5
        )
    return fig2

# Gráfico de barras agrupado para as regiões
@app.callback(Output('bar-grouped-regioes','figure'),
             [Input('regiao-picker','value')])

def update_bar_regioes(selected_regiao):
    # filtrando os dados para a região selecionada
    df_regiao = df[df['Regiao']== selected_regiao]

    fig4 = px.bar(df_regiao, # data frame com os dados
            x = 'Ano', # coluna para os dados do eixo x
            y = 'Total', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'UF', # setando a coluna que irá serparar as colunas dentro do grupo
            hover_name = 'UF', # coluna para setar o titulo do hover
            hover_data = {'UF': False}, # Removendo o Mes para que não fique repetido no título do hover e no conteúdo do hover
            )
    fig4.update_layout(xaxis = dict(linecolor='rgba(0,0,0,1)', # adicionando linha em y = 0
                                    tickmode = 'array', # alterando o modo dos ticks
                                    tickvals = df_regiao['Ano'], # setando o valor do tick de x
                                    ticktext = df_regiao['Ano']), # setando o valor do tick de x
                     yaxis = dict(title = 'Total de focos de queimadas por ano',  # alterando o titulo do eixo y
                                  linecolor='rgba(0,0,0,1)', # adicionando linha em x = 0
                                  tickformat=False), # removendo a formatação no eixo y
                                  title_text = 'Total de focos de queimadas identificados por ano para cada estado na região ' + selected_regiao, # adicionando titulo ao gráfico
                                  title_x = 0.5, # reposicionando o titulo para que ele fique ono centro do gráfico
                     )
    return fig4


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)





"""data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
)"""

"""fig4 = go.Figure(
    data=[go.Table(
    header=dict(values=list(df_casos.columns.tolist()),), # dados do cabeçalho
    cells=dict(values=[df_casos['ANOMES'],
                        df_casos['f_MUNICIPIO'], # dados do corpo da tabela
                        df_casos['REGIAO'],
                        df_casos['ESTUPRO'],
                        df_casos['AMEACA']],
              ))
])"""

"""fig4 = go.bar(df_total,
            x = 'Ano', # coluna para os dados do eixo x
            y = 'Total de focos de queimadas por ano', # coluna para os dados do eixo y
            hover_name = 'Regiao'
            )
fig4.update_layout(xaxis = dict(linecolor='rgba(0,0,0,1)', # adicionando linha em y = 0
                                tickmode = 'array', # alterando o modo dos ticks
                                tickvals = df_regiao['Ano'], # setando o valor do tick de x
                                ticktext = df_regiao['Ano']), # setando o valor do tick de x
                 yaxis = dict(linecolor='rgba(0,0,0,1)', # adicionando linha em x = 0
                              tickformat=False), # removendo a formatação no eixo y
                title_text = 'Total de focos de queimadas identificados na região ' + selected_regiao,  # adicionando titulo ao gráfico
                title_x = 0.5, # reposicionando o titulo para que ele fique ono centro do gráfico
                 )"""

############################################################################################
"""modelo
https://stackoverflow.com/questions/69331376/plotly-dash-layout-with-dbc-col-and-dbc-row
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

dbc.Row([
    dbc.Col([
        dbc.Row([content]),
        dbc.Row([content])
        ]),
    dbc.Col([
        dbc.Row([content]),
        dbc.Row([content])]),
    dbc.Col([content])
    ]),

dbc.Row([
    dbc.Col([content]),
    dbc.Col([content])
    ])"""
        
    


        #CARD 2
        #dbc.Row(
        #    [dbc.Card([dbc.CardBody([
        #    html.Span("Qtd [MÊS]", className="card-text"),
        #    html.H3(style={"color": "#adfc92"}, id="qtd-ocorrencias-text2"),
        #    html.Span("% [ANO]", className="card-text2"),
        #    html.H5(id="perc-todos-casos-text2"),
        #    ])]
        #        ,color="light"
        #        ,outline=True
        #        , style={"width": "auto",
        #                "margin-top": "-300px",
        #                "margin-left": "150px",
        #                "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
        #                "color": "#FFFFFF"})]),      