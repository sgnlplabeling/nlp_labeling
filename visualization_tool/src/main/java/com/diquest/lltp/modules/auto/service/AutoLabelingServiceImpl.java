package com.diquest.lltp.modules.auto.service;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;
import com.diquest.lltp.domain.ProcessQueue;
import com.diquest.lltp.modules.auto.dao.AutoLabelingDao;
import com.diquest.lltp.modules.data.service.DocumentService;

@Service("autoLabelingService")
public class AutoLabelingServiceImpl implements AutoLabelingService {

	@Autowired
	public DocumentService documentService;

	@Autowired
	public AutoLabelingDao autoLabelingDao;

	public void labelingStart(DocumentVo vo) throws Exception {

		String[] docIds = vo.getDocIds();
		Set<Integer> docIdSet = null;

		if (AutoLabelingService.AUTO_LABELD_THREADS.containsKey(vo.getGroupName())) {
			docIdSet = AutoLabelingService.AUTO_LABELD_THREADS.get(vo.getGroupName());
		} else {
			docIdSet = new HashSet<Integer>();
			AutoLabelingService.AUTO_LABELD_THREADS.put(vo.getGroupName(), docIdSet);
		}

		for (int i = 0; i < docIds.length; i++) {
			int docId = Integer.parseInt(docIds[i]);
			docIdSet.add(docId);
		}

		ProcessQueue queue = new ProcessQueue();
		AutoLabelProduce produce = new AutoLabelProduce(documentService, vo.getDocIds(), vo.getGroupName(),
				vo.getUserId(), queue);
		produce.startUp();
		AutoLabelProcess autoLabelProcess = new AutoLabelProcess(queue);
		autoLabelProcess.startup();
	}

	public List<Integer> isRunningAutoLabeled(DocumentVo vo) {
		List<Integer> completeDocId = new ArrayList<Integer>();
		String[] docIds = vo.getDocIds();

		Set<Integer> docIdSet = new HashSet<Integer>();
		if (AutoLabelingService.AUTO_LABELD_THREADS.containsKey(vo.getGroupName())) {
			docIdSet = AutoLabelingService.AUTO_LABELD_THREADS.get(vo.getGroupName());
		} else {
			docIdSet = new HashSet<Integer>();
			AutoLabelingService.AUTO_LABELD_THREADS.put(vo.getGroupName(), docIdSet);
		}
		System.out.println("DOC ID INFO : " + docIdSet);
		for (int i = 0; i < docIds.length; i++) {
			int docId = Integer.parseInt(docIds[i]);
			if (!docIdSet.contains(docId)) {
				completeDocId.add(docId);
			}
		}
		return completeDocId;
	}

	public List<DocumentVo> getAutoLabelingList(DocumentVo vo) throws Exception {
		List<DocumentVo> list = documentService.getDocRecordList(vo);
		List<HistoryVo> jobList = new ArrayList<>();
		int index = 0;

		for (DocumentVo doc : list) {
			jobList = new ArrayList<>();
			jobList = autoLabelingDao.getAutoLabelingStat(doc);

			if (!jobList.isEmpty()) {
				doc.setStartDate("");
				doc.setEndDate("");

				for (HistoryVo job : jobList) {
					String type = job.getJob();
					if (StringUtils.equals(type, "시작")) {
						doc.setRegId(job.getRegId());
						doc.setStartDate(new SimpleDateFormat("yyyy-MM-dd").format(job.getRegDate()));
					}
					if (StringUtils.equals(type, "종료")) {
						doc.setEndDate(new SimpleDateFormat("yyyy-MM-dd").format(job.getRegDate()));
					}
				}
			}

			list.set(index, doc);
			index++;
		}
		return list;
	}

	public int getAutoLabelingListCount(DocumentVo vo) throws Exception {
		return documentService.getDocRecordListCount(vo);
	}

	@Override
	public List<Integer> chkRunningAutoLabeled(DocumentVo vo) {
		List<Integer> completeDocId = new ArrayList<Integer>();
		Set<Integer> docIdSet = new HashSet<Integer>();
		if (AutoLabelingService.AUTO_LABELD_THREADS.containsKey(vo.getGroupName())) {
			docIdSet = AutoLabelingService.AUTO_LABELD_THREADS.get(vo.getGroupName());
		} else {
			docIdSet = new HashSet<Integer>();
			AutoLabelingService.AUTO_LABELD_THREADS.put(vo.getGroupName(), docIdSet);
		}
		completeDocId.addAll(docIdSet);
		return completeDocId;
	}
}
