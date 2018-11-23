package com.diquest.lltp.modules.data.service;

import java.util.List;

import com.diquest.lltp.domain.CollectionVo;

public interface CollectionService {
	
	/**
	 * 도메인 리스트 가져오기
	 * 
	 * @return
	 * @throws Exception
	 */
	public List<CollectionVo> getCollectionList() throws Exception;
	
	/**
	 * 도메인 가져오기
	 * 
	 * @param colId
	 * @return
	 * @throws Exception
	 */
	public CollectionVo getCollectionOne(int colId) throws Exception;
	
	/**
	 * 도메인 jstree 가져오기
	 * 
	 * @param colId
	 * @return
	 * @throws Exception
	 */
	public String domainJstreeHtml(Integer colId) throws Exception;
	
	/**
	 * 도메인추가
	 * 
	 * @param vo
	 * @throws Exception
	 */
	public void insertDomain(CollectionVo vo) throws Exception;

	/**
	 * 도메인 수정
	 * 
	 * @param vo
	 * @throws Exception
	 */
	public void updateDomain(CollectionVo vo) throws Exception;

	/**
	 * 도메인 삭제
	 * 
	 * @param vo
	 * @throws Exception
	 */
	public void deleteDomain(CollectionVo vo) throws Exception;
	
}
