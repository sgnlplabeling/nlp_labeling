package com.diquest.lltp.modules.learning.service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.ProcessQueue;
import com.diquest.lltp.modules.data.service.DocumentService;

@Service("learningService")
public class LearningServiceImpl implements LearningService {

	@Autowired
	public DocumentService documentService;

	public void learningStart(DocumentVo vo) throws Exception {
		String[] docIds = vo.getDocIds();
		Set<Integer> docIdSet = null;

		if (LAERNING_THREAD.containsKey(vo.getGroupName())) {
			docIdSet = LAERNING_THREAD.get(vo.getGroupName());
		} else {
			docIdSet = new HashSet<Integer>();
			LAERNING_THREAD.put(vo.getGroupName(), docIdSet);
		}

		for (int i = 0; i < docIds.length; i++) {
			int docId = Integer.parseInt(docIds[i]);
			docIdSet.add(docId);
		}

		ProcessQueue queue = new ProcessQueue();
		LearningProduce produce = new LearningProduce(documentService, vo.getDocIds(), vo.getGroupName(),
				vo.getUserId(), queue);
		produce.startUp();
		LearningProcess learningProcess = new LearningProcess(queue);
		learningProcess.startup();
	}

	public List<Integer> isRunningLearingThread(DocumentVo vo) {
		List<Integer> completeDocId = new ArrayList<Integer>();
		String[] docIds = vo.getDocIds();

		Set<Integer> docIdSet = new HashSet<Integer>();
		if (LAERNING_THREAD.containsKey(vo.getGroupName())) {
			docIdSet = LAERNING_THREAD.get(vo.getGroupName());
		} else {
			docIdSet = new HashSet<Integer>();
			LAERNING_THREAD.put(vo.getGroupName(), docIdSet);
		}

		for (int i = 0; i < docIds.length; i++) {
			int docId = Integer.parseInt(docIds[i]);
			if (!docIdSet.contains(docId)) {
				completeDocId.add(docId);
			}
		}
		return completeDocId;
	}
}
