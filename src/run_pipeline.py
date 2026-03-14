import os

os.system("python src/load_to_sqlite.py")
os.system("python src/run_sql_script.py")
os.system("python src/run_validation.py")
os.system("python src/export_features.py")

print("Pipeline completed successfully")