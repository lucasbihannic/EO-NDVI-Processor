# Earth Observation Data Processing

This repository contains scripts for fetching and analyzing Earth Observation (EO) data. The scripts utilize the Sentinel-2 dataset and calculate the NDVI (Normalized Difference Vegetation Index) for a specified region and period.

## Prerequisites

Ensure you have the required Python packages installed. You can install the dependencies using the following command:

```sh
pip install -r requirements.txt
```

## 1. Fetching Data

The `fetch_data.py` script fetches EO data for a specified bounding box and date range. The data is saved in a directory named after the best matching item ID.

### Usage

```sh
python3 fetch_data.py <x1> <y1> <x2> <y2> <date_range>
```

### Example

```sh
python3 fetch_data.py 44.737088 40.138597 45.675484 40.658207 2022-01-01/2023-12-31
```

This command fetches data for the bounding box defined by the coordinates `(44.737088, 40.138597)` and `(45.675484, 40.658207)` which correspond to Sevan Lake for the date range from January 1, 2022, to December 31, 2023.

## 2. Analyzing Data

The `analyze_data.py` script analyzes the fetched data by calculating the NDVI for the specified region.

### Usage

```sh
python3 analyze_data.py <output_directory>
```

### Example

```sh
python3 analyze_data.py EO_data/<fetched_item>
```

Replace `<fetched_item>` with the directory name returned by the `fetch_data.py` script.

## Directory Structure

The fetched data will be saved in the `EO_data` directory with the following structure:

```
EO_data/
└── <fetched_item>/
    ├── <fetched_item>_B04.tif
    ├── <fetched_item>_B08.tif
    ├── <fetched_item>_thumbnail.jpg
    ├── <fetched_item>_metadata.json
    └── <fetched_item>_NDVI.tif
```

- `<fetched_item>_B04.tif`: Red band image.
- `<fetched_item>_B08.tif`: Near-infrared band image.
- `<fetched_item>_thumbnail.jpg`: Thumbnail image of the scene.
- `<fetched_item>_metadata.json`: Metadata of the scene.
- `<fetched_item>_NDVI.tif`: Calculated NDVI image.
- `<fetched_item>_NDVI.plot.png`: Calculated NDVI image in png format.

## Output

The scripts will output relevant information during execution, including the number of items found, metadata of the best matching item, and confirmation of saved files.

## Notes

- Ensure you have an active internet connection to fetch the data.
- The scripts are designed to handle Sentinel-2 data, and modifications may be necessary for other datasets.