# AutoLysis

## 📘 About the Project
AutoLysis is a powerful, automated data analysis tool designed to streamline data exploration and preprocessing. This tool leverages API-driven intelligence to identify feature relevance, handle null values, detect and remove outliers, and generate comprehensive visualizations and project documentation.

With a single command, AutoLysis analyzes a dataset, produces plots, and generates descriptive README files, all while following best practices for open-source documentation. This automation reduces manual intervention, enabling users to focus on insights instead of data preparation.

## 🚀 Key Features
- **Automatic Feature Relevance Analysis**: Uses statistical measures to retain only the most important features.
- **Null Value Handling**: Handles null values based on fixed heuristics for numerical and categorical columns.
- **Outlier Detection and Removal**: Identifies and removes outliers using IQR (Interquartile Range) methodology.
- **Visualization Generation**: Creates professional plots to visualize data insights.
- **Automated Documentation**: Generates detailed README files with included images of plots.

## 📂 Project Structure
```
├── autolysis.py            # Main script to run the project
├── LICENSE                 # MIT License for the project
├── README.md               # Main README for the repo
├── /analysis_1             # Contains PNG plots and descriptive README for analysis 1
├── /analysis_2             # Contains PNG plots and descriptive README for analysis 2
└── /analysis_3             # Contains PNG plots and descriptive README for analysis 3
```

## 🛠️ Installation & Setup

This project uses the **uv package manager**, which allows seamless script execution and dependency management.

### Prerequisites
- Python 3.8 or later installed
- Install **uv** package manager. To install `uv`, run:
  ```bash
  pip install uv
  ```

### Initialize the Project
1. **Navigate to your project directory**:
   ```bash
   cd /path/to/project/directory
   ```
2. **Initialize the project with uv**:
   ```bash
   uv init
   ```
   This creates a `uv.json` file, which tracks dependencies and project configuration.
3. **Add required packages**:
   ```bash
   uv add pandas matplotlib scikit-learn python-dotenv requests chardet base64
   ```
   This installs all dependencies and updates the `uv.json` file.

## 🚀 Usage Instructions

To run the **AutoLysis** script, use the following command:
```bash
uv run autolysis.py <path_to_your_dataset>
```
Replace `<path_to_your_dataset>` with the path to your CSV file. The script will process the dataset, visualize the results, and generate project documentation automatically.

### How it Works
1. **File Encoding Detection**: Detects the file encoding to avoid issues when loading the CSV file.
2. **Dataset Loading**: Loads the dataset into a Pandas DataFrame.
3. **Null Handling**: Identifies and handles missing values in the dataset.
4. **Feature Relevance Analysis**: Selects the most important features to improve analysis.
5. **Outlier Removal**: Identifies and removes outliers using IQR.
6. **Visualization**: Generates plots to visualize trends, relationships, and distributions in the data.
7. **README Generation**: Creates a professional README file with plots included.

## 📊 Outputs
The script generates the following outputs:
- **/analysis_1**, **/analysis_2**, **/analysis_3**: Each folder contains plots and README files that describe the visualizations and key findings.
- **README.md**: A comprehensive project documentation file.
- **PNG Files**: Plots are saved as images in the respective folders.

## ⚙️ Commands Reference

| **Command**                | **Description**                    |
|----------------------------|-------------------------------------|
| `uv init`                  | Initializes a uv project            |
| `uv add <package>`         | Installs the specified package      |
| `uv run autolysis.py`      | Runs the AutoLysis script           |
| `uv run autolysis.py <dataset>` | Processes the dataset and generates outputs |

## 🔥 Example Usage

1. **Run analysis on sample.csv**
   ```bash
   uv run autolysis.py sample.csv
   ```
2. **View generated plots and documentation**
   - Navigate to **/analysis_1**, **/analysis_2**, or **/analysis_3** to see the plots and README files.

## 📋 License
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

## 🤝 Contributions
Contributions are welcome! To contribute, follow these steps:
1. Fork the project.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## 📧 Contact
For questions or support, please create an issue in the repository or contact the project maintainers.

---
**With AutoLysis, data analysis is faster, cleaner, and more insightful. Let AutoLysis do the heavy lifting while you focus on the insights.**

