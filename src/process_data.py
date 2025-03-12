"""Script to process raw precinct data into clean format."""
from pathlib import Path
from data_processor import PrecinctDataProcessor

def main():
    # Ensure processed data directory exists
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize and run processor
    processor = PrecinctDataProcessor()
    try:
        data = processor.process_all_states()
        print(f"Successfully processed {len(data)} precincts")
        print("\nSample of processed data:")
        print(data.head())
        print("\nData shape:", data.shape)
        print("\nColumns:", data.columns.tolist())
    except Exception as e:
        print(f"Error processing data: {str(e)}")

if __name__ == "__main__":
    main() 