"""Configuration loader for UpShiftRx - handles public/private data paths."""

import yaml
import os
from pathlib import Path

def load_config(config_path="config/config.yaml"):
    """Load configuration with fallbacks for missing private paths."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        # Default config if file doesn't exist
        config = {
            'data': {'examples_dir': 'results/examples/'},
            'pubmed': {'email': 'your-email@domain.com', 'max_results_default': 50, 'rate_limit_sleep': 2.0},
            'processing': {'use_sample_data': True, 'output_dir': 'results/'}
        }
    
    # Check if private repo paths exist
    private_repo = config.get('data', {}).get('private_repo_path')
    if private_repo and not Path(private_repo).exists():
        print("⚠️  Private repository not found. Using public sample data only.")
        config['processing']['use_sample_data'] = True
    
    return config

def get_data_path(config, data_type='examples'):
    """Get appropriate data path based on availability."""
    data_config = config.get('data', {})
    
    if config.get('processing', {}).get('use_sample_data', True):
        return data_config.get('examples_dir', 'results/examples/')
    
    # Map data types to private paths
    path_map = {
        'examples': data_config.get('examples_dir', 'results/examples/'),
        'full_pubmed': data_config.get('full_pubmed_dir', 'results/examples/'),
        'drugbank': data_config.get('drugbank_dir', 'results/examples/'),
        'models': data_config.get('models_dir', 'results/examples/')
    }
    
    return path_map.get(data_type, data_config.get('examples_dir', 'results/examples/'))