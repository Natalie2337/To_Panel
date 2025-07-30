from utils import Merge_to_one, map_to_eng
import os

files_path = os.path.join(os.getcwd(),"Data")

def main():
    panel_df = Merge_to_one(files_path)
    print(panel_df)
    panel_df.to_csv('panel_data.csv', encoding='utf-8', index=False)
    mapped_df = map_to_eng(panel_df)
    print(mapped_df)
    mapped_df.to_csv('mapped_data.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    main()