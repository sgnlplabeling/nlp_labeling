package com.diquest.lltp.modules.data.dao;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.work.service.HistoryService;


@Repository("documentDao")
public class DocumentDao extends CommonDAO {
	
	@Autowired public HistoryService historyService;	

	public DocumentVo insertDocument(DocumentVo vo) throws Exception {
		String content = vo.getContent();
		content = content.replaceAll("<[^>]*>", " ");
		vo.setContent(content);
		try {
			insert("document.insertDocument" , vo);
			vo.setResult(true);
		} catch(Exception e ){
			vo.setResult(false);
	    }
		return vo;
	}	
	
	public DocumentVo getDocOne(DocumentVo vo) throws Exception {
		return (DocumentVo)selectOne("document.getDocOne" , vo);
	}
	
	public List<DocumentVo> getDocList(DocumentVo vo) throws Exception {
		return selectList("document.getDocList" , vo);
	}
	
	public List<DocumentVo> getDocRecordList(DocumentVo vo) throws Exception {
		List<DocumentVo> list = selectList("document.getDocNum" , vo);
		
		List<DocumentVo> result = new ArrayList<DocumentVo>();
		if (list.size() > 0) {
			HashMap <String,Object> map = new HashMap<>();
			map.put("list", list);
			if (!StringUtils.isEmpty(vo.getGroupName())) {
				map.put("groupName", vo.getGroupName());
			}
			result = selectList("document.getDocRecordList" ,map);
		}
		
		return result;
	}
	
	public List<DocumentVo> getDocIdsRecordList(DocumentVo vo) throws Exception {
		List<DocumentVo> list = new ArrayList<DocumentVo>();
		
		String[] docIds = vo.getDocIds();
		for(int idx=0; idx < docIds.length; idx++) {
			DocumentVo documentVo = new DocumentVo();
			documentVo.setDocId(Integer.parseInt(docIds[idx]));
			list.add(documentVo);
		}
		
		List<DocumentVo> result = new ArrayList<DocumentVo>();
		if (list.size() > 0) {
			HashMap <String,Object> map = new HashMap<>();
			map.put("list", list);
			if (!StringUtils.isEmpty(vo.getGroupName())) {
				map.put("groupName", vo.getGroupName());
			}
			result = selectList("document.getDocRecordList" ,map);
		}
		
		return result;
	}

	public List<DocumentVo> getDocHistoryList(DocumentVo vo) {
		List<DocumentVo> result = selectList("document.getDocHistoryList" ,vo);
		return result;
	}
	
	public List<DocumentVo> getDocSubjectList(DocumentVo vo) throws Exception {
		return selectList("document.getDocSubjectList" , vo);
	}
	
	public int getDocListCount(DocumentVo vo) throws Exception {
		return (int)selectOne("document.getDocListCount" , vo);
	}

	public DocumentVo getRecordOne(DocumentVo vo) throws Exception {
		return (DocumentVo)selectOne("document.getRecordOne" , vo);
	}	
	
	public List<DocumentVo> getRecordList(DocumentVo vo) throws Exception {
		return selectList("document.getRecordList" , vo);
	}

	public int getRecordListCount(DocumentVo vo) throws Exception {
		return (int)selectOne("document.getRecordListCount" , vo);
	}

	public int insertRecord(DocumentVo vo) throws Exception {
		insert("document.insertRecord" , vo);
		return vo.getRecordId();
	}
	
	public void deleteRecord(Integer recordId) throws Exception {
		HashMap <String,Object> map = new HashMap<>();
		map.put("recordId", recordId);

		delete("document.deleteAnnotation", map);
		delete("document.deleteRecord", map);
	}

	public void updateRecordConf(DocumentVo vo) throws Exception {
		update("document.updateRecordConf", vo);
		}

	public void updateRecord(DocumentVo vo) throws Exception {
		update("document.updateRecord", vo);
	}

	public void updateRabelStat(DocumentVo vo) throws Exception {
		update("document.updateRabelStat", vo);
	}
	
	public void updateLearningStat(DocumentVo vo) throws Exception {
		update("document.updateLearningStat", vo);
	}

	public void deleteDocument(Integer docId) throws Exception {
		DocumentVo vo = new DocumentVo();
		vo.setDocId(docId);
		
		HashMap <String,Object> map = new HashMap<>();
		map.put("docId", docId);
		delete("document.deleteDocument", map);
		
	}

	public int getDocRecordListCount(DocumentVo vo) {
		return (int)selectOne("document.getDocRecordListCount" , vo);
	}
	
	public DocumentVo getLearnData(int recordId) throws Exception {
		return (DocumentVo)selectOne("document.getLearningData",recordId);
	}

	public int getDocHistoryListCount(DocumentVo vo) {
		return (int)selectOne("document.getDocHistoryListCount" , vo);
	}


}
