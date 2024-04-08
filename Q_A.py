#%%
# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import re

#%%
# Load Quran dataset
quran_english = pd.read_csv('en.yusufali.csv')

#%%
#
quran_english.shape
#The Quran comprises 6,236 verses, divided into 114 chapters known as surahs. Each surah contains a variable number of verses, referred to as ayat.
#%%
# Load Surah names
surah_names = pd.read_csv('surah_names_english.csv', names=['Surah', 'Surah Name'])
surah_names["Surah Name"] = surah_names["Surah Name"].str[1:]

#%%
# Merge surah names with Quran dataset
quran_english_with_surah = quran_english.merge(surah_names, on='Surah')
quran_english_with_surah.index = np.arange(1, 6236 + 1)
quran_english_with_surah
#%%
# Checking for Null Values
quran_english.isna().sum()

#%%
# Numbers of verses in each chapter.
quran_english_with_surah["Surah Name"].value_counts()

#%%
# Function to plot count plot
def quran_chapters_verses_countplot(dataframe, y_axis, title):
    # Setting figures size and theme
    plt.figure(figsize=(6, 10))
    sns.set_style('darkgrid')

    # Countplot to count the number of verses of each chapter and plot
    ax = sns.countplot(data=dataframe, y=y_axis, palette='viridis')

    # Setting labels for each bar
    for container in ax.containers:
        ax.bar_label(container, size=10, padding=2)

    # Customizing plot
    ax.set_title(title, fontweight='bold', fontsize=12)
    ax.set_ylabel('Chapters (Surahs)', fontweight='bold')
    ax.set_xlabel('Verses', fontweight='bold')
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300])

    plt.show()

#%%
# Splitting quran dataset into 3 parts

# Plotting count plot for verses in chapters 1 - 39
quran_chapters_verses_countplot(quran_english_with_surah[quran_english_with_surah['Surah'] < 40], 'Surah Name', 'No. of verses in each chapter(surah) 1 - 39')

# Plotting count plot for verses in chapters 40 - 79
quran_chapters_verses_countplot(quran_english_with_surah[(quran_english_with_surah['Surah'] > 39) & (quran_english_with_surah['Surah'] < 80)], 'Surah Name', 'No. of verses in each chapter(surah) 40 - 79')

# Plotting count plot for verses in chapters 80 - 114
quran_chapters_verses_countplot(quran_english_with_surah[quran_english_with_surah['Surah'] > 79], 'Surah Name', 'No. of verses in each chapter(surah) 80 - 114')

# Surah Al-Baqarah is the lengthiest Surah : Contains the longest verse in the Quran, Ayat al-Kursi (Verse of the Throne), highlighting Allah's greatness.

#%%
# Function to generate word cloud
def word_cloud_generator(text_corpus, stopwords, title, maxwords):
    word_cloud = WordCloud(background_color='white', stopwords=stopwords, height=1080, width=1920, max_words=maxwords)
    word_cloud.generate(text_corpus)

    plt.figure(figsize=(12, 6))
    plt.imshow(word_cloud)
    plt.title(title, fontweight='bold', fontsize=12)
    plt.axis('off')
    plt.show()

# Define custom stopwords
custom_stopwords = ['ye', 'verily', 'will', 'said', 'say', 'us', 'thy', 'thee', 'O', 'except', 'Nay',
                    'thou', 'hath', 'Thus', 'none', 'therein', 'come', 'came', 'even', 'two', 'word',
                    'every', 'let', 'thing', 'with', 'whose', 'forth', 'wouldst', 'set', 'unto','make','good','day',]

# Update STOPWORDS set
STOPWORDS.update(custom_stopwords)

#%%
# Function to generate word cloud for a specific surah
def generate_surah_word_cloud(quran_data, surah_number, max_words=50):
    surah_text = quran_data[quran_data['Surah'] == surah_number]['Text'].str.cat(sep=' ')
    surah_name = quran_data[quran_data['Surah'] == surah_number]['Surah Name'].iloc[0]
    word_cloud_generator(surah_text, STOPWORDS, f'Surah {surah_name} Word Cloud', max_words)

#%%
# Generate word cloud for Surah Al-Baqarah (Surah 2)
generate_surah_word_cloud(quran_english_with_surah, 2)

