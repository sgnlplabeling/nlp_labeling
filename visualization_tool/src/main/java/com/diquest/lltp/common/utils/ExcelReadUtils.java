package com.diquest.lltp.common.utils;

import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.beanutils.BeanUtils;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.usermodel.DateUtil;
import org.apache.poi.ss.usermodel.FormulaEvaluator;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 엑셀 읽기 유틸리티
 *
 * @author yongseoklee
 * @since 1.0.0
 */
//@Slf4j
public class ExcelReadUtils {

	static final Logger log = LoggerFactory.getLogger(ExcelReadUtils.class);
	
	private ExcelReadUtils() {

	}

	/**
	 * Workbook 읽기
	 *
	 * @param inputStream
	 * @return
	 */
	public static Workbook getWorkbook(InputStream inputStream) {
		try {
			return WorkbookFactory.create(inputStream);
		} catch (IOException | InvalidFormatException e) {
			throw new RuntimeException(e);
		}
	}

	/**
	 * Sheet 존재여부
	 *
	 * @param workbook
	 * @param sheetIndex
	 * @return
	 */
	public static boolean isSheetExisted(Workbook workbook, int sheetIndex) {
		if (workbook == null || sheetIndex < 0)
			return false;

		if ((workbook.getNumberOfSheets() - 1) < sheetIndex)
			return false;

		Sheet sheet = workbook.getSheetAt(sheetIndex);
		if (sheet.getPhysicalNumberOfRows() == 0)
			return false;

		return true;
	}

	/**
	 * 특정 인덱스 Sheet 조회
	 *
	 * @param inputStream
	 * @param sheetIndex
	 * @return
	 */
	public static <T> List<T> getSheetAt(InputStream inputStream, int sheetIndex, int startRowIdx, Class<T> clazz) {
		return getSheetAt(getWorkbook(inputStream), sheetIndex, startRowIdx, clazz);
	}

	/**
	 * 특정 인덱스 Sheet 조회
	 * 
	 * @param workbook
	 * @param sheetIndex
	 * @param startRowIdx
	 *            시작행번호
	 * @param clazz
	 * @return
	 */
	public static <T> List<T> getSheetAt(Workbook workbook, int sheetIndex, int startRowIdx, Class<T> clazz) {
		if (!isSheetExisted(workbook, sheetIndex))
			return null;

		List<T> sheetList = new ArrayList<>();
		Sheet sheet = workbook.getSheetAt(sheetIndex);
		FormulaEvaluator formulaEvaluator = workbook.getCreationHelper().createFormulaEvaluator();

		// 첫번째 행 키값
		List<String> keyNames = getColumnKeys(sheet);
		int keySize = keyNames.size();

		// Row 계산
		int numberOfRows = sheet.getPhysicalNumberOfRows();

		for (int rowIdx = startRowIdx; rowIdx < numberOfRows; rowIdx++) {
			try {
				Row row = sheet.getRow(rowIdx);
				T rowObj = clazz.isAssignableFrom(Map.class) ? clazz.cast(new LinkedHashMap<>()) : clazz.newInstance();
				boolean isEmptyRow = false;

				if (row != null) {
					// emptyCellNum: 빈 셀 개수
					// 값이 있는경우 차감하고, 행 전체가 빈 경우 결과에 추가하지 않는다
					int emptyCellNum = row.getLastCellNum();

					for (Iterator<Cell> iterator = row.cellIterator(); iterator.hasNext();) {
						Cell cell = iterator.next();
						int columnIndex = cell.getColumnIndex();
						if (keySize <= columnIndex)
							continue;

						String cellKey = keyNames.get(columnIndex);
						if ("".equals(cellKey))
							continue;

						Object cellValue = getCellValue(cell, formulaEvaluator);
						if (cellValue != null) {
							emptyCellNum--;
							BeanUtils.setProperty(rowObj, cellKey, cellValue);
						}
					}

					isEmptyRow = emptyCellNum == row.getLastCellNum();
				}

				if (!isEmptyRow)
					sheetList.add(rowObj);
			} catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
				throw new RuntimeException(e);
			}
		}

