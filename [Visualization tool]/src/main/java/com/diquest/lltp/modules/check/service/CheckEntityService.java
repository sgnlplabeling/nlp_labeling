package com.diquest.lltp.modules.check.service;

import java.util.List;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;

public interface CheckEntityService {

	/**
	 * entity list 가져오기
	 * 
	 * @param commonVo
	 * @return
	 */
	public List<EntityVo> getEntityList(CommonVo commonVo);
	
	/**
	 * entity jstree 가져오기
	 * 
	 * @param groupName
	 * @return
	 * @throws Exception
	 */
	public String entityJstreeHtml(String groupName) throws Exception;

	/**
	 * keyword list 가져오기
	 * 
	 * @param groupName
	 * @param entity
	 * @param searchTerm
	 * @return
	 * @throws Exception
	 */
	public List<AnnotationVo> getKeywordList(String groupName, String entity, String searchTerm) throws Exception;

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

	/**
	 * labeling->unlabeling 처리 하기
	 * 
	 * @param docId
	 * @param groupName
	 * @param keyword
	 * @throws Exception
	 */
	public void unlabelingDoc(String[] docId, String groupName, String[] keyword) throws Exception;
}
