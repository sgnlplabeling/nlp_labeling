package com.diquest.lltp.modules.data.service;

import java.util.List;

import org.json.simple.JSONObject;

import com.diquest.lltp.common.utils.file.FileInfo;
import com.diquest.lltp.domain.DocumentVo;

public interface DocumentService {

	public JSONObject insertDocument(DocumentVo vo) throws Exception;

	public String txtParser(FileInfo file) throws Exception;
	
	public List<DocumentVo> getDocList(DocumentVo vo) throws Exception;

	public List<DocumentVo> getDocSubjectList(DocumentVo vo) throws Exception;
	
	public List<DocumentVo> getDocHistoryList(DocumentVo vo) throws Exception;
	
	public int getDocListCount(DocumentVo vo) throws Exception;

	public DocumentVo getDocOne(DocumentVo vo) throws Exception;
	
	public DocumentVo getRecordOne(DocumentVo vo) throws Exception;	
	
	public List<DocumentVo> getRecordList(DocumentVo vo) throws Exception;

	public int getRecordListCount(DocumentVo vo) throws Exception;

	public void deleteDocument(Integer[] docId) throws Exception;
	
	public void deleteRecord(Integer[] recordId) throws Exception;
	
	public void updateRecordConf(DocumentVo vo) throws Exception;

	public int insertRecord(DocumentVo vo) throws Exception;

	public void updateRecord(DocumentVo vo) throws Exception;

	public List<DocumentVo> getDocRecordList(DocumentVo vo) throws Exception;

	public int getDocRecordListCount(DocumentVo vo) throws Exception;
	
	public List<DocumentVo> getDocIdsRecordList(DocumentVo vo) throws Exception;

	public void fileDelete(String string) throws Exception;
	
	public DocumentVo getLearnData(DocumentVo vo) throws Exception;

	public int getDocHistoryListCount(DocumentVo vo);

}