		return sheetList;
	}

	/**
	 * 첫번째 Sheet 조회
	 *
	 * @param inputStream
	 * @return
	 */
	public static <T> List<T> getFirstSheet(InputStream inputStream, int startRowIdx, Class<T> clazz) {
		return getSheetAt(getWorkbook(inputStream), 0, startRowIdx, clazz);
	}

	/**
	 * 첫번째 Sheet 조회
	 * 
	 * @param workbook
	 * @return
	 */
	public static <T> List<T> getFirstSheet(Workbook workbook, int startRowIdx, Class<T> clazz) {
		return getSheetAt(workbook, 0, startRowIdx, clazz);
	}

	/**
	 * 모든 Sheet 조회
	 *
	 * @param inputStream
	 * @return
	 */
	public static <T> List<List<T>> getAllSheets(InputStream inputStream, int startRowIdx, Class<T> clazz) {
		return getAllSheets(getWorkbook(inputStream), startRowIdx, clazz);
	}

	/**
	 * 모든 Sheet 조회
	 *
	 * @param workbook
	 * @return
	 */
	public static <T> List<List<T>> getAllSheets(Workbook workbook, int startRowIdx, Class<T> clazz) {
		if (workbook == null)
			return null;

		List<List<T>> result = new ArrayList<>();

		int numberOfSheets = workbook.getNumberOfSheets();
		for (int sheetIndex = 0; sheetIndex < numberOfSheets; sheetIndex++) {
			List<T> sheetAt = getSheetAt(workbook, sheetIndex, startRowIdx, clazz);
			result.add(sheetAt == null ? new ArrayList<T>() : sheetAt);
		}

		return (result.size() == 0) ? null : result;
	}

	/**
	 * 컬럼 키 조회
	 * 
	 * @param sheet
	 * @return
	 */
	public static List<String> getColumnKeys(Sheet sheet) {
		Row row = sheet.getRow(0);

		List<String> list = new ArrayList<>();

		for (int cellIdx = 0; cellIdx < row.getLastCellNum(); cellIdx++) {
			Cell cell = row.getCell(cellIdx);
			Object cellValue = getCellValue(cell, null);

			list.add(cellValue == null ? "" : String.valueOf(cellValue));
		}

		return list;
	}

	/**
	 * Cell 읽기
	 *
	 * @param cell
	 * @return
	 */
	public static Object getCellValue(Cell cell, FormulaEvaluator formulaEvaluator) {
		if (cell == null)
			return null;

		// Cell 수식 계산
		if (formulaEvaluator != null)
			formulaEvaluator.evaluateInCell(cell);
		// cell.ty
		CellType cellType = cell.getCellTypeEnum();

		switch (cellType) {
			case NUMERIC:
				if (DateUtil.isCellDateFormatted(cell)) {
					return cell.getDateCellValue();
				} else {
					return cell.getNumericCellValue();
				}
			case STRING:
				return clean(cell.getStringCellValue());
			case FORMULA:
				return clean(cell.getCellFormula());
			case BLANK:
				return null;
			case BOOLEAN:
				return cell.getBooleanCellValue();
			case ERROR:
				return cell.getErrorCellValue();
			default:
				return null;
		}
	}

	/**
	 * 문자열 정제 - 양끝 공백제거 (trim) - Hex A0 공백으로 치환
	 *
	 * @param s
	 *            입력문자열
	 * @return (String) 정제된 문자열
	 */
	public static String clean(String s) {
		if (s == null)
			return null;

		String clean = s;
		// 0xA0 : ASCII CODE 의 &nbsp; (Non-breaking space)
		clean = clean.replaceAll("[\\xA0]", " ");
		// trim
		clean = clean.trim();

		return clean.length() == 0 ? null : clean;
	}

}
