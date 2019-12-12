package com.diquest.lltp.modules.auto.service;

import java.lang.Thread.State;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;

import com.diquest.labelproj.api.Labeler;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.ProcessQueue;
import com.diquest.lltp.modules.data.service.DocumentService;

public class AutoLabelProcess implements Runnable {

	@Autowired
	public DocumentService documentService;

	Logger log = Logger.getLogger(this.getClass());
	private Thread thread;

	private ProcessQueue queue;

	public AutoLabelProcess(ProcessQueue queue) {
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
			int recordSeq = 0;
			int docId = vo.getDocId();

			if(docId == -1) {
				return false;
			}
			
			try {
				log.info("자동레이블링 시작");
				log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq + ", DOC_ID: " + docId);
				Labeler.getInstance(recordId, recordSeq, docId, "sogang").label();
				log.info("자동레이블링 정상 종료");
				log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq + ", DOC_ID: " + docId);
			} catch (Exception e) {
				try {
					DocumentVo updateTarget = new DocumentVo();
					updateTarget.setRecordId(recordId);
					updateTarget.setRabelStat("실패");
					documentService.updateRabelStat(updateTarget);
					log.error("자동레이블링 비정상 종료", e);
					log.info("RECORD_ID: " + recordId + ", RECORD_SEQ: " + recordSeq + ", DOC_ID: " + docId);
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			} finally {
				AutoLabelingService.AUTO_LABELD_THREADS.get(vo.getGroupName()).remove(docId);
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
