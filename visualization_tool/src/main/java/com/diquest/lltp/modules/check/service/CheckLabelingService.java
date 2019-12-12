package com.diquest.lltp.modules.check.service;

public interface CheckLabelingService {

	/**
	 * 객체 jstree html 가져오기
	 * 
	 * @param groupName
	 * @return
	 */
	public String elementJstreeHtml(String groupName, String[] selectIds) throws Exception;

}
