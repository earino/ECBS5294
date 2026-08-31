#!/usr/bin/env python3
"""
Decrypt Solution Notebooks

This script decrypts password-protected solution ZIPs.
For instructor/TA use only.

Usage:
    python scripts/decrypt_solution.py <encrypted.zip> --password <pwd>
    python scripts/decrypt_solution.py <encrypted.zip>  # Will prompt for password

Examples:
    python scripts/decrypt_solution.py solutions/solutions-day1-blockA.zip --password "potato123"
    python scripts/decrypt_solution.py solutions/solutions-day1-blockA.zip  # Interactive
"""

import argparse
import os
import sys
import zipfile
import getpass
from pathlib import Path


def decrypt_zip(zip_path, password, output_dir=None):
    """Decrypt and extract a password-protected ZIP file."""
    try:
        # Default output directory
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(zip_path), 'decrypted')

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Extract with password
        with zipfile.ZipFile(zip_path, 'r') as zf:
            try:
                # Set password (must be bytes)
                zf.setpassword(password.encode())

                # Extract all files
                zf.extractall(output_dir)

                # List extracted files
                extracted_files = zf.namelist()
                return True, extracted_files, output_dir

            except RuntimeError as e:
                if 'Bad password' in str(e) or 'password' in str(e).lower():
                    return False, [], None
                else:
                    raise

    except Exception as e:
        print(f"❌ Error: {e}")
        return False, [], None


def main():
    parser = argparse.ArgumentParser(
        description='Decrypt password-protected solution ZIPs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('zip_file', help='Encrypted ZIP file to decrypt')
    parser.add_argument('--password', '-p', help='Password (will prompt if not provided)')
    parser.add_argument('--output', '-o', help='Output directory (default: solutions/decrypted/)')

    args = parser.parse_args()

    # Check if ZIP file exists
    if not os.path.exists(args.zip_file):
        print(f"❌ Error: File not found: {args.zip_file}")
        sys.exit(1)

    # Get password
    if args.password:
        password = args.password
    else:
        password = getpass.getpass("🔑 Enter password: ")

    # Decrypt
    print(f"🔓 Decrypting: {args.zip_file}")

    success, files, output_dir = decrypt_zip(args.zip_file, password, args.output)

    if success:
        print(f"✅ Success! Extracted {len(files)} file(s) to:")
        print(f"   {output_dir}")
        print(f"\nExtracted files:")
        for f in files:
            file_path = os.path.join(output_dir, f)
            file_size = os.path.getsize(file_path)
            print(f"   - {f} ({file_size:,} bytes)")

        print(f"\n⚠️  Remember: These are unencrypted files!")
        print(f"   DO NOT commit them to git!")

    else:
        print("❌ Failed to decrypt. Wrong password?")
        sys.exit(1)


if __name__ == '__main__':
    main()
