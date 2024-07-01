# -*- coding: utf-8 -*-
"""youtube-comments-analysis-updated.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CnWCpJzvEZznYnTaCcHWcE8Q714EthSj

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: ;
           font-size:200%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:black;">Ken Jee's YouTube Data Analysis
    
</h2>
</div>
    
</center>


![image](https://duet-cdn.vox-cdn.com/thumbor/0x0:1680x1050/1440x960/filters:focal(840x525:841x526):no_upscale():format(webp)/cdn0.vox-cdn.com/uploads/chorus_asset/file/9130449/YTLogo_old_new_animation.gif)

## **Table of Contents**

1. [Overview and Problem Statement](#Section1)<br>
2. [Reading the Data](#Section2)<br>
3. [Exploratory Data Analysis](#Section3)<br>
4. [Sentiment Analysis](#Section4)<br>
9. [Summary](#Section5)<br>

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Overview and Problem Statement
    
</h2>
</div>
    
</center>


This dataset provides a comprehensive analysis of **Ken Jee's YouTube Channel** with data spanning from Nov 2017 to Jan 2022. The four files in the repository contain valuable insights for addressing several key questions:

1) **Themes of Comment Data**: The dataset allows us to explore the prevalent themes and topics discussed in the comments section of Ken's videos.

2) **Video Titles and Thumbnails Analysis**: By examining the data, we can determine the types of video titles and thumbnails that have been most effective in driving traffic to his channel.

3) **Understanding the Core Audience**: We can identify Ken's core audience and gain insights into their interests and preferences based on their viewing patterns and engagement.

4) **Videos Leading to Growth**: The dataset enables us to discover which types of videos have contributed the most to the growth and success of Ken's channel.

5) **Engaging Content Identification**: Through analysis, we can uncover the type of content that garners the highest levels of engagement and captures viewers' attention for longer durations.

The data encompasses aggregated metrics, including country-specific and subscriber status dimensions, as well as daily performance data for each video. It has been meticulously gathered by Ken himself via the YouTube API and analytics, with a focus on ensuring audience privacy through anonymization.

Let's proceed with this comprehensive dataset to gain valuable insights into the various aspects of Ken Jee's YouTube Channel!
"""

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from wordcloud import WordCloud
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import matplotlib.pyplot as plt
# %matplotlib inline
plt.rcParams['font.size'] = 14
plt.rcParams['figure.figsize'] = (22, 5)
plt.rcParams['figure.dpi'] = 100

"""Now that we have imported all the required libraries and the classes, we start reading the Data with the help of pandas and taking a look at the data.

<a id = Section2></a>

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Reading the Data
    
</h2>
</div>
    
</center>
"""

Aggregated_df = pd.read_csv("/content/Aggregated_Metrics_By_Video.csv")
Country_df = pd.read_csv(r"/content/Aggregated_Metrics_By_Country_And_Subscriber_Status.csv")
Video_df = pd.read_csv(r"/content/Video_Performance_Over_Time.csv")
Comments_df = pd.read_csv(r"/content/All_Comments_Final.csv")

Aggregated_df.head()

Country_df.head()

Video_df.head()

Comments_df.head()

