custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

legal_analysis_prompt = """
Analyze this legal document provided in the context and identify potential legal issues, risks, and opportunities. Consider relevant case law and statutory provisions.
Draft a summary of the key terms and implications of this legal document.
Context: {context} 
Answer:
"""

document_review_promt = """
Review this contract provided in the context and identify potential ambiguities, inconsistencies, and clauses that may be risky for client.
Context: {context} 
Answer:
"""