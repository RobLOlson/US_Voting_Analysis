"""Process raw precinct data into clean format for analysis."""
import pandas as pd
from pathlib import Path
from typing import Optional


class PrecinctDataProcessor:
    def __init__(self, raw_data_dir: str = "data/raw/2020_precinct",
                 processed_data_dir: str = "data/processed"):
        """Initialize processor with data directories."""
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.dtypes = {
            'precinct': str,
            'office': str,
            'party_simplified': str,
            'mode': str,
            'votes': float,  # Changed to float to handle all cases
            'candidate': str,
            'state_po': str,
            'year': int,
            'stage': str
        }

    def process_state_data(self, state_po: str) -> Optional[pd.DataFrame]:
        """
        Process a single state's data into clean format.
        
        Returns DataFrame with columns:
        - precinct_id: str (state_po + precinct)
        - precinct_name: str
        - election_year: int
        - total_votes: int
        - candidate: str
        - candidate_party: str
        - support_percent: float
        - state: str
        """
        try:
            # Read raw data
            file_path = self.raw_data_dir / f"2020-{state_po.lower()}-precinct-general.csv"
            df = pd.read_csv(file_path, dtype=self.dtypes, usecols=self.dtypes.keys())
            
            # Filter to presidential race and total votes
            pres_df = df[
                (df['office'] == 'PRESIDENT') & 
                (df['mode'] == 'TOTAL') &
                (df['stage'] == 'GEN')
            ].copy()
            
            # Calculate total votes per precinct
            total_votes = pres_df[
                (pres_df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])) &
                (pres_df['candidate'].notna())
            ].groupby('precinct')['votes'].sum().reset_index()
            
            # Calculate candidate support
            candidate_votes = pres_df[
                (pres_df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])) &
                (pres_df['candidate'].notna())
            ].copy()
            
            # Join with total votes
            candidate_votes = pd.merge(
                candidate_votes,
                total_votes.rename(columns={'votes': 'total_votes'}),
                on='precinct'
            )
            
            # Calculate support percentage
            candidate_votes['support_percent'] = (candidate_votes['votes'] / candidate_votes['total_votes']) * 100
            
            # Add identifiers
            candidate_votes['precinct_id'] = state_po + "_" + candidate_votes['precinct']
            candidate_votes['precinct_name'] = candidate_votes['precinct']
            candidate_votes['election_year'] = 2020
            candidate_votes['state'] = state_po
            
            # Select and rename columns
            result = candidate_votes[[
                'precinct_id',
                'precinct_name',
                'election_year',
                'total_votes',
                'candidate',
                'party_simplified',
                'support_percent',
                'state'
            ]].rename(columns={'party_simplified': 'candidate_party'})
            
            # Filter out unrealistic values
            result = result[
                (result['support_percent'] <= 100) &
                (result['support_percent'] > 0)
            ]
            
            # Convert total_votes to int after all calculations
            result['total_votes'] = result['total_votes'].astype(int)
            
            return result
            
        except Exception as e:
            print(f"Error processing {state_po}: {str(e)}")
            return None

    def process_all_states(self) -> pd.DataFrame:
        """Process all state data and combine into single DataFrame."""
        # Get list of all state files
        state_files = list(self.raw_data_dir.glob("2020-*-precinct-general.csv"))
        state_pos = [f.name.split('-')[1].upper() for f in state_files]
        
        # Process each state
        all_data = []
        for state_po in state_pos:
            state_data = self.process_state_data(state_po)
            if state_data is not None:
                all_data.append(state_data)
        
        # Combine all states
        if not all_data:
            raise ValueError("No state data was successfully processed")
            
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to processed data directory
        output_file = self.processed_data_dir / "precinct_turnout_support_2020.parquet"
        combined_data.to_parquet(output_file, index=False)
        
        # Also save a CSV for easier inspection
        csv_file = self.processed_data_dir / "precinct_turnout_support_2020.csv"
        combined_data.to_csv(csv_file, index=False)
        
        return combined_data 