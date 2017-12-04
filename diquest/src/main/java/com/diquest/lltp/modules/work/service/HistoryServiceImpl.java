package com.diquest.lltp.modules.work.service;

import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;
import com.diquest.lltp.modules.data.service.CollectionService;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.work.dao.HistoryDao;

@Service("historyService")
public class HistoryServiceImpl implements HistoryService {
	
	@Autowired public HistoryDao historyDao;
	
	@Autowired public CollectionService collectionService;
	
	@Autowired public DocumentService documentService;
	
	
	public void addHistory(HistoryVo vo) throws Exception {
		historyDao.addHistory(vo);
	}
	 
	public void addHistoryRecord(HistoryVo vo) throws Exception {
		historyDao.addHistoryRecord(vo);
	}
	
	public HistoryVo makeDomainHistory(String action, CollectionVo vo, String etc) throws Exception {
		HistoryVo history = new HistoryVo();
		String description = "";
		
		switch (action) {
			case "수정":
				description = "도메인 "+etc+getEulrl(etc)+" "+vo.getName()+"으로 수정 하였습니다.";
				break;
			case "삭제":
				description = "도메인 "+vo.getName()+getEulrl(vo.getName())+" 삭제 하였습니다.";
				break;
			case "추가":
				description = "도메인 "+vo.getName()+getEulrl(vo.getName())+" 추가 하였습니다.";
				break;
		}
		history.setType("도메인");
		history.setJob(action);
		history.setNote(description);
		
		return history;
	}
	
	public HistoryVo makeDocHistory(String action, DocumentVo vo, String etc) throws Exception {
		HistoryVo history = new HistoryVo();
		String description = "";
		
		if(StringUtils.isEmpty(vo.getSubject())) {
			vo = documentService.getDocOne(vo);
		}
		
		String subject = vo.getSubject();
		
		switch (action) {
			case "삭제":
				description = "문서 ["+subject+"]"+getEulrl(subject)+" 삭제 하였습니다.";
				break;
			case "추가":
				description = "문서 ["+subject+"]"+getEulrl(subject)+" 추가 하였습니다.";
				break;
			case "추가실패":
				description = "문서 ["+subject+"] 추가에 실패 하였습니다.";
				break;
		}
		
		history.setType("문서");
		history.setJob(action);
		history.setNote(description);
		
		return history;
	}
	
	public HistoryVo makeLabelingHistory(String action, int recordId, String etc) throws Exception {
		HistoryVo history = new HistoryVo();
		DocumentVo vo = new DocumentVo();
		vo.setRecordId(recordId);
		vo = documentService.getRecordOne(vo);
		
		String subject = vo.getSubject();
		String groupName = vo.getGroupName();
		switch (groupName) {
			case "namedentity":
				groupName = "개체명";
				break;
			case "syntactic":
				groupName = "구문분석";
				break;
			case "causation":
				groupName = "인과관계";
				break;
		}
		
		String description = "";
		switch (action) {
			case "삭제":
				description = "문서 "+subject+"("+groupName+")의 레이블링정보를 삭제 하였습니다.";
				break;
			case "작업확인":
				description = "문서 "+subject+"("+groupName+")의 작업확인을 완료 하였습니다.";
				break;
			case "작업확인취소":
				description = "문서 "+subject+"("+groupName+")의 작업확인을 취소 하였습니다.";
				break;
			case "자동레이블링 시작":
				description = "문서 "+subject+"("+groupName+")의 자동레이블을 시작 하였습니다.";
				break;
			case "자동레이블링 종료":
				description = "문서 "+subject+"("+groupName+")의 자동레이블을 종료 하였습니다.";
				break;
			case "수정":
				description = "문서 "+subject+"("+groupName+")의 레이블링 정보를 수정 하였습니다.";
				break;
			case "언레이블링":
				description = "문서 "+subject+"("+groupName+")의 "+etc+"을 언레이블링 하였습니다.";
				break;
			case "복원":
				description = "문서 "+subject+"("+groupName+")의 레이블링 정보를 ["+etc+"]으로 복원 하였습니다.";
				break;
		}
		
		history.setType("레이블링");
		history.setRecordId(vo.getRecordId());
		history.setJob(action);
		history.setNote(description);
		
		return history;
	}	
	
	public List<HistoryVo> getHistoryList(CommonVo vo) throws Exception {
		List<CollectionVo> domainList = collectionService.getCollectionList();
		List<HistoryVo> list = historyDao.getHistoryList(vo);
		
		HashMap<Object, String> map = new HashMap<>();
		String[] colIds;
		int index = 0;
		for (CollectionVo domain : domainList) {
			map.put(domain.getColId(),domain.getName());
		}
		
		for (HistoryVo history : list) {
			if (!StringUtils.isEmpty(history.getDomain())) {
				String path = "";
				if (!StringUtils.isEmpty(history.getDomainPath())) {
					colIds = (history.getDomainPath()).split(">");
					
					for (String colId : colIds) {
						path += map.get(Integer.parseInt(colId));
						path += "/";
					}
				}
				
				path += history.getDomain();
				history.setDomainPath(path);
				list.set(index, history);
			}
			
			index++;
		}
		return list;
	}
	
	public int getHistoryListCount(CommonVo vo) throws Exception {
		return historyDao.getHistoryListCount(vo);
	}
	
	public List<HistoryVo> getRecordHistoryList(DocumentVo vo) throws Exception {
		List<HistoryVo> list = historyDao.getRecordHistoryList(vo);
		
		if (list.size()>0) {
			list.remove(0);
		}
		return list;
	}
	
	public List<AnnotationVo> getCompareLoc(DocumentVo vo) throws Exception {
		return historyDao.getCompareLoc(vo);
	}
	
	public static boolean eulrlega(String word) {
		char last = word.charAt(word.length()-1);
		
		if(last < 0xAC00)
			return true;
		
		last -= 0xAC00;
		
		char jong = (char) ((last % 28) + 0x11a7);		
		
		return (jong != 4519);
	}
	
	public static String getEulrl(String word) {
		return eulrlega(word)? "을" : "를";
	}
	
	public static String getEga(String word) {
		return eulrlega(word)? "이" : "가";
	}
	
	public static String getEunnn(String word) {
		return eulrlega(word)? "은" : "는";		
	}
}
