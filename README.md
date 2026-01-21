# KL-Films-RAG
MVP RAG SYSTEM FOR FILM LISTINGS

## MVP DESIGN: 
RAG pipeline (no LLM to to give final context yet):

1) Load raw cinema listing data
2) Normalize + clean the data into a canonical format
3) Chunk the data into retrievable semantic units
4) Embed chunks into vectors
5) Store vectors in a local vector database
6) Embed user queries
7) Perform similarity search
8) Assemble retrieved chunks into a context payload

Design points: 
- Evaluate retrieval independently of generation
- Swap vector DBs or embedders later
- Add MCP or agent tooling without refactoring core logic




# semanitics: 

1) Typical user questions I want to be able to answer: 
2) 


# Points to come back to and understand: 
- point of normalization
- ideas behind the semantic units, .... , choice of vectorDB, dimensions of embedder, 


PROBLEM: Questions that return multiple results: because there are multiple answers. 
e.g. what films are on this weekend at the barbican? 
RAG not really suited to this: When storing embeddings in VDB need to split your raw data into semantic units, but RAG returns k best matches. 
So what it answers is composed of more semantic units than k?

Put another way: Correctness depends on coverage, not ranking.
RAG, by default, does: “Give me the top-k most relevant chunks.” -- but k is fixed, so for some problems this isn't appropraite -- unless we chunk such that a signle or a few chunks relaibly contain the answer.

Solutions: 

a) **chunk such that single semantic unit will have all info for single question**
This would mean: chunk in such a way that top k chunks will have the answer. 
-- ISSUE: infeasbile as space of possible questions too large (even if contrain the questions); answers to querstions would optimally require chunks of varying semantic size (which optimally need differtn D vectors for the encoding; whihc needs mutliple VDBs -- and then have issue of comparing answers)

b) **seperate concerns: use RAG only for the query interpretation matching against available data:** 
LLM-assisted semantic parsing → deterministic data access:

RAG allows me to map from english to fields in my data base (like cinemas I have films for).
So, I could use RAG to go from the english to the search fields in my data,
like actaul film titles, cinemas and from data ranges (like this weekend, next week,...) to searchable date range (2025-10-10 etc).
and then once best matches identified, I have my search fields, and I make deterministic function calls to search my structured data.

e.g. ""what films are on at the Barbican and BFI Southbank this weekend" -->

'''{
  "cinemas": ["barbican", "bfi_southbank"],
  "date_range": {
    "start": "2026-01-17",
    "end": "2026-01-18"
  },
  "intent": "list_films"
}'''

Then once field identifed: 
'''
search_films(
  cinemas = [...],
  start_date = ...,
  end_date = ...
)
'''

DESIGN THINKING: 
- would typical MCP not be better here? 
1) "what tools are in my MCP server, what args do they require"
-- I feel like RAG needed would be useful for looking up obscure names (like names of new cinemas or films)

THINK about: 
failure handling:
how to handle idata rage
how to handle cases where cinema not in my DB? 



-- Q: work through how this would work in practice🟡


But at that point, why not just use traditional code? Like a form the user fills out that then runs server side fucntions and returns it to the user? 


