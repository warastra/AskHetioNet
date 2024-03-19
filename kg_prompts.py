from llama_index.prompts import PromptTemplate
from llama_index.prompts.prompt_type import PromptType
import re

entity_classification_template= """The following are available node names in the knowledge graph
**node names**: {node_names} 

Extract out the entity mentioned in the questions and convert them to their closest equivalent node names then give the **modified question** as the final response

For example:
**Question**: Bagaimana pandangan golkar terhadap UU ITE
**Thought**: There are two entities mentioned in the question, 'golkar' and 'UU ITE' looking at the list of node names i found that 'golkar' is most similar to 'Golongan Karya' and 'UU ITE' is most similar to 'Revisi Undang-undang Informasi Dan Transaksi Elektronik (ITE)'
**Matched Entities**: [Golongan Karya,Revisi Undang-undang Informasi Dan Transaksi Elektronik (ITE)]
**Modified Question**:  Bagaimana pandangan Golongan Karya terhadap Revisi Undang-undang Informasi Dan Transaksi Elektronik (ITE)

**Question**: {question}
**Thought**:"""

entity_classification_promptTemplate = PromptTemplate(
    template = entity_classification_template,
    prompt_type=PromptType.CUSTOM
)

def entity_classification_parser(model_output:str):
    try:
        modified_question = re.search('\*\*Modified Question\*\*:(.*)', model_output).group(1)
        entities = re.search('\*\*Matched Entities\*\*:\s*\\[(.*)\\]', model_output).group(1)
        entities = entities.split(',')
    except:
        modified_question = model_output
        entities = ''
    return modified_question, entities

# If the question involve a political party or issue, always include their 'source' property in the constructed cypher's RETURN statement.

# If the question mention political party or issue, but is irrelevant to the graph schema, only return the cyher query to get the Party's or Issue's source property, 
# Example 3
# Question: Apakah Golongan Karya partai yg baik? 
# MATCH (p:Political_party)
# WHERE p.name = 'Golongan Karya'
# RETURN p.source as source

graph_q_with_ER_template = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement. 
Do not include any text except the generated Cypher statement in the final response.

Example 1
Question: How many Golongan Karya member is involved in corruption case?
MATCH (p:Political_party)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(c:Person)-[:IS_A_CORRUPTION_CONVICT_DUE_TO]->(:CorruptionCase)
WHERE p.name = 'Golongan Karya'
RETURN COLLECT(p.source) as source, COUNT(c) AS total_members_involved_in_corruption

Example 2
Question: Bagaimana pandangan Golongan Karya terhadap UU ITE? 
MATCH (p:Political_party)-[e]->(u:Law)
WHERE p.name = 'Golongan Karya'
    AND u.name = 'Revisi Undang-undang Informasi Dan Transaksi Elektronik (ITE)'
RETURN p.source as source, e.reason as reason, u.description as description


Question: {query_str}
"""
graph_q_with_ER_prompt = PromptTemplate(
    template = graph_q_with_ER_template,
    prompt_type=PromptType.TEXT_TO_GRAPH_QUERY
)

graph_response_answer_template="""The original question is given below.
This question has been translated into a Graph Database query.
Both the Graph query and the response are given below.
Given the Graph Query response, synthesise a response to the original question. always include the source whenever possible

Example 1
Original question: apakah kewarganegaraan ayah Barack Obama?
Graph query: MATCH (a:Person)-[:IS_SON_OF]->(b:Person)
WHERE a.name = 'Barack Obama'
RETURN a.source as source, b.nationality
Graph response: [{{'source': 'https://en.wikipedia.org/wiki/Barack_Obama', 'b.nationality': 'Kenya'}}]
Response: ayah Barack Obawa adalah warga negara Kenya. diambil dari 'https://en.wikipedia.org/wiki/Barack_Obama'

Example 2
Original question: who lead PKB?
Graph query: MATCH (person:Person)-[:IS_LEADER_OF]->(party:Political_Party)
WHERE party.name = 'PKB'
RETURN party.source as source, p.name 
Graph response: [{{'source': 'https://www.bijakmemilih.id/partaiprofil/partai-kebangkitan-bangsa', 'person.name': 'Muhaimin Iskandar'}}]
Response: PKB is led by Muhaimin Iskandar. sourced from 'https://www.bijakmemilih.id/partaiprofil/partai-kebangkitan-bangsa'

