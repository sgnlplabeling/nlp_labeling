package com.diquest.lltp.modules.work.service;

import java.util.List;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;

public interface HistoryService {
	
	public void addHistory(HistoryVo vo) throws Exception;
	
	public void addHistoryRecord(HistoryVo vo) throws Exception;	

	public HistoryVo makeDomainHistory(String action, CollectionVo vo, String etc) throws Exception;
	
	public HistoryVo makeDocHistory(String action, DocumentVo vo, String etc) throws Exception;
		
	public HistoryVo makeLabelingHistory(String action, int recordId, String etc) throws Exception;
	
	public List<HistoryVo> getHistoryList(CommonVo vo) throws Exception;

	public int getHistoryListCount(CommonVo vo) throws Exception;

	public List<HistoryVo> getRecordHistoryList(DocumentVo vo) throws Exception;

	public List<AnnotationVo> getCompareLoc(DocumentVo vo) throws Exception;

}
