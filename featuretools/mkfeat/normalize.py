from pandas import DataFrame
import autonormalize as an

def normalize(df: DataFrame, key_colname):
    es = None
    entities = set()
    relationships = set()

    if len(df) > 1000:
        for _ in range(5):  
            df = df.sample(n=1000)
            es = an.auto_entityset(df, index=key_colname, accuracy=0.98)
            entities.update(es.entities[1:])
            relationships.update(es.relationships)
    else:
        es = an.auto_entityset(df, index=key_colname, accuracy=0.98)
        entities.update(es.entities[1:])
        relationships.update(es.relationships)

    norminfos = []
    # 첫번째 이외의 entity들에 대해서. 첫번째 entity가 main임을 가정
    for et in entities:
        norminfo = []
        for var in et.variables:
            norminfo.append(var.name)
        norminfos.append(norminfo)
    for norminfo in norminfos:
        parent_ids = _get_parent_entity_ids(relationships, norminfo[0])
        for parent_id in parent_ids:
            vars = es[parent_id].variables
            for var in vars[1:]:
                norminfo.append(var.name)
    return norminfos

def _get_parent_entity_ids(rels, child_id):
    parent_ids = []
    for rel in rels:
        if child_id == rel.child_entity.id:
            parent_ids.append(rel.parent_entity.id)
            parent_ids += _get_parent_entity_ids(rels, rel.parent_entity.id)
    return parent_ids