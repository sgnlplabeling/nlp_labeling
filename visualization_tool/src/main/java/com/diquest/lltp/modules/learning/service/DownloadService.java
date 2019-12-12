package com.diquest.lltp.modules.learning.service;

import java.io.File;
import java.io.FileFilter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.LinkedList;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.learning.controller.DownloadController;
import com.diquest.lltp.modules.learning.service.download.DownloadResult;
import com.diquest.lltp.modules.learning.service.download.DownloadResultText;

public class DownloadService {

	Logger logger = LoggerFactory.getLogger(getClass());

	private String fileName;
	private String resultPath;
	private DocumentVo vo;

	List<String> subjects = new LinkedList<String>();

	DownloadResult export;

	private DocumentService documentService;
	private String downloadFilePath;
	private String zipFilePath;

	public DownloadService(DocumentService service, String resultPath, String exportID, DocumentVo vo) {
		this.documentService = service;
		this.resultPath = resultPath;
		this.vo = vo;
		// zipFilePath = this.resultPath + File.separator + exportID + ".zip";
		zipFilePath = this.resultPath + "/" + exportID + ".zip";
	}

	/**
	 * 현재 날짜로 부터 입력된 날짜 수 이전의 파일들만 필터링한다.
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	private static class CustomFileFilter implements FileFilter {
		Calendar c = new GregorianCalendar();

		/**
		 * @param date
		 *            이전 날짜 수.
		 */
		protected CustomFileFilter(int date) {
			c.add(Calendar.DATE, date);
			System.out.println("File filter Date : " + c.getTime());
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.io.FileFilter#accept(java.io.File)
		 */
		@Override
		public boolean accept(File pathname) {
			return c.getTime().after(new Date(pathname.lastModified()));
		}

	}

	/*
	 * 특정 경로내의 파일들이 48시간이 경과된 파일이면 지운다.
	 */
	private void clearFiles(String dirPath) {
		// 파일을 삭제하는 코드
		File path = new File(dirPath);
		File[] files = path.listFiles(new CustomFileFilter(-2));
		for (File f : files) {
			try {
				logger.info("delete file : " + f.getCanonicalPath());
			} catch (IOException e) {
				e.printStackTrace();
			}
			f.delete();
		}
	}

	private void createFileInit(String subject) {
		File dir = new File(resultPath);
		if (!dir.exists()) {
			dir.mkdirs();
		} else {
			clearFiles(resultPath);
		}

		try {
			// downloadFilePath = this.resultPath + File.separator + subject + ".txt";
			downloadFilePath = this.resultPath + "/" + subject + ".txt";
			subjects.add(subject);
			export = new DownloadResultText(downloadFilePath, vo);
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
	}

	public String getDownloadFilePath() {
		return zipFilePath;
	}

	public boolean execute() {
		String[] docIds = vo.getDocIds();
		DocumentVo doc;
		DocumentVo record;

		for (int i = 0; i < docIds.length; i++) {
			try {
				doc = new DocumentVo();
				record = new DocumentVo();

				doc.setDocId(Integer.parseInt(docIds[i]));
				doc.setGroupName(vo.getGroupName());
				// doc.setUserId(vo.getUserId());

				record = documentService.getRecordOne(doc);

				doc = new DocumentVo();
				if (record != null) {
					createFileInit(record.getSubject());
					doc.setRecordId(record.getRecordId());

					DocumentVo resultDoc = documentService.getLearnData(doc);
					makeFile(resultDoc);
				}

				DownloadController.DOWNLOAD_INFO.put(this.fileName,
						subjects.get(i) + "(" + String.valueOf(i + 1) + "/" + String.valueOf(docIds.length) + ")");
			} catch (Exception e) {
				e.printStackTrace();
				logger.error(e.getMessage(), e);
				return false;
			} finally {
				if (export != null) {
					export.close();
				}
			}
		}

		if (subjects.size() > 0) {
			ZipOutputStream zout = null;

			try {
				zout = new ZipOutputStream(new FileOutputStream(zipFilePath));
				byte[] buf = new byte[1024];
				for (int idx = 0; idx < subjects.size(); idx++) {
					// FileInputStream in = new FileInputStream(this.resultPath + File.separator +
					// subjects.get(idx) + ".txt");//압축대상 파일
					FileInputStream in = null;
					zout.putNextEntry(new ZipEntry(subjects.get(idx) + ".txt"));
					try {
						in = new FileInputStream(this.resultPath + "/" + subjects.get(idx) + ".txt");// 압축대상 파일
						int len;
						while ((len = in.read(buf)) > 0) {
							zout.write(buf, 0, len);
						}
					} catch (Exception e) {
						logger.error(e.getMessage(), e);
					} finally {
						if (in != null) {
							in.close();
						}
						zout.closeEntry();
					}
				}
			} catch (Exception e) {
				e.printStackTrace();
			} finally {
				if (null != zout) {
					try {
						zout.close();
					} catch (Exception e) {
					}
					zout = null;
				}
			}
		}

		return true;
	}

	/**
	 * 서버에 파일 경로를 생성한다.
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	void makeFile(DocumentVo resultDoc) throws Exception {
		if (resultDoc == null) {
			throw new Exception("download시 오류가 발생했습니다. resultDoc객체가 null입니다.");
		}

		export.setData(resultDoc.getLearnData());
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}
}
