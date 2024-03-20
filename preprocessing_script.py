import pandas as pd
import json 

# Read in the hetionet zipped JSON file available at https://github.com/hetio/hetionet/tree/main/hetnet/json
with open('hetionet-v1.0.json', 'rb') as f:
    hetnet = json.load(f)

# Reading Nodes and convert to CSV file to be uploaded to Neo4j Aura instance
for nodeTypes in hetnet['metanode_kinds']:
    subset_hetnet = [x for x in hetnet['nodes'] if x['kind']==nodeTypes]
    df = pd.DataFrame(subset_hetnet)
    df['source'] = [x['source'] for x in df['data']]
    df['license'] = [x['license'] for x in df['data']]
    df['url'] = [x['url'] if 'url' in x.keys() else '' for x in df['data']]
    if nodeTypes == 'Gene':
        df['description'] = [x['description'] for x in df['data']] 
        df['chromosome'] = [x['chromosome'] if 'chromosome' in x.keys() else '' for x in df['data']]
    if nodeTypes == 'Anatomy':
        df['mesh_id'] = [x['mesh_id'] for x in df['data']] 
        df['bto_id'] = [x['bto_id'] if 'bto_id' in x.keys() else '' for x in df['data']]
    if nodeTypes == 'Compound':
        df['inchikey'] = [x['inchikey'] for x in df['data']] 
        df['inchi'] = [x['inchi'] for x in df['data']]
    if nodeTypes == 'Pharmacologic Class':
        df['class_type'] = [x['class_type'] for x in df['data']]
    df = df.drop(columns=['data'])
    df.to_csv(r'hetiocsv\{}_nodes.csv'.format(nodeTypes), index=False)
    

# Reading Edges and convert to CSV file to be uploaded to Neo4j Aura instance
for metaEdge in hetnet['metaedge_tuples']:
    edgeTypes = metaEdge[2]
    sourceTypes = hetnet['kind_to_abbrev'][metaEdge[0]]
    targetTypes = hetnet['kind_to_abbrev'][metaEdge[1]]
    subset_hetnet = [x for x in hetnet['edges'] if x['kind']==edgeTypes]
    df = pd.DataFrame(subset_hetnet)
    df['origin_kind'] =[x[0] for x in df['source_id']]
    df['target_kind'] =[x[0] for x in df['target_id']]
    df = df[(df['origin_kind']==metaEdge[0]) & (df['target_kind']==metaEdge[1])]
    
    df['origin_id'] =[x[1] for x in df['source_id']]
    df['target_id'] =[x[1] for x in df['target_id']]
    df['source'] = [x['source'] if 'source' in x.keys() else '' for x in df['data']]
    df['sources'] = [x['sources'] if 'sources' in x.keys() else '' for x in df['data']]
    df['source'] = df['source'].combine_first(df['sources'])
    df['license'] = [x['license'] if 'license' in x.keys() else '' for x in df['data']]
    df['url'] = [x['url'] if 'url' in x.keys() else '' for x in df['data']]
    if edgeTypes=='binds':
        df['bind_actions'] = [x['actions'] if 'actions' in x.keys() else '' for x in df['data']]
        df['binding_affinity'] = [x['affinity_nM'] if 'affinity_nM' in x.keys() else None for x in df['data']]
    if edgeTypes=='regulates':
        df['sub_types'] = [x['sub_types'] if 'sub_types' in x.keys() else '' for x in df['data']]
        df['method'] = [x['method'] if 'method' in x.keys() else None for x in df['data']]
    if edgeTypes=='resembles' and sourceTypes=='C':
        df['similarity'] = [x['similarity'] if 'similarity' in x.keys() else '' for x in df['data']]
    df = df.drop(columns=['data','sources','source_id'])
    df.to_csv(r'hetiocsv\{}_{}c{}_edges.csv'.format(edgeTypes,sourceTypes,targetTypes), index=False)
    