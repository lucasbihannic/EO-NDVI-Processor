import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def calculate_ndvi(nir, red):
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = np.where((nir + red) == 0., 0, (nir - red) / (nir + red))
    return ndvi

def analyze_data(data_dir):
    # File paths for B04 (red) and B08 (NIR) bands
    b4_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_B04.tif")
    b8_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_B08.tif")
    
    # Read the bands
    with rasterio.open(b4_path) as b4, rasterio.open(b8_path) as b8:
        red = b4.read(1).astype(float)
        nir = b8.read(1).astype(float)
        
        # Calculate NDVI
        ndvi = calculate_ndvi(nir, red)
        
        # Save NDVI image
        ndvi_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_NDVI.tif")
        ndvi_meta = b4.meta
        ndvi_meta.update(dtype=rasterio.float32, count=1)
        
        with rasterio.open(ndvi_path, 'w', **ndvi_meta) as ndvi_dst:
            ndvi_dst.write(ndvi.astype(rasterio.float32), 1)
        
        print(f"NDVI image saved to {ndvi_path}")
        
        # Plot NDVI
        plt.imshow(ndvi, cmap='RdYlGn')
        plt.colorbar()
        plt.title('NDVI')
        
        # Save the plot
        plot_path = os.path.join(data_dir, f"{os.path.basename(data_dir)}_NDVI_plot.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"NDVI plot saved to {plot_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python analyze_data.py <data_directory>")
        sys.exit(1)
    
    data_directory = sys.argv[1]
    analyze_data(data_directory)
