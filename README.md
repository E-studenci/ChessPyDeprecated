# ChessPy
<img src="https://user-images.githubusercontent.com/67602274/120203000-8bce5380-c227-11eb-8ae0-da9fb82d60c2.png" height="200"/>

- [ChessPy](#ChessPy)
  * [Introduciton](#Introduciton)
  * [General Modules](#General-Modules)
    + [Chess](#Chess)
    + [Engine](#Engine)
    + [GameMenager](#GameMenager)
    + [GUI](#GUI)
    + [NeuralNetworks](#NeuralNetworks)
  * [Some games](#Some-games)
    + [Game1](#Game-1)
    + [Game 2](#Game-2)
  * [Final](#Final)
## Introduciton
The idea for the project has not appeared out of nowhere. Before the semester even started, we already wanted to take part in something like that, but the lack of motivation, and the vision of countless hours that we would have to spent to achieve any progress has turned us down. The opportunity that this course presented to us was too good to just let it slip right through our fingers. It enabled us to learn a bunch of useful python applications, how neural networks work, working with TensorFlow and many more. It is a tribute to a beautiful game of chess.

## General-Modules
### Chess
Here stands the core of our application. Life of every chess piece, every board and every move starts here. It is responsible for representing the chessboard, all the pieces, applying rules and sticking to them. It counts possible moves for each player and helps  maintaining balance in the universe of chess.
### Engine
Here we keep all the algorithms for our automated bots to find the correct moves. A lot of them are design to run multithreaded and are optimized for high performance. Lets 
show a few of them here to better understand how it all works.
##### AlphaBeta pruning:
Deisgned for finding the best move in a tree like structure. It is a recursive algorithm that cuts off all the unnecessary branches and it is a big improvement from a simple MiniMax.
</br><img src="https://user-images.githubusercontent.com/67602274/120220504-19686e00-c23d-11eb-9d98-a73a1df16094.png" height=200/>
##### Move ordering:
Some moves have a higher chance of being better then the others. For example, a capture has a greater probability of leading to a victory then a boring pawn move. Taking that into consideration we can improve our AlphaBeta algorithm significantly.
##### Board evaluation:
Multiple algorithims that together evaluate the position on the board. Combine that with some biased values, and you have got a working evaluator. Easy as pie.
### GameMenager
GameMenager is responsible for menaging the game between two playters. It is a multithreaded process that keeps the game of chess running and transfers nessesery informations between threads.
### GUI
For our GUI package we used pygame because it was simple enough for us to understand it and complex enough for us to not get bored with it. There is no "Button" object in there that you can just slap into your code and call it a day. Everything had to be designed with care and patience. Things like antialiasing, switch model, buttons, blurring and many more are included to maximize the enjoyment and good look of our application.
</br><img src="https://user-images.githubusercontent.com/67602274/120230052-c7c8df00-c24e-11eb-8e83-31e73bf4bd6f.png" height=400/>

### NeuralNetworks
The application is able to create datasets for neural network to train on from fen data, create and train models and evaluate them.  The models can be either convolutional or residual. There are 4 trained models included into our github data and all of them are able to play the game at a deacent level.

## Some-games
Here are some games against real players played at chess.com.
#### Game-1
Our bot plays black against an 800 rating player. It has choosen the Nimzowitsch-Defense, a great choice for agresive and quick games. As you can see the bot won it without any problems.
</br><img src="https://user-images.githubusercontent.com/67602274/120238701-06659600-c25d-11eb-86fe-08a75234d9a7.gif" height=400/>
#### Game-2
This time the bot went with the Barnes opening which is extremely popular in high level games. The incredible breakthrough happened at the 22nd move, when the bot trapped his opponents rook with his knight. After that it was just a formality to finish the job. The game ended with an incredible checkmate delivered by a rook.
</br><img src="https://user-images.githubusercontent.com/67602274/120239832-76751b80-c25f-11eb-9175-c4bfb7de189f.gif" height=400/>
## Final
You can dowload release, and play it by yourself but to open the game you have do download Cuda enviroment and cDNN. 