"""<a id = Section3></a>

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Exploratory Data Analysis
    
</h2>
</div>
    
</center>

EDA, which stands for **Exploratory Data Analysis**, is a critical initial step in the data analysis process. It involves visually and statistically exploring the data to gain insights, identify patterns, detect anomalies, and better understand the structure and characteristics of the dataset. EDA helps data analysts and scientists to become familiar with the data, validate assumptions, and guide the selection of appropriate data preprocessing and modeling techniques.

Key components and techniques used in Exploratory Data Analysis include:

1. **Data Cleaning**: This step involves identifying and handling missing values, duplicates, and outliers that can affect the quality of the analysis. Cleaning the data ensures that subsequent analyses are based on accurate and reliable information.

2. **Descriptive Statistics**: Descriptive statistics provide summary information about the dataset, including measures of central tendency (e.g., mean, median, mode), dispersion (e.g., range, standard deviation), and distribution of the data.

3. **Data Visualization**: Visualizing the data using various plots and charts helps in gaining an intuitive understanding of the data's distribution and patterns. Common visualizations include:

   - Histograms: For displaying the frequency distribution of continuous data.
   - Box Plots: To identify outliers and visualize the spread of the data.
   - Scatter Plots: For examining relationships between two continuous variables.
   - Bar Charts: For categorical data visualization.
   - Heatmaps: To visualize the correlation between variables.
   - Pair Plots: To visualize pairwise relationships in multi-dimensional datasets.

4. **Correlation Analysis**: EDA often includes calculating and visualizing correlations between variables to understand the strength and direction of their relationships. Correlation matrices and heatmaps are commonly used for this purpose.

5. **Distribution Analysis**: Understanding the distribution of data is crucial. EDA helps to identify if the data follows a normal distribution or if it has skewed or bimodal distributions, which can impact the choice of appropriate statistical tests and models.

6. **Feature Engineering**: Exploratory Data Analysis can inspire feature engineering ideas by revealing important interactions or transformations that might enhance the predictive power of machine learning models.

7. **Data Transformation**: EDA may also indicate the need for data transformations such as normalization, scaling, or log transformations to improve model performance.

8. **Hypothesis Generation**: During EDA, analysts might generate hypotheses about relationships or trends in the data. These hypotheses can be further tested and validated in subsequent steps of the analysis.

EDA is NOT a one-time process but an iterative one. As analysts explore the data and make discoveries, they may go back to data cleaning, apply new visualizations, or conduct deeper analyses based on their findings. EDA helps set the stage for more sophisticated modeling, and it is a crucial step in understanding the data's structure and uncovering insights that can inform decision-making and guide further analysis.
"""

Aggregated_df.describe()

print('Net Subscribers Gained -', Aggregated_df['Sub­scribers gained'].loc[0]-Aggregated_df['Sub­scribers lost'].loc[0])

Video_df.describe()

Country_df.describe()

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: lightgray;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:black;">Analysis
    
</h3>
</div>
    
</center>

1. Over the past six years, Ken has published a total of 223 videos, amassing an impressive 39640 shares, 225,021 likes, and gaining 183,451 new subscribers.
2. On average, Ken receives 126 comments on each of his videos, reflecting active engagement from his viewers.
3. Across his 223 video uploads, the average watch time amounts to 2835 hours, indicative of the captivating content Ken consistently delivers to his audience.
"""

Subscribed_df = Country_df.copy().sort_values(by='Views',ascending= False)
plt.title("Subscribed Or Not")
sns.countplot(x= Subscribed_df['Is Subscribed'])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()

True_df = Country_df[Country_df['Is Subscribed'].eq(True)].sort_values(by='Views',ascending= False)
False_df = Country_df[Country_df['Is Subscribed'].eq(False)].sort_values(by='Views',ascending= False)
True_df['Video Title'].head(10).unique().tolist()

"""

<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> Above are the videos that are most watched by people who have subsribed to the channel.

</div>
  </center>"""

Subscribed_Watchtime = True_df.groupby('Country Code').sum().sort_values(by='Views',ascending= False).head(3).reset_index()
sns.barplot(x=Subscribed_Watchtime['Country Code'], y= Subscribed_Watchtime['Average Watch Time'])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.title("Watch Time from top 3 countries (Subscribed)")
plt.axhline(Subscribed_Watchtime['Average Watch Time'].mean(), linestyle='--', lw=2, zorder=1, color='black')
plt.annotate(f'Average Watch Time', (0.7, Subscribed_Watchtime['Average Watch Time'].mean()+1500), fontsize=15, color='blue')

plt.xlabel('Country Code')
plt.show()

"""<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> People who have subscribed to the channel are from US and Great Britain and contribute to the highest Average Watch Time.

</div>
  </center>
