package com.diquest.lltp.modules.brat.dao;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;


@Repository("BratDao")
public class BratDao extends CommonDAO{

	public List<AnnotationVo> getAnnotationList(DocumentVo vo) {
		return selectList("checkLabeling.getAnnotationList" , vo);
	}

	public void insertAnnotation(AnnotationVo vo) {
		insert("checkLabeling.insertAnnotation" , vo);
	}

}
