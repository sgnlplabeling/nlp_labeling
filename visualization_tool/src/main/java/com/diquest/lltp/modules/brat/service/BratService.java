package com.diquest.lltp.modules.brat.service;

import java.util.HashMap;
import java.util.List;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;

public interface BratService {

	/**
	 * brat docdata 가져오기
	 * 
	 * @param documentVo
	 * @return
	 * @throws Exception
	 */
	public Object getDocData(DocumentVo documentVo) throws Exception;
	
	/**
	 * brat colldata 가져오기
	 * 
	 * @param documentVo
	 * @return
	 * @throws Exception
	 */
	public Object getCollData(DocumentVo documentVo) throws Exception;

	/**
	 * Brat 편집화면이동(readOnly)
	 * 
	 * @param documentVo
	 * @return
	 * @throws Exception
	 */
	public HashMap<String,Object> bratReadOnly(DocumentVo documentVo) throws Exception;
	
	/**
	 * Brat 편집화면이동(readOnly,Edit)
	 * 
	 * @param documentVo
	 * @return
	 * @throws Exception
	 */
	public HashMap<String,Object> bratEdit(DocumentVo documentVo) throws Exception;
	
	/**
	 * Brat 파일 생성
	 * 
	 * @param doc
	 * @param fileName
	 * @throws Exception
	 */
	public void createFile(DocumentVo doc, String fileName) throws Exception;

	/**
	 * Brat 저장
	 * 
	 * @param documentVo
	 * @return
	 * @throws Exception
	 */
	public DocumentVo bratSave(DocumentVo documentVo) throws Exception;

	/**
	 * Brat 관련파일 삭제
	 * 
	 * @param path
	 * @throws Exception
	 */
	public void deleteFile(String path) throws Exception;

	/**
	 * annotation 리스트 가져오기
	 * 
	 * @param documentVo
	 * @return
	 */
	public List<AnnotationVo> getAnnotationList(DocumentVo documentVo) throws Exception;

	/**
	 * annotation 삽입
	 * 
	 * @param ann
	 */
	public void insertAnnotation(AnnotationVo ann);


}
