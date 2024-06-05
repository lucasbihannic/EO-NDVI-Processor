from satsearch import Search
import requests
import os
import json

def get_bbox(geometry):
    x_coordinates, y_coordinates = zip(*geometry[0])
    return [min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)]

def calculate_intersection_area(bbox1, bbox2):
    x1 = max(bbox1[0], bbox2[0])
    y1 = max(bbox1[1], bbox2[1])
    x2 = min(bbox1[2], bbox2[2])
    y2 = min(bbox1[3], bbox2[3])
    width = max(0, x2 - x1)
    height = max(0, y2 - y1)
    return width * height

def fetch_data(bbox, date_range):
    # Define search parameters
    dataRepositoryURL = 'https://earth-search.aws.element84.com/v0/'
    scene_cloud_tolerance = 5

    search = Search(bbox=bbox, datetime=date_range,
                    query={"eo:cloud_cover": {"lt": scene_cloud_tolerance}},
                    collections=["sentinel-s2-l2a-cogs"],
                    url=dataRepositoryURL)

    # Get the items
    items = search.items()
    print(f"Found {len(items)} items")

    # Find the item with the largest intersection area with the original bounding box
    best_item = None
    best_intersection_area = 0
    lowest_cloud_cover = 100  # Initialize to a high value

    for item in items:
        intersection_area = calculate_intersection_area(bbox, item.bbox)
        cloud_cover = item.properties['eo:cloud_cover']
        if intersection_area > best_intersection_area or (intersection_area == best_intersection_area and cloud_cover < lowest_cloud_cover):
            best_intersection_area = intersection_area
            lowest_cloud_cover = cloud_cover
            best_item = item

    # Fetch metadata and download the best matching item
    if best_item:
        print("Best matching item ID:", best_item.id)
        print("Datetime:", best_item.properties['datetime'])
        print("Cloud cover:", best_item.properties['eo:cloud_cover'])
        print("Bounding box correspondance:", best_intersection_area)

        # Prepare directory for saving data
        output_dir = os.path.join('EO_data', best_item.id)
        os.makedirs(output_dir, exist_ok=True)

        # Save metadata
        metadata_path = os.path.join(output_dir, f"{best_item.id}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(best_item.properties, f, indent=4)
        print(f"Metadata saved to {metadata_path}")

        # Download assets (e.g., B04, B08, and thumbnail)
        asset_keys = ['B04', 'B08', 'thumbnail']
        for key in asset_keys:
            if key in best_item.assets:
                href = best_item.assets[key]['href']
                response = requests.get(href)
                asset_path = os.path.join(output_dir, f"{best_item.id}_{key}.tif" if key != 'thumbnail' else f"{best_item.id}_thumbnail.jpg")
                with open(asset_path, 'wb') as f:
                    f.write(response.content)
                print(f"{key} asset saved as {asset_path}")

        return output_dir
    else:
        print("No suitable item found.")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6:
        print("Usage: python fetch_data.py x1 y1 x2 y2 date_range")
    else:
        x1, y1, x2, y2 = map(float, sys.argv[1:5])
        date_range = sys.argv[5]
        bbox = [x1, y1, x2, y2]
        output_directory = fetch_data(bbox, date_range)
        if output_directory:
            print(f"Data fetched and saved in directory: {output_directory}")