"""

unsubscribed_Watchtime = False_df.groupby('Country Code').sum().sort_values(by='Views',ascending= False).head(3).reset_index()
sns.barplot(data=unsubscribed_Watchtime, x=unsubscribed_Watchtime['Country Code'],
            y= unsubscribed_Watchtime['Average Watch Time'])

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.axhline(unsubscribed_Watchtime['Average Watch Time'].mean(), linestyle='--', lw=2, zorder=1, color='black')
plt.annotate(f'Average Watch Time', (0.7, unsubscribed_Watchtime['Average Watch Time'].mean()+1500), fontsize=15, color='blue')

plt.title("Watch Time from top 3 countries (unsubscribed)")
plt.xlabel('Country Code')
plt.show()

"""<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> The most amount of watchtime from the unsubscribed viewers come from Britain then US and then India.

</div>
  </center>
"""

False_df['Video Title'].head(12).unique().tolist()

"""<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> Above is the list of videos being watched the most by the unsubscribed viewers.


</div>
  </center>

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Q. Who is Ken's core audience and what are they interested in?
    
</h2>
</div>
    
</center>
"""

#Top 10 countries where the audience is from
ViewsbyCountry = Country_df[['Country Code', 'Views']].copy().sort_values(by='Views',ascending= False)
ViewsbyCountry.groupby('Country Code').sum().sort_values(by='Views',ascending= False).head(5)

"""


<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> People from US, India and Great Britain watch the videos the most.


</div>
  </center>"""

df = Country_df[['Video Title', 'Views', 'Average Watch Time', 'Country Code']].copy().sort_values(by='Views',ascending= False)
US_df = df[df['Country Code']=='US']
IN_df = df[df['Country Code']=='IN']
GB_df = df[df['Country Code']=='GB']
audience = pd.concat([US_df, IN_df, GB_df], axis=0, sort=False).sort_values(by='Views',ascending= False)

sns.barplot(x=audience['Country Code'] , y= audience['Views'])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.axhline(audience['Views'].mean(), linestyle='--', lw=2, zorder=1, color='red')
plt.annotate(f'Average View Count', (1.8, audience['Views'].mean()+200), fontsize=15, color='blue')

plt.title("Views count from top 3 countries")
plt.xlabel('Views')
plt.show()

audience.groupby('Video Title').sum().sort_values(by='Views',ascending= False).head(5).index.tolist()

"""



<center>
<div class="alert alert-block alert-info">
<b>INTERPRETATION: </b> The people from US, India and Great Britain watch these top 5 videos the most



</div>
  </center>

- 'How I Would Learn Data Science (If I Had to Start Over)',
- 'The Best Free Data Science Courses Nobody is Talking About',
- '3 Proven Data Science Projects for Beginners (Kaggle)',
- 'Beginner Kaggle Data Science Project Walk-Through (Titanic)',
- 'Data Science Certificate vs Bootcamp vs Masters Degree']"""

sns.histplot(data=audience, x=audience['Average Watch Time'], hue='Country Code', kde=True, alpha=0.2)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.axvline(audience['Average Watch Time'].mean(), linestyle='--', lw=2, zorder=1, color='blue')
plt.annotate(f' Mean Average Watch Time', (210, 60), fontsize=18,color='blue')
plt.title('Average Watch Time distribution in top 3 countries')
plt.show()

Video_df.drop_duplicates('Video Title')['Views'].plot(kind='kde', color='lightgray')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.axvline(Video_df['Views'].mean(), linestyle='--', lw=2, zorder=0, color='red')
plt.annotate(f' Average Views', (Video_df['Views'].mean()+20, 0.007),color='red')
plt.title('Views Distribution on Unique Videos')
plt.xlim(left = -400)
plt.show()

ax= sns.kdeplot(data=Video_df, x=Video_df['Video Length'], color='lightgray', alpha=0.2)
ax.lines[0].set_color('red')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.axvline(Video_df['Video Length'].mean(), linestyle='--', lw=2, zorder=1, color='blue')
plt.annotate(f' Average Video Length', (900, 0.0012),color='blue')
plt.title('Video Length Distribution')
plt.show()

corr = Video_df[['Video Length', 'Views', 'Video Likes Added', 'Video Dislikes Added', 'Video Likes Removed',
        'User Subscriptions Added','User Subscriptions Removed', 'Average View Percentage','Average Watch Time']].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(25,20))
cmap = sns.diverging_palette(220, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, annot=True,square=True, linewidths=.5, cbar_kws={'shrink': .5})
plt.show()

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Q: What type of content are people engaging with the most or watching the longest?
    
</h2>
</div>
    
</center>
"""

