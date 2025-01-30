# mp1
A small experiment in vector symbolic architectures and weightless neural networks

## Disclaimer
If you are a sympathizer/supporter of Sam Altman, Elon Musk, or Donald Trump, go away. If you're going to sit here and whine about "no politics" then go away. If you're not bothered by this, read on. 

## Introduction 
MP1 is a small (and badly written by a human) but hopefully meaningful experiment in artificial intelligence. It combines hyperdimensional computing and weightless neural networks. A great introduction to HD/VSA can be found [here](https://www.hd-computing.com/) and WNNs [here](https://www.geocities.ws/iwickert/presentation.html). Unlike ChatGPT and other LLMs, MP1 is able to learn in real time, and possesses a small capability to generalize and reason with uncertainty. 

## How it works 
I'm horrible at explaining things; Please read my code as best you can for the exact details. Here's an overview though:
1. A yes/no question is given to the program at the console
2. HD/VSA operations are used to transform the text into a 1024-bit binary pattern / vector
3. The pattern is then fed to a hierarchy of ramnet-like units (they're closer to VGRAMs, since they utilize hamming distances to find "close enough" matches).
4. The hierarchy will store the distributed representation of the question along with the answer; it will generate its own at all levels if it doesn't find an exact or close enough match.
5. The output is a simple "YES" or "NO" to the question.
6. If it turns out the answer to the question was wrong, you tell MP1 any sentence that has the word "incorrect" in it, and it will store the correct answer in real time.

It sounds too simple to work, but I highly suggest you review my code and try it yourself. Clone the repo and run MP1.py. Ask it questions like "Is Earth Blue" and "Am I a waffle" - if the answers are incorrect, tell it. Let it learn from you. 

I'm also quite new to using github and putting my code out for public scrutiny, but hopefully this catches on. But I call dibs on the phrase "memory is all you need" :) 

Have fun~
