#import modules, libraries
import glob
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly

import pandas as pd
import numpy as np 

import re 
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from textblob import TextBlob, Word
#download two files from NLTK at the first time only
nltk.download('punkt')
nltk.download('stopwords')

def get_tokens(content):
    """Splits given text into sentences, removes symbols and delimiters, converts char to lowercase, tokenize cleaned text.

    Parameters:
    Content(str): text to perform above

    Returns: list of tokens from content text
    """
    sentences = TextBlob(content).sentences
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
    tokenize_word = word_tokenize(content)
    return tokenize_word

def remove_stopwords(tokens):
    """Removes nltk stopwords and custom stopwords from tokenized words in content text. 

    Parameters:
    tokens (list): list of tokens to perform above

    Returns: list of tokens without stopwords 
    """
    stop_words = stopwords.words('english')
    f = open('stopwordlist.txt', encoding='utf-8')
    stop_words2 = f.read()
    f.close()
    stop_words2=(re.sub("\s+", " ", stop_words2)).split()

    for w in stop_words2:
        if w not in stop_words:
            stop_words.append(w)
    stop_words = set(stop_words)

    filtered_sent=[w for w in tokens if w not in stop_words]
    return filtered_sent
def freq_distribution(clean_tokens):
    """Gets frequency distribution of tokens without stopwords. Turns 25 most frequent words into pandas dataframe.

    Parameters:
    tokens (list): list of tokens to perform above

    Returns: pandas dataframe of 25 most frequent words 
    """    
    freq_dist = FreqDist(clean_tokens)
    fd = pd.DataFrame(freq_dist.most_common(25), columns = ['Word', 'Frequency'])
    return fd 

def sent_polarity(content):
    """Returns list of first 100 sentences and their sentiment's polarity

    Parameters:
    content(str): text to perform above

    Returns: list of 100 first sentences with sentiment's polarity 
    """
    sentences = TextBlob(content).sentences
    polar=[]
    sent_len=[]
    i=0
    for sent in sentences:
        sent_len.append(len(sentences[i].words))
        if sentences[i].sentiment[0] > 0:
            polar.append('pos')
        elif sentences[i].sentiment[0] < 0:
            polar.append('neg')
        else:
            polar.append('neu')
        i=i+1

    sent_polar=list(zip(sent_len, polar))[:100]
    return sent_polar
def get_labels(dataframe):
    """Converts sentences' length and polarity into arrays [10,10] and gets labels for plotting

    Parameters:
    dataframe(df): pandas dataframe to perform above

    Returns: [10,10] arrays of length, polarity labels for plotting
    """
    sent_len = np.asarray(dataframe['length']).reshape(10,10)

    polar = np.asarray(dataframe['polarity']).reshape(10,10)

    labels = np.asarray(['{0}\n {1}'.format(leng, polar) for leng, polar in zip(sent_len.flatten(), polar.flatten())]).reshape(10,10)
    return labels
#Get data for sentiment polarity scatterplot, each year
df = [pd.read_csv(f) for f in glob.glob('jake scrape/jake final/*.csv')]

#Get data for words frequency distribution plot
df1 = [pd.read_csv(f) for f in glob.glob('jake scrape/*.csv')]

#Plot sentiment polarity in all years, subplots
years=['2009','2010','2011','2012','2013','2014','2015','2016']

row=1
col=1
fig3 = make_subplots(rows=2, cols=4, shared_yaxes=True)
#range for all files (all blogging years, one file per year)
for i in range(0,8,1):
    
    if col == 5:
        row = 2
        col = 1
        
    fig3.add_trace(go.Scatter(x=df[i].date, y=df[i].sentiment, name=years[i], mode='lines'),
              row=row, col=col)
    
    col = col+1

fig3.update_layout(height=700, width=700,
                  title_text='<b>sentiment in jackbones.com in all years of blog activity</b>', plot_bgcolor='blanchedalmond')
fig3.update_yaxes(autorange="reversed")
fig3.update_xaxes(tickangle=30, tickfont=dict(size=12)) 

#Plot sentiment polarity in all years, one plot
df2 = pd.concat(df, ignore_index=True)

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=df2.date, y=df2.sentiment,
                    mode='lines', line = dict(color = 'limegreen'),
                    
                        ))
