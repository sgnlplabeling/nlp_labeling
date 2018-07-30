package com.diquest.lltp.modules.learning.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.labelproj.api.TrainSetSaver;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.auto.service.AutoLabelProcess;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.work.service.HistoryService;

@Service("learningService")
public class LearningServiceImpl implements LearningService {
	
	@Autowired
	public DocumentService documentService;
		
	public void learningStart(DocumentVo vo) throws Exception {
		String[] docIds = vo.getDocIds();
		DocumentVo doc;
		DocumentVo record;
		
		for (int i=0; i<docIds.length; i++) {
			doc = new DocumentVo();
			record = new DocumentVo();
			
			doc.setDocId(Integer.parseInt(docIds[i]));
			doc.setGroupName(vo.getGroupName());
			doc.setUserId(vo.getUserId());
			
			record = documentService.getRecordOne(doc);
			int recordId;
			int recordSeq = 0;
			if (record == null) {
				recordId = documentService.insertRecord(doc);
			} else {
				recordId = record.getRecordId();
				recordSeq = Integer.parseInt(record.getRecordSeq());
			}
			
			LearningProcess learningProcess = new LearningProcess(recordId, recordSeq);
			learningProcess.startup();
//			TrainSetSaver saver = new TrainSetSaver(recordId, recordSeq);
		}
	}
}
