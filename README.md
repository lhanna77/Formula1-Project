# Formula 1 Project: Incremental Load with Python Notebooks

## Overview
This project aims to perform incremental data loading from a Formula 1 API into a Lakehouse using Python Notebooks. The process involves fetching data from the API, transforming it, and loading it into the Lakehouse, ensuring data integrity and efficiency.

## Requirements
- Python 3.10
- Jupyter Notebooks

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```

## Usage
File run order...

- plan.sh (only for GCP table loads)
- apply.sh (only for GCP table loads)
- get_latest_data_from_api.py
- 1.ingest_circuits_file.ipynb
- 2.ingest_constructors_file.ipynb
- 3.ingest_drivers_file.ipynb
- 7.ingest_races_file_api_multi.ipynb
- 8.ingest_race_circuits_file_api_multi.ipynb
- 9.ingest_results_file_api_mulit.ipynb
- bq_silver_gold_loads_api.py (only for GCP table loads)

To refresh only this years results...

- Run bash - source run_new_results_load_in_order.sh

## Project Structure
- `requirements.txt`: List of required Python packages.
- `files/latest_data_from_api/`: Directory to store fetched latest Formula 1 data direct from API.

## How It Works
1. **get_latest_data_from_api**: main() refreshes Results data from API, main(latest = False), refreshes all files.

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
Special thanks to the Formula 1 API for providing access to the data used in this project.