# Generate word cloud for Surah Yunus (Surah 10)
generate_surah_word_cloud(quran_english_with_surah, 10)

# Generate word cloud for Surah Ash-Shu'ara' (Surah 26)
generate_surah_word_cloud(quran_english_with_surah, 26)

#%%
# Function to plot frequency of prophet names
def plot_prophet_names(dataframe, title):
    prophet_names = ["Isma'il", 'Elisha', 'Zul-Kifl', 'Jesus', 'Moses', "Shu'aib", 'Jacob', 'Lut',
                     'Joseph', 'Isaac', 'Job', 'Aaron', 'Abraham', 'Noah', 'Adam', 'Hud', 'Solomon', 
                     'David', 'Zakariya', 'Yahya', 'Elias', 'Jonah', 'Idris', 'Salih', 'Muhammad']
    prophet_names_freq = {}
    for prophet in prophet_names:
        prophet_names_freq[prophet.lower()] = 0

    for verse in dataframe['Text']:
        words = verse.split(' ')
        for word in words:
            word = re.sub('[^a-zA-Z-\']', '', word.lower())
            if word in prophet_names_freq:
                prophet_names_freq[word] += 1

    prophet_names_df = pd.DataFrame({'Name': list(prophet_names_freq.keys()), 'Frequency': list(prophet_names_freq.values())})
    prophet_names_df['Name'] = prophet_names_df['Name'].str.capitalize()

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    sns.set_style('darkgrid')
    ax = sns.barplot(data=prophet_names_df, x='Name', y='Frequency', palette='husl')

    for container in ax.containers:
        ax.bar_label(container, size=10, padding=2)

    ax.set_title(title, fontweight='bold', fontsize=12)
    ax.set_ylabel("Count", fontweight='bold')
    ax.set_xlabel("Prophets", fontweight='bold')
    ax.tick_params('x', rotation=45)

    plt.show()

#%%
# Plotting frequency of prophet names
plot_prophet_names(quran_english, 'Frequency of prophet names in Quran (may vary)')

#%%
# Function to generate word cloud
def word_cloud_generator(text_corpus, stopwords, title, maxwords):
    word_cloud = WordCloud(background_color='white', stopwords=stopwords, height=1080, width=1920, max_words=maxwords)
    word_cloud.generate(text_corpus)

    plt.figure(figsize=(12, 6))
    plt.imshow(word_cloud)
    plt.title(title, fontweight='bold', fontsize=12)
    plt.axis('off')
    plt.show()

#%%
# Extracting each verse and storing them in a string
quran_text = ""
for lab, row in quran_english.iterrows():
    quran_text += row['Text']

#%%
# Function to generate word cloud
def word_cloud_generator(text_corpus, stopwords, title, maxwords):
    word_cloud = WordCloud(background_color='white', stopwords=stopwords, height=1080, width=1920, max_words=maxwords)
    word_cloud.generate(text_corpus)

    plt.figure(figsize=(12, 6))
    plt.imshow(word_cloud)
    plt.title(title, fontweight='bold', fontsize=12)
    plt.axis('off')
    plt.show()

#%%
# Generating word cloud for Quran
word_cloud_generator(quran_text, STOPWORDS, 'Quran Word Cloud', 100)

#%%
# List of important terms
important_terms = ['Prayer', 'Charity', 'Justice', 'Peace', 'Patience', 'World', 'Heaven', 'Forgive', 'Wisdom', 'Hereafter']

#%%
# Plotting frequency of important terms
terms_list_freq = {}
for term in important_terms:
    terms_list_freq[term.lower()] = 0

for lab, row in quran_english.iterrows():
    ayat_word_list = row['Text'].split(' ')
    for word in ayat_word_list:
        word = word.lower()
        pattern = re.compile('[^a-zA-Z]')
        word = pattern.sub('', word)
        if word in terms_list_freq:
            terms_list_freq[word] += 1
        elif any(term in word for term in terms_list_freq):
            for term in terms_list_freq:
                if term in word:
                    terms_list_freq[term] += 1

terms_df = pd.DataFrame({'Term': list(terms_list_freq.keys()), 'Freq': list(terms_list_freq.values())})
terms_df['Term'] = terms_df['Term'].str.capitalize()

