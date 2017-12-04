package com.diquest.lltp.modules.brat.dao;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;


@Repository("BratDao")
public class BratDao extends CommonDAO{

	public List<AnnotationVo> getAnnotationList(DocumentVo vo) {
		return (List<AnnotationVo>)selectList("checkLabeling.getAnnotationList" , vo);
	}

	public void insertAnnotation(AnnotationVo vo) {
		insert("checkLabeling.insertAnnotation" , vo);
	}

}
