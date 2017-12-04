package com.diquest.lltp.modules.data.service;

import java.util.List;

import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.domain.DocumentVo;

public interface CollectionService {
	
	public List<CollectionVo> getCollectionList() throws Exception;
	
	public CollectionVo getCollectionOne(int colId) throws Exception;
	
	public String domainJstreeHtml(Integer colId) throws Exception;
	
	public void insertDomain(CollectionVo vo) throws Exception;

	public void updateDomain(CollectionVo vo) throws Exception;

	public void deleteDomain(CollectionVo vo) throws Exception;
	
}
