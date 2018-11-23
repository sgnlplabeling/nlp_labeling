package com.diquest.lltp.modules.auto.service;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.ProcessQueue;
import com.diquest.lltp.modules.data.service.DocumentService;

public class AutoLabelProduce implements Runnable {

	private DocumentVo vo;
	private ProcessQueue queue;

	private Thread thread;
	private DocumentService service;
	private String[] docIds;
	private String groupName;
	private String userId;

	public AutoLabelProduce(DocumentService service, String[] docId, String groupName, String userId, ProcessQueue queue) {
		this.service = service;
		this.docIds = docId;
		this.groupName = groupName;
		this.userId = userId;
		this.queue = queue;
	}

	public void startUp() {
		this.thread = new Thread(this);
		this.thread.start();
	}

	@Override
	public void run() {
		try {
			for (int i = 0; i < docIds.length; i++) {
				DocumentVo doc = new DocumentVo();
				DocumentVo record = new DocumentVo();
				doc.setDocId(Integer.parseInt(docIds[i]));
				doc.setGroupName(groupName);
				doc.setUserId(userId);

				try {
					record = service.getRecordOne(doc);
				} catch (Exception e) {
					e.printStackTrace();
					break;
				}
				if (record == null) {
					doc.setRabelStat("자동");
					try {
						service.insertRecord(doc);
					} catch (Exception e) {
						e.printStackTrace();
						break;
					}
					try {
						record = service.getRecordOne(doc);
					} catch (Exception e) {
						e.printStackTrace();
						break;
					}
				}
				queue.putData(record);
			}
			DocumentVo emptyVo = new DocumentVo();
			emptyVo.setDocId(-1);
			queue.putData(emptyVo);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
