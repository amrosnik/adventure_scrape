# adventure_scrape
An adventure in text mining.

Here please find the code to create a pandas DataFrame of Adventure Time transcripts, applied in this order:
-- adventure_scrape.py
-- adventure_dataframe.py
-- adventure_cleaning.py

.pkl files of the DataFrames are included for your convenience; the ones with the most recent commit dates are the most relevant! 

From there, you can explore the data via text mining statistics and plots:
-- adventure_analysis.py 

To generate data for the character RNN InFINNerator, use:
-- get_finn_data.py
-- format_finn.py

to create the finn-related .pkl pickles. finn_just_dialogue.pkl is the initial dataset for InFINNerator.

Finally, the Google Colabs notebook INFINNERATOR_example.ipynb is the way to create the char RNN. 
It's a mini-batched LSTM network. I tried several different architectures and didn't get excellent 
performance, but please write me if you do! 


Cheers,
Andreana


