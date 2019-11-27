package com.diquest.lltp.modules.work.dao;

import java.util.HashMap;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;

@Repository("historyDao")
public class HistoryDao extends CommonDAO {
	
	public void addHistory(HistoryVo vo) {
		insert("history.addHistory" , vo);
	}
	
	public void addHistoryRecord(HistoryVo vo) {
		insert("history.addHistoryRecord" , vo);
	}
	
	public List<HistoryVo> getHistoryList(CommonVo vo) {
		return selectList("history.getHistoryList" , vo);
	}

	public int getHistoryListCount(CommonVo vo) {
		return (int)selectOne("history.getHistoryListCount" , vo);
	}

	public List<HistoryVo> getRecordHistoryList(DocumentVo vo) {
		return selectList("history.getRecordHistoryList" , vo);
	}

	public List<AnnotationVo> getCompareLoc(HashMap<String,Object> map) {
		return selectList("history.getCompareLoc" , map);
	}

}
