package com.diquest.lltp.modules.auto.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.labelproj.api.Labeler;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.service.DocumentService;

@Service("autoLabelingService")
public class AutoLabelingServiceImpl implements AutoLabelingService{
	
	@Autowired
	public DocumentService documentService;
	
	public void labelingStart(DocumentVo vo) throws Exception {
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
			int docId =  Integer.parseInt(docIds[i]);
			
			if (record == null) {
				doc.setRabelStat("자동");
				recordId = documentService.insertRecord(doc);
			} else { 
				recordId = record.getRecordId();
			}
			
			AutoLabelProcess autoLabelProcess = new AutoLabelProcess(recordId, recordSeq, docId);
			autoLabelProcess.startup();
		}
	}
}
