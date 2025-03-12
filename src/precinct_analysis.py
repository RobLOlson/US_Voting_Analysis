import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class PrecinctAnalyzer:
    def __init__(self, data_dir: str = "data/raw/2020_precinct"):
        """Initialize the PrecinctAnalyzer with path to data directory."""
        self.data_dir = Path(data_dir)
        self.dtypes = {
            'precinct': str,
            'office': str,
            'party_detailed': str,
            'party_simplified': str,
            'mode': str,
            'votes': int,
            'county_name': str,
            'county_fips': str,
            'jurisdiction_name': str,
            'jurisdiction_fips': str,
            'candidate': str,
            'district': str,
            'dataverse': str,
            'year': int,
            'stage': str,
            'state': str,
            'special': str,
            'writein': str,
            'state_po': str,
            'state_fips': str,
            'state_cen': str,
            'state_ic': str,
            'date': str,
            'readme_check': str,
            'magnitude': int
        }
    
    def load_state_data(self, state_po: str) -> pd.DataFrame:
        """Load precinct data for a given state postal code."""
        file_path = self.data_dir / f"2020-{state_po.lower()}-precinct-general.csv"
        # Handle Texas separately due to turnout percentages in votes column
        if state_po.lower() == 'tx':
            self.dtypes['votes'] = float
        df = pd.read_csv(file_path, dtype=self.dtypes)
        # Reset votes dtype back to int for future state loads
        self.dtypes['votes'] = int
        return df
    
    def calculate_turnout_and_support(self, state_po: str) -> pd.DataFrame:
        """
        Calculate turnout percentage and candidate support percentage for each precinct.
        Returns DataFrame with columns: precinct, turnout_percent, dem_support_percent, rep_support_percent
        """
        df = self.load_state_data(state_po)
        
        # Get presidential race data
        pres_df = df[
            (df['office'] == 'PRESIDENT') & 
            (df['mode'] == 'TOTAL') &  # Use total votes, not broken down by voting mode
            (df['stage'] == 'GEN')  # General election only
        ].copy()
        
        # Get registered voters data if available
        reg_voters = df[
            (df['candidate'] == 'REGISTERED VOTERS') & 
            (df['mode'] == 'TOTAL')
        ].copy()
        
        if len(reg_voters) == 0:
            print(f"Warning: No registered voters data found for {state_po}")
            return None
            
        # Calculate total votes and party votes by precinct
        precinct_totals = pres_df.groupby('precinct').agg({
            'votes': lambda x: x[pres_df['writein'] == 'FALSE'].sum()  # Exclude write-ins
        }).reset_index()
        
        dem_votes = pres_df[pres_df['party_simplified'] == 'DEMOCRAT'].groupby('precinct')['votes'].sum().reset_index()
        rep_votes = pres_df[pres_df['party_simplified'] == 'REPUBLICAN'].groupby('precinct')['votes'].sum().reset_index()
        
        # Merge all data
        result = precinct_totals.merge(reg_voters[['precinct', 'votes']], on='precinct', suffixes=('_total', '_registered'))
        result = result.merge(dem_votes, on='precinct', suffixes=('', '_dem'))
        result = result.merge(rep_votes, on='precinct', suffixes=('', '_rep'))
        
        # Calculate percentages
        result['turnout_percent'] = (result['votes_total'] / result['votes_registered']) * 100
        result['dem_support_percent'] = (result['votes_dem'] / result['votes_total']) * 100
        result['rep_support_percent'] = (result['votes_rep'] / result['votes_total']) * 100
        
        # Filter out unrealistic values
        result = result[
            (result['turnout_percent'] <= 100) &  # Remove turnout > 100%
            (result['turnout_percent'] > 0) &     # Remove zero turnout
            (result['votes_total'] > 0)           # Remove zero total votes
        ]
        
        return result
    
    def plot_turnout_vs_support(self, state_po: str, party: str = 'DEMOCRAT'):
        """
        Create a scatter plot of turnout vs party support percentage.
        
        Args:
            state_po: State postal code
            party: 'DEMOCRAT' or 'REPUBLICAN'
        """
        result = self.calculate_turnout_and_support(state_po)
        if result is None:
            return
            
        support_col = 'dem_support_percent' if party == 'DEMOCRAT' else 'rep_support_percent'
        
        plt.figure(figsize=(10, 8))
        sns.scatterplot(
            data=result,
            x='turnout_percent',
            y=support_col,
            alpha=0.5
        )
        
        plt.title(f'{state_po} Precinct-Level Turnout vs {party} Support')
        plt.xlabel('Turnout Percentage')
        plt.ylabel(f'{party} Support Percentage')
        plt.grid(True, alpha=0.3)
        
        return plt 