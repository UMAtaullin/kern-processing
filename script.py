import pandas as pd
import numpy as np
import os
from datetime import datetime

def process_core_data(input_file, output_dir='processed_results'):
    """
    Обрабатывает данные керна из CSV/Excel файла.
    
    Параметры:
        input_file (str): Путь к входному файлу (CSV или Excel)
        output_dir (str): Директория для сохранения результатов
    """
    # Создаем директорию для результатов, если ее нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Определяем тип файла и загружаем данные
    file_ext = os.path.splitext(input_file)[1].lower()
    
    try:
        if file_ext == '.csv':
            df = pd.read_csv(input_file)
        elif file_ext in ('.xlsx', '.xls'):
            df = pd.read_excel(input_file)
        else:
            raise ValueError("Неподдерживаемый формат файла. Используйте CSV или Excel.")
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return
    
    # Проверяем наличие необходимых столбцов
    required_columns = ['DEPTH', 'POROSITY', 'PERMEABILITY']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        print(f"Предупреждение: В данных отсутствуют важные столбцы: {missing_cols}")
    
    # Базовая очистка данных
    print("\n=== Статистика данных до обработки ===")
    print(df.info())
    print(df.describe())
    
    # Обработка пропущенных значений
    df_clean = df.copy()
    
    # Для числовых колонок заполняем медианными значениями
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # Для категориальных колонок заполняем наиболее частым значением
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col in df_clean.columns:
            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    # Дополнительные расчеты
    if all(col in df_clean.columns for col in ['POROSITY', 'PERMEABILITY']):
        df_clean['FLOW_ZONES'] = pd.cut(df_clean['POROSITY'], bins=5, labels=['FZ1', 'FZ2', 'FZ3', 'FZ4', 'FZ5'])
        
        # Расчет коэффициента качества коллектора (RQI)
        df_clean['RQI'] = 0.0314 * np.sqrt(df_clean['PERMEABILITY'] / df_clean['POROSITY'])
    
    print("\n=== Статистика данных после обработки ===")
    print(df_clean.info())
    print(df_clean.describe())
    
    # Сохранение результатов
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"processed_core_data_{timestamp}.xlsx")
    
    with pd.ExcelWriter(output_file) as writer:
        df_clean.to_excel(writer, sheet_name='Processed Data', index=False)
        
        # Добавляем сводные таблицы
        if 'FLOW_ZONES' in df_clean.columns:
            summary_table = df_clean.groupby('FLOW_ZONES').agg({
                'POROSITY': ['mean', 'median', 'std'],
                'PERMEABILITY': ['mean', 'median', 'std'],
                'RQI': ['mean', 'median', 'std']
            })
            summary_table.to_excel(writer, sheet_name='Flow Zones Summary')
    
    print(f"\nОбработка завершена. Результаты сохранены в: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Обработка данных керна из CSV/Excel файлов')
    parser.add_argument('input_file', help='Путь к входному файлу (CSV или Excel)')
    parser.add_argument('--output_dir', help='Директория для сохранения результатов', default='processed_results')
    
    args = parser.parse_args()
    
    process_core_data(args.input_file, args.output_dir)