# Summary:
Our program takes in a database of text messages and provides the user with AI generated text suggestions to help them finish their sentences. 
By running the TextAppGenerator.py file, a GUI will pop up which allows a user to input a sentence of their desired length and at any point they can press the generate button which will provide 3 words that would best finish the sentence based on the user’s text history. 


**Note:** NLTK must be installed : https://www.nltk.org/install.html

<h3>How to run:</h3>

    - 💻 TextGenerator.py will work with modification of the variable “current_word”

    - 💭 Insert history by setting “messages” equal to a list of strings

       - The longer the history the higher the accuracy but the runtime will also take a hit.
   
       - The shortness of the algorithm allows for many words to be added before a difference is seen, but this is still something to be cautious of. 
   
       - Accompanying deletion algorithm coming soon!
   
    - 🖊️ Test algorithm by modifying current_word variable
  
        - Implementation of a sort of I/O around the algorithm while updating current_word will also operate as desired! 
    
        - Try ours with TestAlgorithmApp.py!
<h3>More information on this project</h3>
🖇️ <a href="https://docs.google.com/presentation/d/e/2PACX-1vRl5zSYAJrDzXSpoXI3D7_FHuZENPaaj4w15Jj_SGszEpqxiiaQbEetKpc-nC35JZSgNip-u3unUZex/pub?start=false&loop=false&delayms=3000">Text Generator Slides</a>