#Top 5 videos that have garnered the most views
Views_df = Video_df[['Video Title','External Video ID', 'Views']].copy().sort_values(by='Views',ascending= False)
Views_df.drop_duplicates('Video Title',inplace=True)
Views_df['Video Title'].head(10).values.tolist()

"""

<center>
<div class="alert alert-block alert-info">
 From the results, evidently people are keen to know about



</div>
  </center>


- Data Science Roadmap
- Projects
- Roles in Datascience"""

Video_df.groupby('Video Title').sum().sort_values(by='Average Watch Time',ascending= False).head(5).index.tolist()

"""<center>
<div class="alert alert-block alert-info">
Top 5 videos that have been watched the longest are:-




</div>
  </center>

- 'Uber Driver to Machine Learning Engineer in 9 Months! (@Daniel Bourke) - KNN EP. 05',
- 'Data Science Project from Scratch - Part 4 (Exploratory Data Analysis)',
- 'Data Science Fundamentals: Data Manipulation in Python (Pandas)',
- 'Data Science Project from Scratch - Part 3 (Data Cleaning)',
- 'Advice from a Data Analytics CEO (@How to Get an Analytics Job) - KNN EP. 17'

<center>
<div style="color:;
           displaya:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Q. What are the themes of the comment data?
    
</h2>
</div>
    
</center>

In this section we will be doing Sentiment analysis of the comments and most commented video too.
<a id = Section4></a>

<center>
<div style="color:;
           displaya:fill;
           border-radius:5px;
           background-color: lightgray;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:black;">Sentiment analysis
    
</h2>
</div>
    
</center>


**Sentiment analysis**, also known as opinion mining, is a natural language processing (NLP) task that involves determining the sentiment or emotion expressed in a piece of text. The main goal of sentiment analysis is to understand whether the expressed opinion is positive, negative, neutral, or sometimes more granular emotions like happy, sad, angry, etc. This has numerous applications in various fields, such as market research, social media monitoring, customer feedback analysis, and more.

*Traditional sentiment analysis* approaches often relied on hand-crafted features and machine learning algorithms like Support Vector Machines (SVM), Naive Bayes, or logistic regression. These models required domain-specific feature engineering and lacked the ability to capture complex language patterns effectively.
"""

print('Comments on videos - ', format(len(Comments_df['Comments'])))
print('Unique Videos - ', format(Comments_df['VidId'].nunique()))
print('Comments per Video -', format(int(len(Comments_df['Comments'])/Comments_df['VidId'].nunique())))

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"([-?.!,/\"])", '', text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,']", "", text)
    text = re.sub(r"[ ]+", " ", text)
    text = re.sub('\n\n','', text)
    text = text.rstrip().strip()
    return text

clean_text(Comments_df['Comments'][0])

clean_comments = []
for i in range(len(Comments_df['Comments'])):
    try:
        clean_comments.append(clean_text(Comments_df['Comments'][i]))
    except:
        clean_comments.append('None')
    if i % 1000==0:
        print(f'{i} iteration(s) completed')
Comments_df['Clean Comments'] = clean_comments

"""- **Polarity** is a float value within the range **[-1.0 to 1.0]**.
  
  - Here, **0** indicates **neutral**,
  
  - **+1** indicates a **very positive** sentiment, and
  
  - **-1** represents a **very negative** sentiment.

"""

polarity = []
for i in Comments_df['Clean Comments']:
    blob = TextBlob(i)
    polarity.append(round(blob.sentiment.polarity,3))
Comments_df['polarity'] = polarity
print('Polarity Column added to the dataframe')

Comments_df.head()

