package com.diquest.lltp.domain;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ProcessQueue {
	BlockingQueue<DocumentVo> queue = new LinkedBlockingQueue<DocumentVo>(3);

	public void putData(DocumentVo vo) {
		try {
			queue.put(vo);
		} catch (InterruptedException e) {
		}
	}

	public DocumentVo getData() {
		try {
			return queue.take();
		} catch (InterruptedException e) {
		}
		return null;
	}

}
