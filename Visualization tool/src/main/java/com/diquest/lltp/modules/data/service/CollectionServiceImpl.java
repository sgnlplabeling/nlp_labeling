package com.diquest.lltp.modules.data.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.lltp.common.utils.JsTree;
import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.modules.data.dao.CollectionDao;
import com.diquest.lltp.modules.work.service.HistoryService;

@Service("collectionService")
public class CollectionServiceImpl implements CollectionService{

	@Autowired public CollectionDao checkDao;

	@Autowired public HistoryService historyService;	
	
	public List<CollectionVo> getCollectionList() throws Exception {
		HashMap<Object, String> map = new HashMap<>();
		
		List<CollectionVo> list = checkDao.getCollectionList();
		List<CollectionVo> result = new ArrayList<>();
		String path;
		String [] colIds = {};
		
		for (CollectionVo vo : list) {
			map.put(vo.getColId(),vo.getName());
		}
		
		CollectionVo root = new CollectionVo();
		root.setColId(0);
		root.setPath("ROOT");
		result.add(root);
		
		for (CollectionVo vo : list) {
			path="ROOT/";
			
			if (!StringUtils.isEmpty(vo.getPath())) {
				colIds = (vo.getPath()).split(">");
				
				for (String colId : colIds) {
					path += map.get(Integer.parseInt(colId));
					path += "/";
				}
			}
			path += vo.getName();
			vo.setPath(path);
			result.add(vo);
		}
		return result;
	}
	
	public String domainJstreeHtml(Integer colId) throws Exception {
		List<CollectionVo> list = getCollectionList();
	
		List<String> selId = new ArrayList<String>();
		if (colId != null) {
			selId.add(String.valueOf(colId));
		}
		
        return new JsTree.Mapper("colId", "path").parseAsHtml(list, selId);
	}
	
	public void insertDomain(CollectionVo vo) throws Exception {
		if (vo.getParentId() != null) {
			CollectionVo parentVo = checkDao.getCollectionOne(vo.getParentId());
			String path = "";
			
			if (parentVo != null) {
				if (!StringUtils.isEmpty(parentVo.getPath())) {
					path += parentVo.getPath();
					path += ">";
				}
				path += parentVo.getColId();
			}
			vo.setPath(path);
		}
        historyService.addHistory(historyService.makeDomainHistory("추가",vo, null));
		checkDao.insertDomain(vo);
	}
	
	public void updateDomain(CollectionVo vo) throws Exception {
		CollectionVo preVo = getCollectionOne(vo.getColId());
		checkDao.updateDomain(vo);
        historyService.addHistory(historyService.makeDomainHistory("수정", vo, preVo.getName()));
	}

	public void deleteDomain(CollectionVo vo) throws Exception {
		vo = getCollectionOne(vo.getColId());
		checkDao.deleteDomain(vo);
        historyService.addHistory(historyService.makeDomainHistory("삭제", vo, null));
	}
	
	public CollectionVo getCollectionOne(int colId) throws Exception {
		return checkDao.getCollectionOne(colId);
	}
	
}