print('Reviews with Positive Sentiment based on Polarity :', len(Comments_df[Comments_df['polarity'] > 0]))
print('Reviews with Negative Sentiment based on Polarity :', len(Comments_df[Comments_df['polarity'] < 0]))
print('Reviews with Neutral Sentiment based on Polarity :', len(Comments_df[Comments_df['polarity'] == 0]))

# prompt: make a pie chart

import matplotlib.pyplot as plt

# Define data
labels = ['Positive', 'Negative', 'Neutral']
sizes = [len(Comments_df[Comments_df['polarity'] > 0]), len(Comments_df[Comments_df['polarity'] < 0]), len(Comments_df[Comments_df['polarity'] == 0])]
colors = ['green', 'red', 'grey']

# Create pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Sentiment Analysis of Comments')
plt.show()

sentiment = []
for i in range(len(Comments_df['polarity'])):
    if Comments_df['polarity'][i] > 0:
        sentiment.append('Positive')
    elif Comments_df['polarity'][i] < 0:
        sentiment.append('Negative')
    else:
        sentiment.append('Neutral')
Comments_df['sentiment'] = sentiment
print('Sentiment column has been added to the dataframe.')

Comments_df.head()

# Plotting the Count and Proportional Distribution of reviews based on sentiment as per polarity
plt.subplot(1, 2, 1)

# Plotting the count of reviews for each sentiment
sns.countplot(Comments_df['sentiment'],  )
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Sentiments based on Polarity', fontsize=18)

plt.subplot(1, 2, 2)
# Plotting the proportional distribution of sentiments
plt.pie(x=[len(Comments_df[Comments_df['polarity'] < 0]), len(Comments_df[Comments_df['polarity'] == 0]),
           len(Comments_df[Comments_df['polarity'] > 0])],
        labels=['Negative', 'Neutral', 'Positive'], autopct='%1.1f%%', pctdistance=0.5,
        textprops={'fontsize':14, 'color':'white'})
plt.title('Proportional Distribution of Sentiments')
plt.legend()
plt.show()

#Making a new dataframe for further use
df=Comments_df[['VidId','polarity','sentiment' ]].copy()

"""<a id = Section4.1></a>

<center>
<div style="color:;
           displaya:fill;
           border-radius:5px;
           background-color: lightblue;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:black;">Sentiment analysis Using BERT
    
</h3>
</div>

BERT (*Bidirectional Encoder Representations from Transformers*) is a deep learning model introduced by Google in 2018, which significantly advanced the field of NLP. Unlike traditional models that process text in a sequential manner, BERT utilizes a transformer-based architecture, enabling it to capture the context of words bidirectionally (both left and right) in a sentence.

Here's a brief overview of BERT's architecture and its key components:

1. **Transformer Encoder**: The transformer architecture relies on self-attention mechanisms, allowing it to weigh the importance of different words in the context of the whole sentence. This attention mechanism is used to generate contextualized word embeddings for each word in the sentence.

2. **Pre-training**: BERT is pre-trained on a large corpus of text using a masked language model objective. During pre-training, some words in the input are randomly masked, and the model is trained to predict the masked words based on the surrounding context. This process helps BERT learn rich contextual representations of words.

3. **Fine-tuning**: After pre-training, BERT is fine-tuned on specific downstream tasks like sentiment analysis. During fine-tuning, the model's weights are adjusted to adapt it to the target task.

Now, let's discuss how BERT makes sentiment analysis more effective and easier:

1. **Contextual Word Representations**: BERT's bidirectional nature enables it to understand the context in which a word appears in a sentence. This contextual understanding allows BERT to capture nuances in sentiment, such as sarcasm or negation, which were challenging for traditional methods to handle.

2. **Transfer Learning**: BERT is pre-trained on a large amount of general text data. This pre-training captures a wide range of language patterns and features, making it highly effective for a wide array of NLP tasks, including sentiment analysis. Fine-tuning on task-specific data further refines the model's performance.

3. **No Need for Hand-Crafted Features**: BERT does not require extensive hand-crafted feature engineering. It automatically learns and represents features from the data during pre-training and fine-tuning.

4. **State-of-the-art Performance**: BERT has achieved state-of-the-art performance on various NLP benchmarks, including sentiment analysis tasks, surpassing the performance of many traditional models.

So, BERT's bidirectional contextual word representations and transfer learning capabilities have revolutionized the field of sentiment analysis. By capturing the rich context and semantics of language, BERT offers superior performance and simplifies the process of sentiment analysis, making it a breeze compared to traditional approaches.
"""

