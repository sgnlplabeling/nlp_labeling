package com.diquest.lltp.modules.data.dao;

import java.util.HashMap;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;

@Repository("entityDao")
public class EntityDao extends CommonDAO {

	public List<EntityVo> getOverlapCheck(HashMap<String, Object> map) {
		return selectList("entity.getOverlapCheck",map);
	}

	public Integer insertEntity(EntityVo vo) {
		return (Integer)insert("entity.insertEntity",vo);
	}
	
	public EntityVo getEntityOne(EntityVo vo) {
		return (EntityVo)selectOne("entity.getEntityOne",vo);
	}

	public void updateEntity(EntityVo vo) {
		update("entity.updateEntity",vo);
	}

	public void deleteEntity(EntityVo vo) {
		delete("entity.deleteEntity",vo);
	}

	public List<DocumentVo> getEntityDocList(EntityVo vo) {
		return selectList("entity.getEntityDocList",vo);
	}

	public int getEntityDocListCount(EntityVo vo) {
		List<EntityVo> list = selectList("entity.getEntityDocListCount",vo);
		return list.size();
	}

	public List<AnnotationVo> getAnnotationList(DocumentVo doc) {
		return selectList("entity.getAnnotationList",doc);
	}

	public List<RelationVo> getRelationList(EntityVo vo) {
		return selectList("entity.getRelationList",vo);
	}
	
	public RelationVo getRelationOne(RelationVo vo) {
		return (RelationVo)selectOne("entity.getRelationOne",vo);
	}
	
	public List<EntityVo> getEntityList(EntityVo vo) {
		return selectList("entity.getEntityList",vo);
	}

	public String updateRelation(RelationVo vo) {
		String relId;
		RelationVo rel = getRelationOne(vo);
		if (rel != null) {
			vo.setRelId(rel.getRelId());
			update("entity.updateRelation",vo);
			relId = rel.getRelId();
		} else {
			insert("entity.insertRelation",vo);
			relId = vo.getRelId();
			System.out.println(relId);
		}
		return relId;
	}

	public void deleteRelation(RelationVo vo) {
		delete("entity.deleteRelation",vo);
	}

	public Integer insertRelation(RelationVo vo) {
		return (Integer)insert("entity.insertRelation",vo);
	}
	
	public List<EntityVo> getEntityByEntId(EntityVo vo) {
		return selectList("entity.getEntityByEntId",vo);
	}
}
