package com.diquest.lltp.modules.data.dao;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.modules.work.service.HistoryService;

@Repository("collectionDao")
public class CollectionDao extends CommonDAO {

	public List<CollectionVo> getCollectionList() throws Exception {
		return (List<CollectionVo>)selectList("collection.getCollectionList");
	}
	
	public CollectionVo getCollectionOne(int colId) throws Exception {
		return (CollectionVo)selectOne("collection.getCollectionOne",colId);
	}
	
	public void insertDomain(CollectionVo vo) throws Exception {
		insert("collection.insertDomain" , vo);
	}

	public void updateDomain(CollectionVo vo) throws Exception {
		update("collection.updateDomain" , vo);
	}

	public void deleteDomain(CollectionVo vo) throws Exception {
		delete("collection.deleteDomain" , vo);
	}
	
}
