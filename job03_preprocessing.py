import os
import pandas as pd

# 병합할 CSV 파일이 있는 폴더 경로 설정
folder_path = 'C:/workspace/news_category_classfication/crawling_data'  # Windows의 경우, '\' 대신 '/' 사용하세요.

# 폴더에 있는 파일 목록 확인
try:
    files_in_folder = os.listdir(folder_path)
    print(f"폴더 내 파일: {files_in_folder}")
except FileNotFoundError:
    print(f"폴더 경로가 올바르지 않습니다: {folder_path}")

# CSV 파일만 필터링
csv_files = [file for file in files_in_folder if file.endswith('.csv')]
print(f"CSV 파일 목록: {csv_files}")

# CSV 파일 병합
if csv_files:
    dataframes = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 결과 저장
    output_path = os.path.join(folder_path, "naver_headline_news20241219.csv")
    merged_df.to_csv(output_path, index=False)
    print(f"병합된 파일이 저장되었습니다: {output_path}")
else:
    print("CSV 파일이 폴더에 없습니다.")



