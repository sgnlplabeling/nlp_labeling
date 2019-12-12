package com.diquest.lltp.modules.auto.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.diquest.lltp.domain.DocumentVo;

public interface AutoLabelingService {

	public static final Map<String, Set<Integer>> AUTO_LABELD_THREADS = new HashMap<String, Set<Integer>>();
	/**
	 * 자동 레이블링 시작
	 * 
	 * @param vo
	 * @throws Exception
	 */
	public void labelingStart(DocumentVo vo) throws Exception;

	public List<DocumentVo> getAutoLabelingList(DocumentVo vo) throws Exception;

	public int getAutoLabelingListCount(DocumentVo vo) throws Exception;

	/**
	 * 사용자가 자동레이블링 선택했을때 동작되는 모션 처리
	 * 
	 * @param vo
	 * @return
	 */
	public List<Integer> isRunningAutoLabeled(DocumentVo vo);
	
	/**
	 * 
	 * 사용자가 페이지 진입시 실행되는 레이블링 현황
	 * 
	 * @param vo
	 * @return
	 */
	public List<Integer> chkRunningAutoLabeled(DocumentVo vo);
	
}
