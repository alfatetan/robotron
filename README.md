# Robotic calls

#### Notice:

_This is the very first version of the automated phone conversation system (a pilot project). Due to the development of this area of AI, this code has become irrelevant. I left this repository as an example of my former experience. This version of the automated phone conversation system has been moved to the public with the customer's permission. Unfortunately, all remarks and notes made in the code are in Russian, as the project itself was launched in Russia in 2018. All phone numbers, tokens, and codes are now completely irrelevant._

---

#### System requirements

This system was implemented on CentOS v.7 LTS, Asterisk v.13 LTS, and Python v.3.6
Unfortunately, the file requirenments.txt was lost, and it is hard for me to reconstruct all dependencies for this project from memory.

---

#### How this code works

- A special conversation script consisting of blocks was written before running.
- Each block consisted of a voiced or synthesized audio file and conditions for moving to the next block.
- A "graph system" between blocks of conversation was used to describe the algorithm. In this way, conditional transitions and even returns to previous blocks could be used.

<img align="center" width="250" src="https://github.com/alfatetan/robotron/assets/46200647/3d424758-5db6-400d-926c-1eb10bd13aab">
  
  ![IMG_0725](https://github.com/alfatetan/robotron/assets/46200647/3d424758-5db6-400d-926c-1eb10bd13aab)

- The client was called using a pre-prepared list.
- Yandex Cloud Speech Recognition Service was used for speech recognition and synthesis.
- To simulate natural communication, a function allowing to interrupt the interlocutor's speech was built in.
- An algorithm for filtering profanity was also implemented.

<img align="center" width="100" height="100" src="https://github.com/alfatetan/robotron/assets/46200647/3d424758-5db6-400d-926c-1eb10bd13aab">

[![Sample dialogue and logging](https://github.com/alfatetan/robotron/assets/46200647/7bdc639d-cbc9-4657-ac20-983928b58a69)](https://youtu.be/ib41Xp70UAo)
