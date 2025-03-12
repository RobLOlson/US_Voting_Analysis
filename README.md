# US Voting Analysis

A data analysis project examining precinct-level voting patterns in US elections, with a focus on the relationship between voter turnout and candidate support.

## Project Goals

1. Analyze precinct-level relationships between:
   - Voter turnout percentages
   - Presidential candidate support
   - Geographic and demographic factors
2. Create visualizations to identify patterns and outliers
3. Compare patterns across different election years (planned)

## Data Source

This project uses precinct-level election returns from the MIT Election Data and Science Lab (MEDSL). The current analysis focuses on 2020 data, with plans to incorporate data from previous elections.

## Project Structure

```
.
├── data/               # Data directory (not in git)
│   ├── raw/           # Original data files
│   └── processed/     # Cleaned and transformed data
├── notebooks/         # Jupyter notebooks for analysis
├── src/              # Source code
│   └── precinct_analysis.py  # Main analysis module
└── tests/            # Test files
```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the precinct-level data from [MEDSL Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NT66Z3)
4. Place the downloaded CSV files in `data/raw/2020_precinct/`
5. Run the Jupyter notebooks in `notebooks/` to see the analysis

## Development Notes

This project serves a dual purpose:
1. Analyzing US voting patterns at the precinct level
2. Experimenting with [Cursor](https://cursor.sh/) as a development environment and AI assistant

The development process is being actively guided by Cursor's AI capabilities, making this project both a study of voting patterns and an exploration of AI-assisted development workflows.

## Contributing

Interested in contributing? Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- MIT Election Data and Science Lab for the precinct-level data
- Cursor.sh team for the AI-assisted development environment 