If the Graph response only contains information about the source, respond with the default response "Informasi tidak ditemukan, cari lebih lanjut di" + source 
Example 3
Original question: apakah Gerindra ingin menang pemilu 2024??
Graph query: MATCH (p:Political_party)-[v:VOTE_WON_IN]->(r:RegionVote)
WHERE p.name = 'Gerindra' AND v.election_year = 2024
RETURN p.source as source, v.percentage as percentage, r.name as region_vote
UNION
MATCH (p:Political_party)
WHERE p.name = 'Gerindra'
RETURN p.source as source, NULL as percentage, NULL as region_vote
Graph response: [{{'source': 'https://www.bijakmemilih.id/partaiprofil/partai-gerakan-indonesia-raya', 'percentage': None, 'region_vote': None}}]
Response: Informasi tidak ditemukan, cari lebih lanjut di 'https://www.bijakmemilih.id/partaiprofil/partai-gerakan-indonesia-raya'

Original question: {query_str}
Graph query: {kg_query_str}
Graph response: {kg_response_str}
Response:
"""
graph_response_answer_prompt = PromptTemplate(
    template = graph_response_answer_template,
    prompt_type=PromptType.QUESTION_ANSWER
)

refine_template = """The original query is as follows: {query_str}
We have provided an existing answer, including sources: {existing_answer}
We have the opportunity to refine the existing answer (only if needed) with some more context below.
------------
{context_msg}
------------
Given the new context, refine the original answer to better answer the query. If you do update it, please update the sources as well. If the context isn't useful, return the original answer.
Refined Answer: 
"""

refine_prompt = PromptTemplate(
    template = refine_template,
    prompt_type=PromptType.REFINE
)




new_graph_q_synthesis_template = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement. 
Do not include any text except the generated Cypher statement in the final response.
When looking to match Political_party or Person mentioned in the question, always convert them to lowercase first and look also at the lowercased **alias** or lowercased **index** field whenever possible. entity should match when either the name or the alias matched.
When looking to match Law mentioned in the question, ignore the word undang-undang, UU, or RUU mentioned in the question. use partial match with cypher contains clause instead of exact match

Example 2
Question: How many Golkar member is involved in corruption case?
MATCH (p:Political_party)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(c:Person)-[:IS_A_CORRUPTION_CONVICT_DUE_TO]->(:CorruptionCase)
WHERE toLower(p.name) = toLower('Golkar') OR toLower(p.index)=toLower('Golkar') OR toLower(p.alias)=toLower('Golkar')
RETURN COUNT(c) AS total_members_involved_in_corruption

Question: Bagaimana sikap Golkar dalam pembahasan RUU KUHP?
MATCH (p:Political_party)-[e]->(u:Law)
WHERE (toLower(p.name) = toLower('Golkar') OR toLower(p.index)=toLower('Golkar') OR toLower(p.alias)=toLower('Golkar'))
    AND (toLower(u.name) CONTAINS toLower('KUHP') OR toLower(u.index) CONTAINS toLower('KUHP'))
RETURN e.reason, e.source, u,description

Question:{query_str}
"""
new_graph_q_synthesis_promptTemplate = PromptTemplate(
    template = new_graph_q_synthesis_template,
    prompt_type=PromptType.TEXT_TO_GRAPH_QUERY
)

refine_template = """The original query is as follows: {query_str}
We have provided an existing answer, including sources: {existing_answer}
We have the opportunity to refine the existing answer (only if needed) with some more context below.
------------
{context_msg}
------------
Given the new context, refine the original answer to better answer the query. If you do update it, please update the sources as well. If the context isn't useful, return the original answer.
Refined Answer: 
"""

refine_prompt = PromptTemplate(
    template = refine_template,
    prompt_type=PromptType.REFINE
)

# modify the question as little as possible
chat_history_template= """Given a conversation (between User and Assistant) and a follow up message from User, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation. if the question is not in english, translate it to english.
**chat history**: {chat_history} 

**Question**: {question}
**Updated Question**:"""

chat_history_promptTemplate = PromptTemplate(
    template = chat_history_template,
    prompt_type=PromptType.CUSTOM
)