fig4.update_yaxes(autorange="reversed")
fig4.update_layout(title_text='<b>jackbones.com sentiment in all years of blog activity</b>', plot_bgcolor='blanchedalmond', height=600, margin=go.layout.Margin(
                    l=50,
                    r=50,
                    b=100,
                    t=150,
                    pad=4))

#Initialize Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Year in numbers at jackes-bones.com'

app.layout = html.Div(children=[
    html.H2('Year in numbers at jakes-bones.com', style={
        'textAlign': 'center'
    }),
    html.H4('Data visualization for blogging tendencies', style={
        'textAlign': 'center'
    }),
    html.Div(
        className='row',
        children=[ 
            dcc.Markdown("__Author's Words__: This is a University project which allows you to visualize content of chosen blogs scrapped from web. If you like it, star ⭐️ this project on [GitHub](https://github.com/Malwoiniak/thematic-analysis-helper)!✨"),
        ],style={'width': '35%', 'marginLeft': 70,}
    ),
    html.Br(),

    html.Div(
        className='row',
        children=[
        html.P('Choose the year:'),
#add dropdown option from dcc components
    dcc.Dropdown(
    id='Years',
    options=[
        {'label': '2009', 'value': '2009'},
        {'label': '2010', 'value': '2010'},
        {'label': '2011', 'value': '2011'},
        {'label': '2012', 'value': '2012'},
        {'label': '2013', 'value': '2013'},
        {'label': '2014', 'value': '2014'},
        {'label': '2015', 'value': '2015'},
        {'label': '2016', 'value': '2016'},
    ],
    value='2009'
)
          
        ], style={'marginRight': 70,'marginLeft': 70,}
        ),
    html.Br(),

    html.Div([
        html.Div([
            dcc.Graph(
        id='scatter-polar')
        ], className='six columns'),

        html.Div([
            dcc.Graph(
        id='freq-dist')

        ], className='six columns')


    ], className='row'),


    html.Div([
        html.Div([
            dcc.Graph(
        id='wordcloud'
        )], className='six columns'),

        html.Div([
            dcc.Graph(
        id='heatmap'
        )], className='six columns')


    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(
        id='senti-all-loop',
        figure=fig3
        )], className='six columns'),

        html.Div([
            dcc.Graph(
        id='senti-in-one',
        figure=fig4
        )], className='six columns')


    ], className='row')

])
#Append stylesheet to enable className='six columns', className='row'
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
#Create callbacks for dropdown menu
@app.callback(
    dash.dependencies.Output('scatter-polar', 'figure'),
    [(dash.dependencies.Input('Years', 'value'))]
    )
#Callback function for updating graph 
def update_graph(year):
    if '2009' in year:
        i = 0
    elif '2010' in year:
        i = 1  
    elif '2011' in year:
        i = 2
    elif '2012' in year:
        i = 3
    elif '2013' in year:
        i = 4
    elif '2014' in year:
        i = 5
    elif '2015' in year:
        i = 6
    else:
        i = 7
    #Get scatterplot of sentiment's polarity per blog post of each year
    fig0 = px.scatter(df[i], 
        x=df[i].headline, 
        y=df[i].polarity, 
        color=df[i].polarity, 
        color_continuous_scale=px.colors.diverging.Portland[::-1], 
        size=abs(df[i].polarity), 
        size_max=40, 
        opacity=0.85, 
        range_color=[-1,1],  
        labels={'polarity':'Post\'s polarity', 'headline':'Post\'s title'}, 
        title='<b>jackes-bones.com: posts in {0}</b>'.format(year))

    fig0.update_traces(dict(marker_line_width=2,marker_line_color='darkslategray'),
    hovertemplate=
    'post\'s title:<b>%{x}</b>'+
    '<br>date:<b>%{text|%Y-%m-%d}</b><br>'
    'polarity:<b>%{y}</b>',
    text = df[i].date,
    )
    fig0.update_xaxes(showticklabels=False)

    fig0.update_layout(plot_bgcolor='blanchedalmond', width=850)
    figure=fig0
    return figure


@app.callback(
    dash.dependencies.Output('freq-dist', 'figure'),
    [(dash.dependencies.Input('Years', 'value'))]
    )
