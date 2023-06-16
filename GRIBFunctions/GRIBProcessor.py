import os
import cfgrib

#Function to convert GRIB input to XArray
def xarray_conversion(grib_file):
    
    #Process GRIB file using cfgrib
    return cfgrib.open_datasets(grib_file)[0]

# Function to convert XArray input to CSV file
def csv_conversion(meteo_arr):

    # Rename the variable within the dataset
    meteo_arr = meteo_arr.rename({'gh': 'gh'})

    # Convert to DataFrame
    met_frame = meteo_arr.to_dataframe()

    # Reset index to convert multi-index to columns
    met_frame.reset_index(inplace=True)

    # Create output folder and set output path
    output_folder = './output/'
    output_filename = "csv_out.csv"
    output_path = os.path.join(output_folder, output_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Save and return CSV
    met_frame.to_csv(output_path, index=False)
    return open(output_path)

if __name__ == "__main__":
    import GRIBTester as tg
    grib_file = tg.get_grib()

    #Test XArray Conversion
    xarray_test = xarray_conversion(grib_file)
    print(xarray_test)

    #Test CSV Conversion
    csv_conversion(xarray_test)