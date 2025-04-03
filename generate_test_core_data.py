import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_test_core_data(num_samples=1000, output_file='test_core_data.csv'):
    """
    Генерирует тестовые данные керна для проверки скрипта
    
    Параметры:
        num_samples (int): Количество образцов
        output_file (str): Имя выходного файла
    """
    np.random.seed(42)
    random.seed(42)
    
    # Генерация глубины
    depth = np.linspace(2500, 3500, num_samples)
    
    # Генерация пористости (нормальное распределение)
    porosity = np.random.normal(loc=0.15, scale=0.03, size=num_samples)
    porosity = np.clip(porosity, 0.01, 0.35)  # Ограничение значений
    
    # Генерация проницаемости (логарифмически нормальное распределение)
    permeability = np.random.lognormal(mean=-1, sigma=0.8, size=num_samples)
    permeability = np.clip(permeability, 0.001, 2000)  # мД
    
    # Генерация литологии
    lithologies = ['Sandstone', 'Shale', 'Limestone', 'Dolomite']
    lithology = random.choices(lithologies, 
                             weights=[0.6, 0.25, 0.1, 0.05], 
                             k=num_samples)
    
    # Создание DataFrame
    df = pd.DataFrame({
        'DEPTH': depth,
        'POROSITY': porosity,
        'PERMEABILITY': permeability,
        'LITHOLOGY': lithology,
        'GRAIN_DENSITY': np.random.normal(2.65, 0.05, num_samples),
        'RESISTIVITY': np.random.lognormal(2, 0.5, num_samples)
    })
    
    # Добавление пропущенных значений (10%)
    for col in ['POROSITY', 'PERMEABILITY', 'GRAIN_DENSITY']:
        df.loc[df.sample(frac=0.1).index, col] = np.nan
    
    # Сохранение
    file_ext = output_file.split('.')[-1].lower()
    
    if file_ext == 'csv':
        df.to_csv(output_file, index=False)
    elif file_ext in ('xlsx', 'xls'):
        df.to_excel(output_file, index=False)
    else:
        raise ValueError("Поддерживаются только CSV или Excel форматы")
    
    print(f"Тестовые данные сохранены в {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Генератор тестовых данных керна')
    parser.add_argument('--output', help='Имя выходного файла', default='test_core_data.csv')
    parser.add_argument('--samples', help='Количество образцов', type=int, default=1000)
    
    args = parser.parse_args()
    
    generate_test_core_data(num_samples=args.samples, output_file=args.output)