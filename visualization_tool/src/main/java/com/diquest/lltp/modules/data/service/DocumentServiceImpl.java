package com.diquest.lltp.modules.data.service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.json.simple.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.diquest.lltp.common.utils.FileEncodingCheck;
import com.diquest.lltp.common.utils.file.FileInfo;
import com.diquest.lltp.common.utils.file.FileUpload;
import com.diquest.lltp.domain.CollectionVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.dao.CollectionDao;
import com.diquest.lltp.modules.data.dao.DocumentDao;
import com.diquest.lltp.modules.work.service.HistoryService;

@Service("documentService")
public class DocumentServiceImpl implements DocumentService {

	@Value("#{app['file.uploadPath']}")
	private String uploadfile;

	@Autowired
	public DocumentDao documentDao;

	@Autowired
	public CollectionDao checkDao;

	@Autowired
	public HistoryService historyService;

	@SuppressWarnings("unchecked")
	public JSONObject insertDocument(DocumentVo vo) throws Exception {
		final List<FileInfo> fileList = FileUpload.fileUpload(vo.getFile(), uploadfile);
		int colId = vo.getColId();

		List<Integer> successDocIds = new ArrayList<>();
		List<String> failDocSubject = new ArrayList<>();
		List<String> overlapDocSubject = new ArrayList<>();

		for (FileInfo file : fileList) {
			if (file.getGubun().equals("txt")) {
				vo = new DocumentVo();
				vo.setContent(txtParser(file));
				vo.setSubject(file.getOrgn_file_nm());
				vo.setColId(colId);

				if (documentDao.getDocOne(vo) != null) {
					overlapDocSubject.add(vo.getSubject());
				} else {
					vo = documentDao.insertDocument(vo);

					if (vo.isResult()) {
						successDocIds.add(vo.getDocId());
						historyService.addHistory(historyService.makeDocHistory("추가", vo, null));
					} else {
						failDocSubject.add(vo.getSubject());
						historyService.addHistory(historyService.makeDocHistory("추가실패", vo, null));
					}
				}

			}
		}

		fileDelete(fileList.get(0).getSave_path());

		JSONObject json = new JSONObject();
		json.put("successDocIds", successDocIds);
		json.put("failDocSubject", failDocSubject);
		json.put("overlapDocSubject", overlapDocSubject);

		return json;
	}

	public void fileDelete(String path) {
		File file = new File(path);
		if (!file.exists())
			return;

		File[] tempFile = file.listFiles();

		if (tempFile.length > 0 && tempFile != null) {
			for (int i = 0; i < tempFile.length; i++) {
				tempFile[i].delete();
			}
		}

		file.delete();
	}

	public String txtParser(FileInfo file) throws Exception {
		String txt = null;
		String filePath = file.getSave_path() + file.getSave_file_nm();

		StringBuffer buffer = new StringBuffer();
		String encoding = FileEncodingCheck.getTextFileEncoding(filePath);
		BufferedReader in = null;
		try {
			in = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), encoding));
			
			int readbyte;
			while ((readbyte = in.read()) != -1) {
				buffer.append((char) readbyte);
			}
			txt = buffer.toString();
			buffer.setLength(0);
			return txt;
		} catch (Exception e) {
			throw e;
		} finally {
			if (in != null) {
				in.close();
			}
		}

	}
	
	public DocumentVo getDocOne(DocumentVo vo) throws Exception {
		return documentDao.getDocOne(vo);
	}

	public List<DocumentVo> getDocList(DocumentVo vo) throws Exception {
		return documentDao.getDocList(vo);
	}

	public List<DocumentVo> getDocSubjectList(DocumentVo vo) throws Exception {
		return documentDao.getDocSubjectList(vo);
	}

	public List<DocumentVo> getDocHistoryList(DocumentVo vo) throws Exception {
		return documentDao.getDocHistoryList(vo);
	}

	public int getDocHistoryListCount(DocumentVo vo) {
		return documentDao.getDocHistoryListCount(vo);
	}

	public List<DocumentVo> getDocRecordList(DocumentVo vo) throws Exception {
		return documentDao.getDocRecordList(vo);
	}

	public int getDocListCount(DocumentVo vo) throws Exception {
		return documentDao.getDocListCount(vo);
	}

	public List<DocumentVo> getDocIdsRecordList(DocumentVo vo) throws Exception {
		return documentDao.getDocIdsRecordList(vo);
	}

	public int getDocRecordListCount(DocumentVo vo) throws Exception {
		return documentDao.getDocRecordListCount(vo);
	}

	public DocumentVo getRecordOne(DocumentVo vo) throws Exception {
		vo = documentDao.getRecordOne(vo);

		if (vo != null) {
			List<CollectionVo> list = checkDao.getCollectionList();
			HashMap<Object, String> map = new HashMap<>();

			String path = "";
			String[] colIds = {};

			for (CollectionVo domain : list) {
				map.put(domain.getColId(), domain.getName());
			}

			if (!StringUtils.isEmpty(vo.getDomainPath())) {
				String domainPath = vo.getDomainPath();

				colIds = domainPath.split(">");

				for (String colId : colIds) {
					path += map.get(Integer.parseInt(colId));
					path += "/";
				}
			}
			path += vo.getDomain();
			vo.setDomainPath(path);
		}

		return vo;
	}

	public List<DocumentVo> getRecordList(DocumentVo vo) throws Exception {
		return documentDao.getRecordList(vo);
	}

	public int getRecordListCount(DocumentVo vo) throws Exception {
		return documentDao.getRecordListCount(vo);
	}

	public void deleteDocument(Integer[] docId) throws Exception {
		DocumentVo doc;
		for (Integer id : docId) {
			doc = new DocumentVo();
			doc.setDocId(id);
			List<DocumentVo> list = getRecordList(doc);

			if (list.size() > 0) {
				for (DocumentVo vo : list) {
					historyService.addHistoryRecord(historyService.makeLabelingHistory("삭제", vo.getRecordId(), null));
					documentDao.deleteRecord(vo.getRecordId());
				}
			}
			historyService.addHistory(historyService.makeDocHistory("삭제", doc, null));
			documentDao.deleteDocument(id);
		}
	}

	public void deleteRecord(Integer[] recordId) throws Exception {
		for (Integer id : recordId) {
			historyService.addHistoryRecord(historyService.makeLabelingHistory("삭제", id, null));
			documentDao.deleteRecord(id);
		}
	}

	public void updateRecordConf(DocumentVo vo) throws Exception {
		if ((vo.getTypeOpt()).equals("save")) {
			vo.setConfId(vo.getUserId());
			historyService.addHistoryRecord(historyService.makeLabelingHistory("작업확인", vo.getRecordId(), null));
		} else {
			historyService.addHistoryRecord(historyService.makeLabelingHistory("작업확인취소", vo.getRecordId(), null));
		}
		documentDao.updateRecordConf(vo);
	}

	public int insertRecord(DocumentVo vo) throws Exception {
		int recordId = documentDao.insertRecord(vo);
		return recordId;
	}

	public void updateRecord(DocumentVo vo) throws Exception {
		documentDao.updateRecord(vo);
	}

	public void updateRabelStat(DocumentVo vo) throws Exception {
		documentDao.updateRabelStat(vo);
	}

	public void updateLearnStat(DocumentVo vo) throws Exception {
		documentDao.updateLearningStat(vo);
	}

	public DocumentVo getLearnData(DocumentVo vo) throws Exception {
		int recordId = vo.getRecordId();
		return documentDao.getLearnData(recordId);
	}
}
