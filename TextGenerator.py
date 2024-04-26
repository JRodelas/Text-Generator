import nltk
nltk.download('punkt')
import re # used to preprocess data (remove characters)
import nltk # natural language toolkit; used to tokenize the input data into a list of words
from collections import defaultdict # used to create dictionary where each word maps to a list of tuples, helping construct the tree
import heapq # used for the max heap data structure to implement priority queue

# Step 1: Data Collection and Preprocessing
# Define a list of sample messages (can be user's message history); Replace or expand as needed with actual data.
messages = [
  "Hey there! How's your day going?",
  "I just finished reading a great book. Have you read anything interesting lately?",
  "What's your favorite movie of all time?",
  "Do you prefer coffee or tea?",
  "I'm thinking of redecorating my room. Any suggestions?",
  "Just saw the most beautiful sunset. Nature never fails to amaze me.",
  "Did you hear about the new restaurant that opened downtown?",
  "I'm so excited for my upcoming vacation. Any travel tips?",
  "Sometimes I wish I could just teleport to my favorite place.",
  "Do you believe in aliens?",
  "I can't stop listening to this new song. It's stuck in my head!",
  "There's nothing better than a cozy night in with a good movie.",
  "What's your go-to comfort food?",
  "I wish I could speak another language fluently.",
  "Have you ever tried bungee jumping? It's on my bucket list.",
  "I'm feeling really motivated today. Ready to tackle anything!",
  "Do you think technology is making us more or less connected?",
  "Just finished a workout and feeling pumped!",
  "Life is full of surprises, isn't it?",
  "What's the best piece of advice you've ever received?",
  "I'm craving something sweet. Ice cream or cake?",
  "The stars look amazing tonight. Wish I had a telescope!",
  "I'm so grateful for all the amazing people in my life.",
  "What's your favorite childhood memory?",
  "I love getting lost in a good book. It's like entering another world.",
  "It's the little things in life that bring the most joy.",
  "I've been binge-watching this TV show and I can't get enough of it.",
  "Life is like a rollercoaster, full of ups and downs.",
  "I can't wait for summer to arrive. Beach days are the best!",
  "Just had the most delicious meal. I'm officially stuffed!",
  "What's the most adventurous thing you've ever done?",
  "Do you believe in destiny?",
  "I'm in desperate need of a vacation. Somewhere tropical, perhaps?",
  "Sometimes I wish I could turn back time and relive certain moments.",
  "I'm trying to learn how to cook. Do you have any easy recipes?",
  "Today's weather is perfect for a hike. Time to get outdoors!",
  "What's your favorite thing to do on a lazy Sunday?",
  "I'm feeling a bit nostalgic today. Remembering the good old days.",
  "I'm so grateful for this beautiful day. Life is truly wonderful.",
  "I'm convinced that laughter is the best medicine.",
  "I just adopted a pet. Any advice for new pet owners?",
  "What's the most beautiful place you've ever visited?",
  "I believe that everything happens for a reason.",
  "Just got back from a road trip. It was such an adventure!",
  "I wish I could travel back in time and witness a historical event.",
  "Do you have any hidden talents?",
  "I'm amazed by the power of human creativity.",
  "What's the best concert you've ever been to?",
  "I'm determined to make today a great day!",
  "Do you think aliens exist?",
  "I'm feeling inspired to start a new hobby. Any suggestions?",
  "There's nothing like a good cup of tea to warm you up on a cold day.",
  "I'm so grateful for the simple pleasures in life.",
  "What's your favorite thing about yourself?",
  "I've been thinking about taking up meditation. Have you tried it?",
  "Life is too short to hold grudges. Forgiveness is key.",
  "I'm so excited for the weekend. Any fun plans?",
  "How was your day today?",
  "How was your day yesterday?",
  "How is your day going?",
  "What is your goto restaurant?",
  "Do you prefer sunrise or sunset?",
  "I believe in the power of positivity.",
  "Just saw a shooting star. Made a wish!",
  "What's your favorite holiday tradition?",
  "I'm feeling a bit overwhelmed today. Any advice for managing stress?",
  "I'm so thankful for all the blessings in my life.",
  "I'm feeling a bit restless. Maybe I should go for a walk.",
  "What's the best piece of advice you've ever given someone?",
  "I believe that kindness can change the world.",
  "Do you think it's important to set goals?",
  "I'm so grateful for all the opportunities life has given me.",
  "What's the most valuable lesson you've learned in life?",
  "I'm feeling a bit lost lately. Trying to find my way.",
  "I'm so thankful for all the love and support in my life.",
  "I believe that laughter is the best medicine.",
  "I am feeling pumped about the concert tonight.",
  "I am feeling overwhelmed today with work.",
  "Are you feeling overwhelmed?",
  "I am feeling really tired today.",
  "I am feeling pumped up for this Giants game.",
  "What's your favorite way to unwind after a long day?",
  "Do you have any regrets in life?",
  "I'm feeling really positive about the future.",
  "What's the most memorable dream you've ever had?",
  "I believe that everything happens for a reason.",
  "I'm so grateful for the beauty of nature.",
  "What's your favorite childhood game?",
  "I'm so excited for the holidays. It's my favorite time of year!",
  "Do you believe in second chances?",
  "I'm feeling really inspired today. Ready to take on the world!",
  "What's your favorite thing about yourself?",
  "I'm feeling a bit overwhelmed with work. Need to find a balance.",
  "I'm so grateful for all the amazing people in my life.",
  "What's your favorite way to relax and unwind?",
  "I'm feeling a bit restless today. Maybe I need a change of scenery.",
  "I'm so thankful for all the opportunities life has given me.",
  "What's the best piece of advice you've ever received?",
  "I'm feeling a bit nostalgic today. Remembering the good old days.",
  "I believe that laughter is the best medicine.",
  "What's the most adventurous thing you've ever done?",
  "I'm feeling really positive about the future.",
  "Do you believe that everything happens for a reason?",
  "I'm so grateful for all the love and support in my life."
]

