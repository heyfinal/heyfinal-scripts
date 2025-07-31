#!/usr/bin/env python3
"""
Claude Code Auto-Initialization Script
Ensures CLAUDE.md files are read and applied on every session start

This script should be run automatically when Claude Code starts a new session
to load user preferences, workflow instructions, and system configuration.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def find_claude_configs():
    """Find all CLAUDE.md configuration files"""
    config_files = []
    
    # Standard locations to check
    locations = [
        Path.home() / ".claude" / "CLAUDE.md",
        Path("/mnt/mycloud-kali/CLAUDE.md"),
        Path("/home/kali/.claude/CLAUDE.md"),
        Path.cwd() / "CLAUDE.md"
    ]
    
    for location in locations:
        if location.exists():
            config_files.append(location)
    
    return config_files

def read_and_parse_config(config_file):
    """Read and parse CLAUDE.md configuration"""
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        config = {
            "file_path": str(config_file),
            "last_modified": datetime.fromtimestamp(config_file.stat().st_mtime).isoformat(),
            "content": content,
            "instructions": [],
            "settings": {}
        }
        
        # Parse key instructions and settings
        lines = content.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('#'):
                current_section = line.replace('#', '').strip()
                config["instructions"].append(f"SECTION: {current_section}")
            elif line.startswith('-') or line.startswith('*'):
                instruction = line.replace('-', '').replace('*', '').strip()
                config["instructions"].append(instruction)
            elif ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                config["settings"][key.strip()] = value.strip()
        
        return config
        
    except Exception as e:
        print(f"Error reading {config_file}: {e}")
        return None

def apply_system_configuration(configs):
    """Apply system configuration from CLAUDE.md files"""
    print("🤖 Claude Code Auto-Initialization")
    print("=" * 50)
    
    if not configs:
        print("⚠️  No CLAUDE.md configuration files found!")
        print("Consider creating ~/.claude/CLAUDE.md with your preferences")
        return False
    
    for config in configs:
        print(f"\n📖 Loading configuration from: {config['file_path']}")
        print(f"   Last modified: {config['last_modified']}")
        
        # Display key instructions
        print(f"   Instructions loaded: {len(config['instructions'])}")
        for instruction in config['instructions'][:5]:  # Show first 5
            print(f"   • {instruction}")
        
        if len(config['instructions']) > 5:
            print(f"   • ... and {len(config['instructions']) - 5} more")
        
        # Display key settings
        if config['settings']:
            print(f"   Settings: {list(config['settings'].keys())}")
    
    print(f"\n✅ Loaded {len(configs)} configuration file(s)")
    
    # Save loaded config for reference
    session_config = {
        "session_start": datetime.now().isoformat(),
        "configs_loaded": [c['file_path'] for c in configs],
        "total_instructions": sum(len(c['instructions']) for c in configs),
        "all_configs": configs
    }
    
    config_cache = Path.home() / ".claude" / "session-config.json"
    config_cache.parent.mkdir(exist_ok=True)
    
    with open(config_cache, 'w') as f:
        json.dump(session_config, f, indent=2)
    
    print(f"📝 Session configuration cached to: {config_cache}")
    return True

def create_initialization_reminder():
    """Create a visible reminder of loaded configuration"""
    configs = find_claude_configs()
    
    if configs:
        primary_config = configs[0]  # Use first config as primary
        config_data = read_and_parse_config(primary_config)
        
        if config_data:
            print("\n" + "="*60)
            print("🔧 ACTIVE CLAUDE CODE CONFIGURATION")
            print("="*60)
            
            # Show critical settings
            critical_settings = {
                'Root': config_data['settings'].get('Root', 'Not set'),
                'GitHub': config_data['settings'].get('GitHub', 'Not set'), 
                'Sudo password': config_data['settings'].get('Sudo password', 'Not set')
            }
            
            for key, value in critical_settings.items():
                print(f"{key}: {value}")
            
            print("\n📋 Key Workflow Rules:")
            workflow_rules = [
                "Check knowledge base/research before API calls",
                "Run /compact before saving memory/research", 
                "Backup projects before builds",
                "Never use placeholder/mock/demo code",
                "Autonomous operation (minimal approval requests)"
            ]
            
            for rule in workflow_rules:
                print(f"• {rule}")
            
            print("="*60)
            print("Configuration loaded and active for this session")
            print("="*60)

def main():
    """Main initialization function"""
    # Find and load all CLAUDE.md files
    config_files = find_claude_configs()
    
    # Parse configurations
    configs = []
    for config_file in config_files:
        config = read_and_parse_config(config_file)
        if config:
            configs.append(config)
    
    # Apply configuration
    success = apply_system_configuration(configs)
    
    if success:
        create_initialization_reminder()
        return True
    else:
        print("❌ Failed to load Claude Code configuration")
        return False

if __name__ == "__main__":
    main()