#%%
# Plotting frequency of important terms
plt.figure(figsize=(8, 6))
sns.set_style('darkgrid')
ax = sns.barplot(data=terms_df, x='Term', y='Freq', palette='crest_r')

for container in ax.containers:
    ax.bar_label(container, size=15, padding=-30, color='white', rotation=90)

ax.set_title("Some Important things which Quran has emphasized", fontweight='bold', fontsize=12)
ax.set_ylabel("No. of times mentioned (English translation) (may vary)", fontweight='bold')
ax.set_xlabel("Terms", fontweight='bold')

plt.show()

#%%
# List of condemned terms
condemned_terms = ['Injustice', 'Oppress', 'Adultery', 'Hell', 'Satan', 'Wrongdoing', 'Resurrection', 'Hypocrite', 'Liar', 'Greed']

terms_list_freq = {}
for term in condemned_terms:
    terms_list_freq[term.lower()] = 0

for lab, row in quran_english.iterrows():
    ayat_word_list = row['Text'].split(' ')
    for word in ayat_word_list:
        word = word.lower()
        pattern = re.compile('[^a-zA-Z]')
        word = pattern.sub('', word)
        if word in terms_list_freq:
            terms_list_freq[word] += 1
        elif any(term in word for term in terms_list_freq):
            for term in terms_list_freq:
                if term in word:
                    terms_list_freq[term] += 1

terms2_df = pd.DataFrame({'Term': list(terms_list_freq.keys()), 'Freq': list(terms_list_freq.values())})
terms2_df['Term'] = terms2_df['Term'].str.capitalize()

#%%
# Plotting frequency of condemned terms
plt.figure(figsize=(8, 6))
sns.set_style('darkgrid')
ax = sns.barplot(data=terms2_df, x='Term', y='Freq', palette='rocket')

ax.set_title("Some important terms which Quran has condemned and warned", fontweight='bold', fontsize=12)
ax.set_ylabel("No. of times mentioned (English translation) (may vary)", fontweight='bold')
ax.set_xlabel("Terms", fontweight='bold')
ax.tick_params('x', rotation=45)

plt.show()

# %%
# List of places
places = ['Egypt', 'Medina', 'Babylon', 'Saba', 'Midian', 'Sinai']

# %%
# Convert all places to lowercase
places_lower = [place.lower() for place in places]

# %%
# Initialize a dictionary to store place counts
place_counts = {place: 0 for place in places_lower}

# Iterate through the verses and count the occurrences of each place
for verse in quran_english['Text']:
    verse_lower = verse.lower()
    for place in places_lower:
        if place in verse_lower:
            place_counts[place] += 1

# %%
# Convert the dictionary to a DataFrame for plotting
places_df = pd.DataFrame({'Place': [place.capitalize() for place in place_counts.keys()], 'Count': list(place_counts.values())})

# %%
# Plot the counts
plt.figure(figsize=(10, 6))
plt.bar(places_df['Place'], places_df['Count'], color='skyblue')
plt.xlabel('Place')
plt.ylabel('Count')
plt.title('Occurrences of Places in the Quran')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
#Surah Al-Kawthar: One of the shortest chapters in the Quran, consisting of only three verses, emphasizing blessings bestowed upon Prophet Muhammad.
#Surah Al-Baqarah: Contains the longest verse in the Quran, Ayat al-Kursi (Verse of the Throne), highlighting Allah's greatness.
#Surah Al-Fatiha: Known as the "Mother of the Quran," recited in every unit of Muslim prayer (Salah), seeking guidance and mercy from Allah.
#Surah Al-Mulk: Emphasizes accountability in the afterlife and reflection on Allah's creation.
#Surah Al-Isra: Narrates Prophet Muhammad's miraculous journey from Mecca to Jerusalem and ascension to the heavens.
#Surah Al-Kahf: Contains four stories imparting moral lessons, including encounters between Prophet Moses and Khidr.
#Surah Al-Fil: Recounts the destruction of Abraha's army of elephants attempting to attack the Kaaba in Mecca.
#Surah Al-Masad: Condemns Abu Lahab and his wife for hostility towards Prophet Muhammad, predicting their punishment.
#Surah Al-Ikhlas: Affirms the oneness of Allah, highly revered and frequently recited for spiritual connection.
#Surah An-Nas: Seeks refuge in Allah from Satan's evil whispers, emphasizing protection from harm and malevolent influences.