#Downloading the model and the tokenizer
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tokens = tokenizer.encode(Comments_df['Comments'][0], return_tensors='pt')
result = model(tokens)
print(f'The sentiment of the first comment is {int(torch.argmax(result.logits))+1}')

def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits))+1

for i in range(0,10):
    score = sentiment_score(Comments_df['Comments'][i])
    comment = Comments_df['Comments'][i]
    print(f'Comment : {comment[0:100]}, Score : {score}.')
    print('\n')

# prompt: make a pir chart

import matplotlib.pyplot as plt

# Create data
labels = ["Category 1", "Category 2", "Category 3", "Category 4"]
sizes = [30, 25, 20, 25]

# Create a pie chart
plt.pie(sizes, labels=labels, autopct="%1.1f%%")

# Add title
plt.title("Pie Chart of Categories")

# Show the pie chart
plt.show()

"""We can see how easy it is to get the sentiment analysis with the BERT model. This allows us to spend more time on analysis rather than figuring out how to build the pipeline here. I have not ran the algo on the whole comments because of the limited computational power here on Kaggle

<center>
<div style="color:;
           displaya:fill;
           border-radius:5px;
           background-color: lightgray;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:black;">Top Vids (with highest positive polarity)
    
</h3>
</div>
    
</center>
"""

df.sort_values(by='polarity',ascending= False).head(5)

"""<center>
<div style="color:;
           displaya:fill;
           border-radius:5px;
           background-color: lightgray;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:black;">Bottom Vids (with highest negative polarity)
    
</h3>
</div>
    
</center>
"""

df.sort_values(by='polarity',ascending= False).tail(5)

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:white;">Words Used In Positive Comments
    
</h3>
</div>
    
</center>

We will be using something known as Word Cloud to visualize the words.

What is Word Cloud you ask? Well, A **word cloud** is a visual representation of text data where the most frequently occurring words in a given piece of text are displayed in a graphical form. In a word cloud, the size of each word is proportional to its frequency in the text. The more frequently a word appears in the text, the larger and bolder it appears in the word cloud.

Word clouds are often used to **provide a quick and intuitive overview** of the most important or commonly used words in a document, a collection of documents, or any other textual data source. They are particularly useful for identifying key themes, topics, or sentiments present in the text.

Creating a word cloud typically involves the following steps:

1. **Text Processing**: The text data is preprocessed to remove common stop words (e.g., "the," "is," "and," etc.) and other irrelevant or noisy words. The remaining words are then used to build the word cloud.

2. **Word Frequency Count**: The frequency of each word is calculated to determine how often it appears in the text.

3. **Word Cloud Visualization**: The words and their respective frequencies are represented graphically in the form of a word cloud. The more frequent a word, the larger and more prominent it appears in the cloud.

Word clouds are often used for various purposes, such as:

- Visualizing the content of a document or an article.
- Understanding the most common topics discussed in customer reviews, feedback, or social media comments.
- Analyzing responses in surveys to identify prevalent keywords or themes.
- Gaining insights into the vocabulary used in a specific domain or text corpus.
- Creating visually appealing artwork or illustrations based on text data.

