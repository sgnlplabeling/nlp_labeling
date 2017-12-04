package com.diquest.lltp.modules.learning.service;

import org.apache.log4j.Logger;

import com.diquest.labelproj.api.TrainSetSaver;

public class LearningProcess implements Runnable {
	
	Logger log = Logger.getLogger(this.getClass());
	private int recordId;
	private int recordSeq;
	private Thread thread;
	
	public LearningProcess(int recordId, int recordSeq) {
		this.recordId = recordId;
		this.recordSeq = recordSeq;
	}
		
	public void startup() {
		this.thread = new Thread(this);
		this.thread.start();
	}

	@Override
	public void run() {
		try {
			log.info("학습데이터 생성 시작");
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq);
			TrainSetSaver saver = new TrainSetSaver(recordId, recordSeq);
			saver.save();
			log.info("학습데이터 생성 정상 종료");
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq);
		} catch (Exception e) {
			log.error("학습데이터 생성 비정상 종료",e);
			log.info("RECORD_ID: "+this.recordId+", RECORD_SEQ: "+recordSeq);
		}
	}

}
