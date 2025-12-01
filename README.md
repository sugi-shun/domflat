# DOM-FLAT: DOM Flattening and Reconstruction Kit

## Overview

This repository provides a specialized toolset, **DOM-FLAT**, for converting an HTML Document Object Model (DOM) structure into a flattened, data-centric CSV format and rebuilding the original HTML from that CSV. This is highly useful for generating **labeled data for machine learning models** that require structured context and content of web pages.

The process uses **Depth-First Search (DFS)** for consistent ordering and employs the **`{idXXX}`** format to explicitly link parent and child elements within the flat CSV structure.

## Requirements

The scripts require the following Python libraries:

```bash
pip install -r requirements.txt
````

**requirements.txt:**

```
pandas
beautifulsoup4
```

## Scripts

### 1\. `html2csv.py` (The Flattener)

Converts an HTML file into the structured CSV format.

| Column | Data Type | Description |
| :--- | :--- | :--- |
| **id** | int | Unique element ID (assigned via DFS starting from 0). Used for child referencing. |
| **xpath** | string | The XPath-like DOM path (e.g., `html/body/div[0]`). Index `[0]` is omitted if the element has no same-tag siblings. |
| **attributes** | JSON string | All HTML attributes serialized as a JSON string. |
| **contents** | string | Direct text content, where child elements are replaced by **`{idXXX}`** references. Literal curly braces are escaped as `\{` or `\}`. |

### 2\. `csv2html.py` (The Reconstructor)

Rebuilds the original HTML document from the structured CSV data by resolving the `{idXXX}` references and correctly handling attribute reconstruction and unescaping.

## Usage Example

### Step 1: Flatten DOM to CSV

Assuming you have `input.html`:

```bash
python html2csv.py sample_data/input.html sample_data/output.csv
```

### Step 2: Reconstruct HTML from CSV

```bash
python csv2html.py sample_data/output.csv sample_data/reconstructed.html
```