# Preprocess text data to prepare for storing in tree: converts all text to lowercase to ensure uniformity, removes all
# non-alphanumeric characters (punctuation and emojis) to focus solely on words, and tokenizes the cleaned text into individual words.
# Function takes in a string that needs preprocessing and returns a list of word tokens extracted from the input text.
def preprocess_data(text):
    text = text.lower()  # convert text to lowercase for consistency
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation, special characters, and emojis, cleaning the text to consist only of words and spaces
    tokens = nltk.word_tokenize(text)  # split the text into words using nltk's word tokenizer
    return tokens

# Apply preprocessing to each message in the list
preprocessed_messages = [preprocess_data(msg) for msg in messages]

# Step 2: Building the Phrase Tree with Priority Queue

# Builds a phrase tree with a max-heap structure to keep track of the most frequent subsequent words.
# Each word in the processed data serves as a key in a dictionary.
# Each key's value is a list of tuples, where each tuple contains a word and its negative frequency.
# Words are stored in a max-heap based on their negative frequency to prioritize higher frequencies.
# Function takes in the list of preprocessed messages and returns a dictionary where keys are words and values are lists functioning as heaps.
def build_tree(data):
    tree = defaultdict(list) # defaultdict(list) is used to create a dictionary where each word maps to a list of tuples; each tuple containing a subsequent word and its negative frequency
    for message in data:
        for i in range(len(message) - 1):
            found = False
            # check if the subsequent word already exists in the heap
            for index, (neg_freq, word) in enumerate(tree[message[i]]):
                if word == message[i+1]:
                    # increment the count of this word in the heap
                    tree[message[i]][index] = (neg_freq - 1, word)
                    heapq.heapify(tree[message[i]])  # re-heapify to maintain heap properties
                    found = True
                    break
            if not found:
                # if the word is not in the heap (hasn't been used yet), add it with an initial frequency of -1
                heapq.heappush(tree[message[i]], (-1, message[i+1]))
    return tree

# Construct the phrase tree from the preprocessed data
phrase_tree = build_tree(preprocessed_messages)

# Function to predict the next 3 most frequent words along with their frequencies using the phrase tree.
# Utilizes a max-heap to efficiently find the top 3 frequent following words
# Function takes in the tree where each key is a word and its value is a heap of next words, the word to predict the next 3 of,
# and the number of next predictions to return (in this case we are returning the next 3, but we can change this as pleased). The function then
# returns a list of tuples, containing the top 3 next words and their respective frequencies.
def predict_next_words(tree, word, num_predictions=3):
    if word in tree:
        # retrieve the top elements from the heap, sorted by negative frequency
        top_words = heapq.nlargest(num_predictions, tree[word], key=lambda x: x[0])
        # sort these words by frequency in descending order
        top_words_sorted = sorted(top_words, key=lambda x: x[0])
        return [(word, -freq) for freq, word in top_words_sorted]
    return []

# Predicting the next words for a given word; change 'current_word' accordingly
current_word = 'the'
predicted_words = predict_next_words(phrase_tree, current_word)
print(f"Next word suggestions for '{current_word}': {predicted_words}")