def update_graph(year):
    if '2009' in year:
        i = 0
    elif '2010' in year:
        i = 1  
    elif '2011' in year:
        i = 2
    elif '2012' in year:
        i = 3
    elif '2013' in year:
        i = 4
    elif '2014' in year:
        i = 5
    elif '2015' in year:
        i = 6
    else:
        i = 7
    #Get data for most frequent bar chart: merged content of all blog texts
    content = ' '.join(df1[i]['summary'])
    #Get frequency distribution of tokens without stopwords 
    fd = freq_distribution(remove_stopwords(get_tokens(content)))
    #Plot frequency distribution of 25 most frequent words
    fig = px.bar(fd, x="Word", y="Frequency")
    fig.update_traces(marker_color=' lawngreen',          
    marker_line_color='mediumvioletred',                    
    marker_line_width=1.5, opacity=0.8)
    fig.update_xaxes(tickangle=30) 
    fig.update_layout(title_text='<b>25 most frequent words in {0}</b>'.format(year), plot_bgcolor='blanchedalmond')

    figure=fig
    return figure

@app.callback(
    dash.dependencies.Output('wordcloud', 'figure'),
    [(dash.dependencies.Input('Years', 'value'))]
    )
def update_graph(year):
    if '2009' in year:
        i = 0
    elif '2010' in year:
        i = 1  
    elif '2011' in year:
        i = 2
    elif '2012' in year:
        i = 3
    elif '2013' in year:
        i = 4
    elif '2014' in year:
        i = 5
    elif '2015' in year:
        i = 6
    else:
        i = 7
    #Get all blog texts joined as data
    content = ' '.join(df1[i]['summary'])   
    fd = freq_distribution(remove_stopwords(get_tokens(content)))
    #words in wordcloud
    words = fd.Word
    #randomly assign plotly default colour to word
    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(25)]
    #font size will depend on word frequency (weight)
    weights = fd.Frequency
    #xaxis with length range 0 to 25 (number of words plotted) to minimalize the problem of words overlap
    length = fd.shape[0]
    #normalize font size to differences in data freqencies/size of words
    lower, upper = 30, 65
    weights1 = [((x - min(weights))/ (max(weights) - min(weights))) * (upper-lower) + lower for x in weights]
    #Get wordcloud
    data = go.Scatter(x=list(range(length)),
                        y=random.choices(range(length),k=length),#unique and random values of yaxis to reduce overlapping issue
                        mode='text',
                        text=words,
                        marker={'opacity':0.3},
                        textfont={'size':weights1,
                        'color':colors},
                        hovertext=['{0}<br><b>frequency:</b>{1}</br>'.format(w, f) for w, f in zip(words, weights)],
                        hoverinfo='text'
                        )
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},

                        }, title_text='<b>25 most frequent words in {0}</b>'.format(year), plot_bgcolor='blanchedalmond', 
                        margin=go.layout.Margin(
                        l=50,
                        r=50,
                        b=100,
                        t=150,
                        pad=4), height=500)
    fig1 = go.Figure(data=[data], layout=layout)

    figure=fig1
    return figure

@app.callback(
    dash.dependencies.Output('heatmap', 'figure'),
    [(dash.dependencies.Input('Years', 'value'))]
    )
def update_graph(year):
    if '2009' in year:
        i = 0
    elif '2010' in year:
        i = 1  
    elif '2011' in year:
        i = 2
    elif '2012' in year:
        i = 3
    elif '2013' in year:
        i = 4
    elif '2014' in year:
        i = 5
    elif '2015' in year:
        i = 6
    else:
        i = 7

    content = ' '.join(df1[i]['summary'])
    #Get list of 100 first sentences and their sentiment's polarity from content (all blog text joined together)
    sent_polar = sent_polarity(content)
    #Create dataframe of sentences and their polarity
    sp = pd.DataFrame(sent_polar, 
                   columns =['length', 'polarity'])
    #Get labels for heatmap annotations
    labels = get_labels(sp)
    #Get results (sentences' length) as [10,10] array 
    results = np.asarray(sp.length).reshape(10,10)
    #Create heatmap
    fig2 = ff.create_annotated_heatmap(results, annotation_text=labels, text=labels, hoverinfo='text', showscale=True)
    fig2.update_layout(
                   title_text='<b>Length and polarity of first 100 sentences in {0}</b>'.format(year), height=600)
    figure=fig2
    return figure


if __name__ == '__main__':
    app.run_server(debug=True
        )