Word clouds are easy to interpret and provide a quick overview of the most relevant information in a visually engaging manner. However, it's important to note that word clouds have limitations, particularly when dealing with large volumes of text. They may not capture the full context of the text or convey more intricate relationships between words. In some cases, more advanced text analysis techniques, such as topic modeling or sentiment analysis, may be required for deeper insights into the textual data.
"""

wordcloud = WordCloud(width=2500, height=2000, max_words=50,
                      background_color='White').generate(str(Comments_df[(Comments_df['polarity'] > 0)].sample(1000,
                     random_state=0)['Clean Comments']))

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# prompt: plot a pie chart for above code

import matplotlib.pyplot as plt
# Create a dictionary to store the word counts
word_counts = {}

# Loop through the comments and count the words
for comment in Comments_df[(Comments_df['polarity'] > 0)].sample(1000, random_state=0)['Clean Comments']:
  for word in comment.split():
    if word not in word_counts:
      word_counts[word] = 0
    word_counts[word] += 1

# Create a list of tuples sorted by word count
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Extract the top 10 words and their counts
top_words = sorted_words[:10]

# Create a list of labels and values for the pie chart
labels, values = zip(*top_words)

# Create the pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title('Top 10 Words Used in Positive Comments')
plt.show()

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 10px;
              color:white;">Words Used in Negative Comments
    
</h3>
</div>
    
</center>
"""

wordcloud = WordCloud(width=2500, height=2000, max_words=50,
                      background_color='White').generate(str(Comments_df[(Comments_df['polarity'] < 0)].sample(100,
                     random_state=0)['Clean Comments']))

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# prompt: make a pie chart for above code

import matplotlib.pyplot as plt
# Create a dictionary to store the word counts
word_counts = {}

# Loop through the comments and count the words
for comment in Comments_df[(Comments_df['polarity'] < 0)].sample(100, random_state=0)['Clean Comments']:
  for word in comment.split():
    if word not in word_counts:
      word_counts[word] = 0
    word_counts[word] += 1

# Create a list of tuples sorted by word count
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Extract the top 10 words and their counts
top_words = sorted_words[:10]

# Create a list of labels and values for the pie chart
labels, values = zip(*top_words)

# Create the pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title('Top 10 Words Used in Negative Comments')
plt.show()

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumpurple;
           font-size:110%;
           letter-spacing:0.5px">

<h3 style="padding: 5px;
              color:white;">Most Commented Video
    
</h3>
</div>
    
</center>
"""

topcommentsdf = pd.pivot_table(Comments_df, index = 'VidId', values = 'Comment_ID', aggfunc = 'count')
topcommentsdf = topcommentsdf.sort_values('Comment_ID', ascending = False)
New_df = topcommentsdf.merge(Aggregated_df,left_on='VidId', right_on='Video' )
New_df.groupby('Video title').sum().sort_values(by='Comment_ID',ascending= False).reset_index().head(5)

# prompt: make a bar chart for above code

import matplotlib.pyplot as plt

# Get the data from the provided code
data = New_df.groupby('Video title').sum().sort_values(by='Comment_ID',ascending= False).reset_index().head(5)

# Create the bar chart
plt.bar(data['Video title'], data['Comment_ID'])
plt.xlabel('Video Title')
plt.ylabel('Number of Comments')
plt.title('Most Commented Videos')
plt.xticks(rotation=90)
plt.show()

"""<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Q. What types of video titles and thumbnails drive the most traffic?
    
</h2>
</div>
    
</center>
"""

df = Video_df[['Video Title','Thumbnail link', 'Average View Percentage','Average Watch Time']].copy()
df.sort_values(by='Average Watch Time',ascending= False).drop_duplicates('Video Title')['Video Title'].head(10).values.tolist()

"""<center>
<div class="alert alert-block alert-info">
Video titles with words Live, Stream, Fundamentals and Data Science gets the most traffic


</div>
  </center>

<center>
<div style="color:;
           display:fill;
           border-radius:5px;
           background-color: mediumseagreen;
           font-size:110%;
           letter-spacing:0.5px">

<h2 style="padding: 10px;
              color:white;">Q. What types of videos have led to the most growth?
    
</h2>
</div>
    
</center>
"""

df=Aggregated_df[['Video','Video title','Sub­scribers gained' ]].copy()
df.sort_values(by='Sub­scribers gained',ascending= False).drop([0]).head(5)['Video title'].values.tolist()