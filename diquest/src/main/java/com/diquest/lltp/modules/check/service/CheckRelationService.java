package com.diquest.lltp.modules.check.service;

import java.util.List;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.RelationVo;

public interface CheckRelationService {

	/**
	 * relation 리스트 가져오기
	 * 
	 * @param commonVo
	 * @return
	 */
	public List<RelationVo> getRelationList(CommonVo commonVo);
	
	/**
	 * relation jstree 가져오기
	 * 
	 * @param groupName
	 * @return
	 * @throws Exception
	 */
	public String relationJstreeHtml(String groupName) throws Exception;

	/** 
	 * start 포인트 키워드 가져오기
	 * 
	 * @param groupName
	 * @param relation
	 * @param searchTerm
	 * @return
	 */
	public List<AnnotationVo> getKeywordStartPoint(String groupName, String relation, String searchTerm);
	
	/**
	 * end 포인트 키워드 가져오기
	 * 
	 * @param groupName
	 * @param relation
	 * @param searchTerm
	 * @return
	 */
	public List<AnnotationVo> getKeywordEndPoint(String groupName, String relation, String searchTerm);
	
	/**
	 * labeling 된 문서 가져오기
	 * 
	 * @param vo
	 * @return
	 * @throws Exception
	 */
	public List<DocumentVo> getLabelingDocList(AnnotationVo vo) throws Exception;

	/**
	 * labeling 안된 문서 가져오기
	 * 
	 * @param list
	 * @return
	 * @throws Exception
	 */
	public List<DocumentVo> getUnlabelingList(List<DocumentVo> list) throws Exception;

}
