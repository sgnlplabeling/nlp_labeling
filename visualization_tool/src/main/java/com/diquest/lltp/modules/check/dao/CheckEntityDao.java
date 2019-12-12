package com.diquest.lltp.modules.check.dao;

import java.util.HashMap;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;


@Repository("CheckEntityDao")
public class CheckEntityDao extends CommonDAO{

	public List<EntityVo> getEntityList(CommonVo vo) {
		return selectList("checkEntity.getEntityList" , vo);
	}

	public List<AnnotationVo> getKeywordList(HashMap<String,Object> map) {
		return selectList("checkEntity.getKeywordList" , map);
	}

	public List<DocumentVo> getLabelingDocList(AnnotationVo vo) {
		return selectList("checkEntity.getLabelingDocList" , vo);
	}

	public List<DocumentVo> getUnlabelingList(List<DocumentVo> list) {
		HashMap <String,Object> map = new HashMap<>();
		map.put("list", list);
		return selectList("checkEntity.getUnlabelingList" , map);
	}

}
