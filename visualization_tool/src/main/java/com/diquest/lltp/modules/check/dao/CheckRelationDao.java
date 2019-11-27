package com.diquest.lltp.modules.check.dao;

import java.util.HashMap;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.RelationVo;


@Repository("CheckRelationDao")
public class CheckRelationDao extends CommonDAO{

	public List<RelationVo> getRelationList(CommonVo vo) {
		return selectList("checkRelation.getRelationList" , vo);
	}

	public List<AnnotationVo> getKeywordStartPoint(HashMap<String,Object> map) {
		return selectList("checkRelation.getKeywordStartPoint" , map);
	}
	
	public List<AnnotationVo> getKeywordEndPoint(HashMap<String,Object> map) {
		return selectList("checkRelation.getKeywordEndPoint" , map);
	}

	public List<DocumentVo> getLabelingDocList(AnnotationVo vo) {
		return selectList("checkRelation.getLabelingDocList" , vo);
	}

	public List<DocumentVo> getUnlabelingList(List<DocumentVo> list) {
		HashMap <String,Object> map = new HashMap<>();
		map.put("list", list);
		return selectList("checkRelation.getUnlabelingList" , map);
	}

	public List<AnnotationVo> getKeywordList(RelationVo vo) {
		return selectList("checkRelation.getKeywordList" , vo);
	}

	public List<RelationVo> getRelationLoc(AnnotationVo vo) {
		return selectList("checkRelation.getRelationLoc" , vo);
	}

}
