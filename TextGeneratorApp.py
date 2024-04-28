import tkinter as tk
from tkinter import scrolledtext
import nltk
import re
from collections import defaultdict
import heapq
nltk.download('punkt')


#simple UI for the text generator
#implement sample text data in messages
class TextingHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Texting Helper App")
        
        self.messages = [
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
        
        #process text and build priority tree
        self.preprocessed_messages = [self.preprocess_data(msg) for msg in self.messages]
        self.phrase_tree = self.build_tree(self.preprocessed_messages)
        
        self.create_widgets()
    
    def preprocess_data(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = nltk.word_tokenize(text)
        return tokens
    
    def build_tree(self, data):
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
    
    #returns an array of the words with the highest priority based on the previously inputted word
    def predict_next_words(self, user_input, num_predictions=3):
        words = user_input.split()
        last_word = words[-1] if words else ""
    
        if last_word in self.phrase_tree:
            top_words = heapq.nlargest(num_predictions, self.phrase_tree[last_word], key=lambda x: x[0])
            top_words_sorted = sorted(top_words, key=lambda x: x[0])
            return [word for freq, word in top_words_sorted]
        return []
    
    #generates the array of predicted words or returns idk if it hasn't been trained well on that certain word
    def generate_text(self, user_input):
        predictions = self.predict_next_words(user_input)
        if predictions:
            return " ".join(predictions)
        else:
            return "I don't know what to suggest."
        
    #small widget for input and output
    def create_widgets(self):
        self.input_label = tk.Label(self.root, text="Type your message:")
        self.input_label.pack()
        
        self.input_text = scrolledtext.ScrolledText(self.root, width=50, height=10, wrap=tk.WORD)
        self.input_text.pack()
        
        self.suggestion_label = tk.Label(self.root, text="Suggestions:")
        self.suggestion_label.pack()
        
        self.suggestion_text = tk.Text(self.root, width=50, height=3)
        self.suggestion_text.pack()
        
        self.submit_button = tk.Button(self.root, text="Generate", command=self.on_submit)
        self.submit_button.pack()
    
    #once submit is pressed the next predicted words are generated
    def on_submit(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            suggestion = self.generate_text(user_input.lower())
            self.suggestion_text.delete("1.0", tk.END)
            self.suggestion_text.insert(tk.END, suggestion)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextingHelperApp(root)
    root.mainloop()

