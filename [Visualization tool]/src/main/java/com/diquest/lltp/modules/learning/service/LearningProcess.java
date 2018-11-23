package com.diquest.lltp.modules.learning.service;

import java.lang.Thread.State;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;

import com.diquest.labelproj.api.TrainSetSaver;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.ProcessQueue;
import com.diquest.lltp.modules.data.service.DocumentService;

public class LearningProcess implements Runnable {

	@Autowired
	public DocumentService documentService;

	Logger log = Logger.getLogger(this.getClass());
	private Thread thread;

	private ProcessQueue queue;

	public LearningProcess(ProcessQueue queue) {
		this.queue = queue;
	}

	public void startup() {
		this.thread = new Thread(this);
		this.thread.start();
	}
	
	public State getState() {
		return this.thread.getState();
	}

	public boolean autoLabeled() {
		try {
			DocumentVo vo = queue.getData();
			if (vo == null) {
				return false;
			}
			int recordId = vo.getRecordId();
			int recordSeq = Integer.parseInt(vo.getRecordSeq() == null ? "0" : vo.getRecordSeq());
			int docId = vo.getDocId();
			
			if(docId == -1) {
				return false;
			}
			
			try {
				log.info("학습데이터 생성 시작");
				log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq);
				TrainSetSaver saver = new TrainSetSaver(recordId, recordSeq);
				saver.save();
				log.info("학습데이터 생성 정상 종료");
				log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq);
			} catch (Exception e) {
				try {
					DocumentVo updateVo = new DocumentVo();
					updateVo.setRecordId(recordId);
					updateVo.setRabelStat("실패");
					documentService.updateLearnStat(updateVo);
					log.error("학습데이터 생성 비정상 종료", e);
					log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq);
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			} finally {
				LearningService.LAERNING_THREAD.get(vo.getGroupName()).remove(docId);
			}
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

	@Override
	public void run() {
		while (true) {
			if (!autoLabeled()) {
				break;
			}
		}
	}

}
