from llama_index.prompts import PromptTemplate
from llama_index.prompts.prompt_type import PromptType
import re, json
from openai import OpenAI as OpenAI_cli

entity_labels_classification_template= """The following are available node types in a knowledge graph
**node_types**: {node_types} 
Label the entity mentioned in the question to their corresponding node types. Format the final entity labels as a JSON-readable dictionary of "entity_name":"node_type")

Example 1:
**Question**: What are the compounds that can cause mobilisation of tumour cell?
**Thought**: The question ask about compounds that may cause a SideEffect of mobilisation of tumour cell
**Entity Labels**: {{"mobilisation of tumour cell":"SideEffect"}}

Example 2:
**Question**: Can nicergoline treat bipolar symptom?
**Thought**: The question if a Compound named nicergoline is able to treat a Disease called bipolar
**Entity Labels**: {{"nicergoline":"Compound","bipolar":"Disease"}}

Example 3:
**Question**: is ASGR1 gene associated with disease that attacks digestive system?
**Thought**: The question ask if a Gene, ASGR1 is associated with disease affecting an Anatomy, digestive system
**Entity Labels**: {{"ASGR1":"Gene","digestive system":"Anatomy"}}

**Question**: {question}
**Thought**:"""

def entity_labels_parser(model_output:str):
    entity_labels = re.search('\*\*Entity Labels\*\*:\s*(.*)', model_output).group(1)
    return json.loads(entity_labels)

entity_matching_template= """Given an entity_name match it with the closest equivalent node names in a biomedical knowledge graph.
Format the answer as JSON-readable dictionary of "entity":"ClosestNodeNames" . always use double quote for the answer. Return back the entity if there is no close match.
Do not include the examples or the word 'json' in the output response. Strictly follow the output format in the examples.

Example 1
**entity**: nicergoline
**nodeNames**: Scopolamine,Nicergoline,Mannitol,Phosphoric Acid,Methanol
**MatchedNodeNames**:{{"nicergoline":"Nicergoline"}}

Example 2
**entity**: mobilisation of tumour cell
**nodeNames**: Melancholia,Haemophilia,Skin exfoliation,Pupils unequal,Ethanol,Tumour cell mobilisation
**MatchedNodeNames**:{{"mobilisation of tumour cell":"Tumour cell mobilisation"}}

Example 3
**entity**: bipolar
**nodeNames**: Melancholia,Haemophilia,Skin exfoliation,Pupils unequal,Ethanol,Tumour cell mobilisation
**MatchedNodeNames**:{{"bipolar":"bipolar"}}

**entity**: {entity}
**nodeNames**: {node_names}
**MatchedNodeNames**:"""

def entity_matching_parser(model_output:str):
    model_output = model_output.replace('json','')
    try:
        entity_matching = re.search('\*\*MatchedNodeNames\*\*:\s*(.*)', model_output).group(1)
    except TypeError:
        pass
    return json.loads(entity_matching)

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
Question: What are the common side effects for drugs that treats bipolar disorder and hypertension?
MATCH (d:Disease)-[:TREATS]-(c:Compound)-[:CAUSES]->(s:SideEffect)
WHERE d.name = 'bipolar disorder' or d.name = 'hypertension'
RETURN s.name as SideEffect, COUNT(distinct c) AS drugCount
ORDER BY drugCount DESC

Example 2
Question: Name three genes in chromosome 2 associated with disease that attacks both digestive system and hematopoietic system? 
MATCH (g:Gene)-[:IS_ASSOCIATED_WITH]-(d:Disease)-[:LOCALIZES]-(a:Anatomy)
WHERE  g.chromosome = '2'
    AND (a.name = 'digestive system' or a.name = 'hematopoietic system')
WITH g.name as gene_name, d, count(distinct a) as AnatomyCount
WHERE AnatomyCount > 1
RETURN gene_name, d.name as disease

Example 3
Question: Give the inchi key of three drugs that can be used to alleviate symptoms for disease that attacks digestive system or the hematopoietic system
MATCH (c:Compound)-[:PALLIATES]-(d:Disease)-[:LOCALIZES]-(a:Anatomy)
WHERE  a.name = 'digestive system' or a.name = 'hematopoietic system'
RETURN c.name as Compound, c.inchikey as Compound_InChiKey, d.name as Disease, a.name as Affected_Anatomy
LIMIT 3

Example 4
Question: Give the inchi of three drugs that indirectly targets the SERPINF2 gene
MATCH (c:Compound)-[r]-(g:Gene)-[e:REGULATES]-(g2:Gene)
WHERE g2.name='SERPINF2'
RETURN c.name as Compound, c.inchi as Compound_InChi, r as Compound_Gene_Relationship, g.name as RegulatingGene, e, g2.name as RegulatedGene
LIMIT 3

Question: {query_str}
"""
graph_q_with_ER_prompt = PromptTemplate(
    template = graph_q_with_ER_template,
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
