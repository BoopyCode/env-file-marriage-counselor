#!/usr/bin/env python3
"""
.env Marriage Counselor - Because your environments need couples therapy.
Helps reconcile differences between dev, staging, and production .env files.
"""

import sys
from pathlib import Path
from collections import defaultdict

def read_env_file(filepath):
    """Reads .env file, returns dict of key=value pairs."""
    env = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"⚠️  Therapist note: {filepath} is missing. Commitment issues?")
    return env

def compare_envs(envs):
    """Compares multiple .env files, finds inconsistencies."""
    all_keys = set()
    for env in envs.values():
        all_keys.update(env.keys())
    
    print("\n🔍 Relationship Status Report:\n")
    print("=" * 50)
    
    for key in sorted(all_keys):
        values = {name: envs[name].get(key, "[MISSING]") for name in envs}
        unique_values = set(values.values())
        
        if len(unique_values) > 1:
            print(f"🚨 CONFLICT: '{key}' has commitment issues:")
            for name, value in values.items():
                print(f"  {name}: {value}")
            print()
        else:
            print(f"✅ Harmony: '{key}' = {list(values.values())[0]}")
    
    print("=" * 50)
    
    # Find keys unique to each environment
    for name, env in envs.items():
        others = [e for n, e in envs.items() if n != name]
        other_keys = set()
        for other in others:
            other_keys.update(other.keys())
        unique = set(env.keys()) - other_keys
        if unique:
            print(f"\n🎭 {name} is keeping secrets: {', '.join(sorted(unique))}")

def main():
    """Main therapy session."""
    if len(sys.argv) < 2:
        print("Usage: python env_marriage_counselor.py <env1> <env2> [env3...]")
        print("Example: python env_marriage_counselor.py .env.dev .env.staging .env.prod")
        sys.exit(1)
    
    envs = {}
    for filepath in sys.argv[1:]:
        name = Path(filepath).name
        envs[name] = read_env_file(filepath)
    
    if not envs:
        print("💔 No .env files found. Relationship terminated.")
        return
    
    compare_envs(envs)
    print("\n💖 Remember: Communication is key! Sync those values!")

if __name__ == "__main__":
    main()
