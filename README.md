# unsupervised_WSD_on_top_of_word2vec
This is a project based on the paper : 

      @misc{
      sun2017simple,
      title={A Simple Approach to Learn Polysemous Word Embeddings}, 
      author={Yifan Sun and Nikhil Rao and Weicong Ding},
      year={2017},
      eprint={1707.01793},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
      }  
 https://arxiv.org/abs/1707.01793#:~:text=In%20this%20paper%2C%20we%20propose,single%20pass%20over%20the%20data.
***********************************************************************************************************************************

The vectors generated by the Gensim word2vec model are considered as base vector embedding, because every word has only one vector corresponding to it, as there is no consideration for poysemous words in this kind of model.
Given a target word and its context we can construct a contextual embedding vector as a linear combination of weighted sum of its corresponding context words' base embedding vectors.
To achieve the above mentioned, the method is to first build a matrix W of V*V dimensions where V is the total vocabulary of the selected corpus. In the paper above, W[i,j] is defined as,

      W[i,j]=co-occurence of words i and j /(freq._of_word_i * freq_of_word_j)

   This matrix gives us a score of what words occur together frequently, meaning it tells us whether word j is a relevant context of the word i.I have been able to construct this Matrix W using brown corpus, even though I'm using a wiki corpus to train the gensim word2vec, Im using brown corpus to construct W because W takes up a huge amout of memory to store and brown is a smaller corpus suitable for this.

   According to the method if we have two usages of the word bank, example: (1)I was sitting by the side of the River bank. (2)I need to withdraw my savings from the bank.

then vector, 
                  
      bank1 =W[sitting,bank]*vector(sitting) + W[side,bank]*vector(side) + W[River,bank]*vector(river)
and,

      bank2 = W[need,bank]*vector(need) + W[withdraw,bank]*vector(withdraw) + W[savings,bank]*vector(savings)

The above representations mean that the target words can be represented as the sum of the vectors of their context. Here the vectors are directly taken from the word embedding (word2vec) trained on the Google news model. Also note that W[i,j] acts as a weight to each vector in the context to weigh the context word according to its relevance.
