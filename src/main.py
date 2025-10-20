import argparse
import sys
from pathlib import Path

import pandas as pd

from anon import atgk


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='ATGK Data Anonymization Tool - Works with ANY CSV dataset!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples with different types of datasets:

  # Healthcare data
  python main.py -i data/patients.csv -o output.csv -q age,zipcode,diagnosis -k 5

  # Employee data
  python main.py -i data/employees.csv -o output.csv -q age,city,salary,dept -k 8

  # Customer data  
  python main.py -i data/customers.csv -o output.csv -q age,location,income -k 10

  # Education data
  python main.py -i data/students.csv -o output.csv -q age,school,grade -k 5

  # Any CSV with custom parameters
  python main.py -i your_data.csv -o anon.csv -q col1,col2,col3 -k 5 --gorillas 50 --iterations 100

Note: Specify YOUR dataset's quasi-identifiers (columns that could identify individuals)
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to ANY input CSV file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to output anonymized CSV file'
    )
    
    parser.add_argument(
        '-q', '--quasi-identifiers',
        type=str,
        required=True,
        help='Comma-separated quasi-identifier columns from YOUR dataset (e.g., "age,city,income")'
    )
    
    parser.add_argument(
        '-k', '--k-anonymity',
        type=int,
        required=True,
        help='k-anonymity parameter (minimum group size)'
    )
    
    # Optional algorithm parameters
    parser.add_argument(
        '--gorillas',
        type=int,
        default=40,
        help='Number of gorillas in population (default: 40)'
    )
    
    parser.add_argument(
        '--iterations',
        type=int,
        default=75,
        help='Maximum number of iterations for optimization (default: 75)'
    )
    
    parser.add_argument(
        '--clusters',
        type=int,
        default=None,
        help='Number of clusters for fuzzy c-means (default: max(5, k))'
    )
    
    # Data handling options
    parser.add_argument(
        '--separator',
        type=str,
        default=',',
        help='CSV separator character (default: ",")'
    )
    
    parser.add_argument(
        '--encoding',
        type=str,
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--no-header',
        action='store_true',
        help='CSV file has no header row'
    )
    
    # Display options
    parser.add_argument(
        '--preview',
        type=int,
        default=5,
        help='Number of rows to preview before/after (default: 5, 0 to disable)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output messages'
    )
    
    return parser.parse_args()


def validate_inputs(args, df):
    """Validate input arguments and data."""
    qis = [qi.strip() for qi in args.quasi_identifiers.split(',')]
    
    if args.k_anonymity < 2:
        raise ValueError("k-anonymity must be at least 2")
    
    if args.k_anonymity > len(df):
        raise ValueError(f"k-anonymity ({args.k_anonymity}) cannot be larger than dataset size ({len(df)})")
    
    missing_columns = [qi for qi in qis if qi not in df.columns]
    if missing_columns:
        raise ValueError(f"Quasi-identifiers not found in dataset: {', '.join(missing_columns)}")
    
    if args.gorillas < 1:
        raise ValueError("Number of gorillas must be at least 1")
    
    if args.iterations < 1:
        raise ValueError("Number of iterations must be at least 1")
    
    if args.clusters is not None and args.clusters < 2:
        raise ValueError("Number of clusters must be at least 2")
    
    return qis


def print_dataset_info(df, qis, args):
    """Print information about the dataset."""
    if args.quiet:
        return
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    print(f"File: {args.input}")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Data Types: {df.dtypes.value_counts().to_dict()}")
    print(f"\nAll Columns: {', '.join(df.columns.tolist())}")
    print(f"\nQuasi-identifiers (will be anonymized): {', '.join(qis)}")
    print(f"Other columns (preserved as-is): {', '.join([c for c in df.columns if c not in qis])}")
    
    print(f"\nQuasi-identifier details:")
    for qi in qis:
        dtype = df[qi].dtype
        unique = df[qi].nunique()
        qi_type = "numeric" if pd.api.types.is_numeric_dtype(df[qi]) else "categorical"
        print(f"  • {qi}: {qi_type} ({unique} unique values)")
    
    print("="*70)


def print_preview(df, title, n_rows):
    """Print a preview of the dataframe."""
    if n_rows <= 0:
        return
    
    print(f"\n{title}")
    print("-" * 70)
    print(df.head(n_rows).to_string(index=False))
    print()


def main():
    """Main entry point for the CLI tool."""
    try:
        args = parse_arguments()
        
        if not args.quiet:
            print("\n" + "="*70)
            print("ATGK ANONYMIZATION TOOL")
            print("="*70)
        
        if not args.quiet:
            print(f"\nLoading data from: {args.input}")
        
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            return 1
        
        header = None if args.no_header else 'infer'
        df = pd.read_csv(args.input, sep=args.separator, encoding=args.encoding, header=header)
        
        if not args.quiet:
            print(f"✓ Loaded {len(df)} records")
        
        qis = validate_inputs(args, df)
        print_dataset_info(df, qis, args)
        
        if args.preview > 0 and not args.quiet:
            print_preview(df, "ORIGINAL DATA (first rows)", args.preview)
        
        anonymized_df = atgk(
            df=df,
            qis=qis,
            k=args.k_anonymity,
            n_gorillas=args.gorillas,
            max_iter=args.iterations,
            n_clusters=args.clusters
        )
        
        if args.preview > 0 and not args.quiet:
            print_preview(anonymized_df, "ANONYMIZED DATA (first rows)", args.preview)
        
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        anonymized_df.to_csv(args.output, sep=args.separator, encoding=args.encoding, index=False)
        
        if not args.quiet:
            print(f"\n{'='*70}")
            print(f"✓ Anonymized data saved to: {args.output}")
            print(f"{'='*70}\n")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
