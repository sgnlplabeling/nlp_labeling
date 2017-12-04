package com.diquest.lltp.modules.auto.service;

import org.apache.log4j.Logger;

import com.diquest.labelproj.api.Labeler;

public class AutoLabelProcess implements Runnable {
	
	Logger log = Logger.getLogger(this.getClass());
	private int recordId;
	private int recordSeq;
	private int docId;
	private Thread thread;
	
	public AutoLabelProcess(int recordId, int recordSeq, int docId) {
		this.recordId = recordId;
		this.recordSeq = recordSeq;
		this.docId = docId;
	}
		
	public void startup() {
		this.thread = new Thread(this);
		this.thread.start();
	}

	@Override
	public void run() {
		try {
			log.info("자동레이블링 시작");
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq+", DOC_ID: "+docId);
			Labeler.getInstance(recordId,recordSeq, docId).label();
			log.info("자동레이블링 정상 종료");
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq+", DOC_ID: "+docId);
		} catch (Exception e) {
			log.error("자동레이블링 비정상 종료",e);
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq+", DOC_ID: "+docId);
		}
	}

}
