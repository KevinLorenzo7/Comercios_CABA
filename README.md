# Interactive Map of Businesses and Bank Branches in CABA

This repository contains a Python script to visualize businesses and Banco Ciudad branches in Buenos Aires City (CABA). It uses `geopandas`, `folium`, and `scipy.spatial` to process and display the data on an interactive map.

## 📌 Features

- Filters active businesses in CABA that are `UNICOMERCIAL` or `MULTICOMERCIAL`.
- Finds the nearest Banco Ciudad branch for each business.
- Generates an interactive map using `folium` showing businesses and branches.
- Saves processed data in an Excel file.

## 📂 Project Structure

```
📁 Project
├── main.py               # Main script
├── Usos_del_Suelo_CABA.zip # Shapefile with business data (Private)
├── banks.xlsx           # Banco Ciudad branch data
├── Map.html    # Generated interactive map
├── businesses_and_bank_branches.xlsx # Processed data in Excel format (Private)
└── README.md             # This file
```

## 🔧 Requirements

Before running the script, ensure you have the following dependencies installed:

```bash
pip install pandas geopandas folium shapely scipy openpyxl
```

## 🚀 Usage

1. Place the files `Usos_del_Suelo_CABA.zip` and `banks.xlsx` in the same directory as `main.py`.
2. Run the script:
   ```bash
   python main.py
   ```
3. The script will generate `Map.html` (interactive map) and `businesses_and_bank_branches.xlsx` (processed data).
4. Open `Map.html` in a browser to view the map.

## 📌 Notes

- The script uses `cKDTree` from `scipy.spatial` to efficiently find the nearest branch.
- It is recommended to validate file paths before running the script.

---
📍 *Developed for visualizing businesses and bank branches in CABA.*

