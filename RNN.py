import nltk
nltk.download('punkt')
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input, Concatenate
from tensorflow.keras.utils import pad_sequences
import re
from collections import defaultdict
import heapq

# Step 1: Data Collection and Preprocessing
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

def preprocess_data(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    return tokens

preprocessed_messages = [preprocess_data(msg) for msg in messages]

# Step 2: Building the Phrase Tree with Priority Queue
def build_tree(data):
    tree = defaultdict(list)
    for message in data:
        for i in range(len(message) - 1):
            found = False
            for index, (neg_freq, word) in enumerate(tree[message[i]]):
                if word == message[i + 1]:
                    tree[message[i]][index] = (neg_freq - 1, word)
                    heapq.heapify(tree[message[i]])
                    found = True
                    break
            if not found:
                heapq.heappush(tree[message[i]], (-1, message[i + 1]))
    return tree

phrase_tree = build_tree(preprocessed_messages)

# Generate training data for the RNN model
def generate_rnn_training_data(data):
    X = []
    y = []
    for message in data:
        for i in range(len(message) - 1):
            X.append(message[:i + 1])
            y.append(message[i + 1])
    return X, y

X_rnn, y_rnn = generate_rnn_training_data(preprocessed_messages)

def augment_training_data(X, y, phrase_tree):
    augmented_X = []
    for seq, target_word in zip(X, y):
        freq_info = [freq for freq, word in phrase_tree[seq[-1]]]
        augmented_X.append(seq + freq_info)
    return augmented_X, y

X_augmented, y_augmented = augment_training_data(X_rnn, y_rnn, phrase_tree)

X_augmented = np.array(X_augmented)
y_augmented = np.array(y_augmented)

vocab_size = len(set([word for seq in preprocessed_messages for word in seq])) + 1
embedding_dim = 100
seq_length = max(len(seq) for seq in X_augmented)
num_freq_features = 3

input_sequence = Input(shape=(seq_length,))
freq_features = Input(shape=(num_freq_features,))

embedding_layer = Embedding(vocab_size, embedding_dim)(input_sequence)

lstm_output = LSTM(128)(embedding_layer)

concatenated_output = Concatenate()([lstm_output, freq_features])

output = Dense(vocab_size, activation='softmax')(concatenated_output)

model = Model(inputs=[input_sequence, freq_features], outputs=output)

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit([X_augmented[:, :seq_length], X_augmented[:, seq_length:]], y_augmented, epochs=10, batch_size=32)

def generate_rnn_suggestions(seed_word, phrase_tree, next_words=3):
    for _ in range(next_words):
        token_list = [seed_word]
        token_list = pad_sequences([token_list], maxlen=seq_length, padding='pre')
        freq_info = [freq for freq, word in phrase_tree[seed_word]]
        predicted_probs = model.predict([token_list, np.array([freq_info])])[0]
        predicted_index = np.argmax(predicted_probs)
        predicted_word = predicted_index
        seed_word += " " + predicted_word
    return seed_word.split()[1:]

next_word_suggestions = generate_rnn_suggestions("the", phrase_tree, next_words=3)
print("Next word suggestions from RNN with tree structure:", next_word_suggestions)
