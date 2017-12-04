package com.diquest.lltp.modules.learning.service.thread;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.diquest.lltp.modules.learning.controller.DownloadController;
import com.diquest.lltp.modules.learning.service.DownloadService;

public class DownloadThread extends Thread {
	private String exportID;
	private DownloadService service;

	public DownloadThread(String exportID, DownloadService service) {
		this.exportID = exportID;
		this.service = service;
		this.service.setFileName(exportID);
	}

	@Override
	public void run() {
		Logger l = LoggerFactory.getLogger(getClass());
		boolean r = false;
		if (this.service != null) {
			try {
				l.info("start export thread : {}", getName());
				r = this.service.execute();
				l.info("end export thread : {}", getName());
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		if (this.exportID.length() > 0) {
			if (DownloadController.DOWNLOAD_INFO.containsKey(this.exportID)) {
				DownloadController.DOWNLOAD_INFO.remove(this.exportID);
			}
			DownloadController.DOWNLOAD_INFO.put(this.exportID, String.valueOf(r));
		} else {
			DownloadController.DOWNLOAD_INFO.put(this.exportID, String.valueOf(false));
		}
	}

}
