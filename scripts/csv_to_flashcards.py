#!/usr/bin/env python3
"""
CSV to FlashCards Import Script

This script reads a CSV file with language learning data and creates flashcards
with AI-generated images using the FlashCards API.

CSV Format Expected:
German Word,English Translation,Description for Image

Usage:
    python csv_to_flashcards.py <csv_file> [options]

Example:
    python csv_to_flashcards.py german_words.csv --group-name "German Vocabulary" --base-url http://5.161.100.20:8009
"""

import csv
import requests
import argparse
import sys
import os
import time
from typing import Optional, Dict, Any
import json

# Try to import optional AI image generation libraries
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False


class FlashCardUploader:
    def __init__(self, base_url: str = "http://5.161.100.20:8009", openai_api_key: str = None, 
                 replicate_api_token: str = None):
        """
        Initialize the FlashCard uploader.
        
        Args:
            base_url: Base URL of the FlashCards application
            openai_api_key: OpenAI API key for DALL-E image generation
            replicate_api_token: Replicate API token for Stable Diffusion
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api"
        self.session = requests.Session()
        
        # Initialize AI services
        self.openai_client = None
        if openai_api_key and OPENAI_AVAILABLE:
            self.openai_client = OpenAI(api_key=openai_api_key)
            
        self.replicate_token = replicate_api_token
        if replicate_api_token and REPLICATE_AVAILABLE:
            os.environ["REPLICATE_API_TOKEN"] = replicate_api_token
    
    def get_or_create_group(self, group_name: str) -> Optional[int]:
        """
        Get existing group by name or create a new one.
        
        Args:
            group_name: Name of the card group
            
        Returns:
            Group ID if successful, None otherwise
        """
        try:
            # First, try to get existing groups
            response = self.session.get(f"{self.api_base}/groups/")
            if response.status_code == 200:
                groups = response.json().get('results', [])
                for group in groups:
                    if group['name'].lower() == group_name.lower():
                        print(f"✓ Found existing group: {group['name']} (ID: {group['id']})")
                        return group['id']
            
            # If group doesn't exist, create it
            group_data = {
                "name": group_name,
                "image": None
            }
            
            response = self.session.post(f"{self.api_base}/groups/", json=group_data)
            if response.status_code == 201:
                group = response.json()
                print(f"✓ Created new group: {group['name']} (ID: {group['id']})")
                return group['id']
            else:
                print(f"✗ Failed to create group: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Error managing group: {e}")
            return None
    
    def generate_image_openai(self, description: str, word: str) -> Optional[str]:
        """
        Generate image using OpenAI DALL-E.
        
        Args:
            description: Description for the image
            word: The word being illustrated
            
        Returns:
            Image URL if successful, None otherwise
        """
        if not self.openai_client:
            return None
            
        try:
            prompt = f"A clear, simple illustration of {description}. Educational style, clean background, suitable for language learning flashcard."
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
            
        except Exception as e:
            print(f"✗ OpenAI image generation failed for '{word}': {e}")
            return None
    
    def generate_image_replicate(self, description: str, word: str) -> Optional[str]:
        """
        Generate image using Replicate Stable Diffusion.
        
        Args:
            description: Description for the image
            word: The word being illustrated
            
        Returns:
            Image URL if successful, None otherwise
        """
        if not REPLICATE_AVAILABLE or not self.replicate_token:
            return None
            
        try:
            prompt = f"A clear, simple illustration of {description}, educational style, clean background, high quality"
            
            output = replicate.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            )
            
            if output and len(output) > 0:
                return output[0]
            return None
            
        except Exception as e:
            print(f"✗ Replicate image generation failed for '{word}': {e}")
            return None
    
    def download_image(self, image_url: str) -> Optional[bytes]:
        """
        Download image from URL.
        
        Args:
            image_url: URL of the image to download
            
        Returns:
            Image bytes if successful, None otherwise
        """
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return response.content
            return None
        except Exception as e:
            print(f"✗ Failed to download image: {e}")
            return None
    
    def create_card(self, name: str, description: str, group_id: int, 
                   image_description: str = None, generate_image: bool = True) -> bool:
        """
        Create a flashcard.
        
        Args:
            name: Card name (e.g., German word)
            description: Card description (e.g., English translation)
            group_id: ID of the card group
            image_description: Description for image generation
            generate_image: Whether to generate an image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            card_data = {
                "name": name,
                "group": group_id,
                "description": description,
                "status": "published"
            }
            
            # Try to generate image if requested and description provided
            image_url = None
            if generate_image and image_description:
                print(f"  → Generating image for '{name}'...")
                
                # Try OpenAI first, then Replicate
                if self.openai_client:
                    image_url = self.generate_image_openai(image_description, name)
                elif REPLICATE_AVAILABLE and self.replicate_token:
                    image_url = self.generate_image_replicate(image_description, name)
                
                if image_url:
                    print(f"    ✓ Image generated: {image_url[:50]}...")
                else:
                    print(f"    ⚠ No image generated (continuing without image)")
            
            # If we have an image URL, download it and prepare for upload
            files = {}
            if image_url:
                image_data = self.download_image(image_url)
                if image_data:
                    files['image'] = ('image.jpg', image_data, 'image/jpeg')
                    print(f"    ✓ Image downloaded ({len(image_data)} bytes)")
            
            # Create the card
            if files:
                # Use multipart form data when uploading image
                response = self.session.post(f"{self.api_base}/cards/", data=card_data, files=files)
            else:
                # Use JSON when no image
                response = self.session.post(f"{self.api_base}/cards/", json=card_data)
            
            if response.status_code == 201:
                card = response.json()
                print(f"  ✓ Created card: {name} → {description}")
                return True
            else:
                print(f"  ✗ Failed to create card '{name}': {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error creating card '{name}': {e}")
            return False
    
    def process_csv(self, csv_file: str, group_name: str, generate_images: bool = True, 
                   delay: float = 1.0) -> Dict[str, int]:
        """
        Process CSV file and create flashcards.
        
        Args:
            csv_file: Path to the CSV file
            group_name: Name of the card group
            generate_images: Whether to generate images for cards
            delay: Delay between API calls (seconds)
            
        Returns:
            Dictionary with success and failure counts
        """
        if not os.path.exists(csv_file):
            print(f"✗ CSV file not found: {csv_file}")
            return {"success": 0, "failed": 0}
        
        # Get or create the group
        group_id = self.get_or_create_group(group_name)
        if not group_id:
            print("✗ Failed to create or find card group")
            return {"success": 0, "failed": 0}
        
        success_count = 0
        failed_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                # Try to detect the CSV format
                sample = file.read(1024)
                file.seek(0)
                
                # Create CSV reader
                csv_reader = csv.DictReader(file)
                
                # Get the field names
                fieldnames = csv_reader.fieldnames
                print(f"✓ CSV columns detected: {', '.join(fieldnames)}")
                
                # Map common column variations
                name_col = None
                desc_col = None
                image_col = None
                
                for field in fieldnames:
                    field_lower = field.lower()
                    if 'german' in field_lower or 'word' in field_lower:
                        name_col = field
                    elif 'english' in field_lower or 'translation' in field_lower:
                        desc_col = field
                    elif 'image' in field_lower or 'description' in field_lower:
                        image_col = field
                
                if not name_col or not desc_col:
                    print("✗ Could not identify name and description columns")
                    return {"success": 0, "failed": 0}
                
                print(f"✓ Using columns - Name: '{name_col}', Description: '{desc_col}', Image: '{image_col}'")
                print(f"✓ Starting to process cards...")
                
                for row_num, row in enumerate(csv_reader, 1):
                    name = row.get(name_col, '').strip()
                    description = row.get(desc_col, '').strip()
                    image_description = row.get(image_col, '').strip() if image_col else None
                    
                    if not name or not description:
                        print(f"  ⚠ Skipping row {row_num}: missing name or description")
                        failed_count += 1
                        continue
                    
                    print(f"Processing {row_num}: {name}")
                    
                    if self.create_card(name, description, group_id, image_description, generate_images):
                        success_count += 1
                    else:
                        failed_count += 1
                    
                    # Add delay to avoid overwhelming the API
                    if delay > 0:
                        time.sleep(delay)
                        
        except Exception as e:
            print(f"✗ Error processing CSV: {e}")
            
        return {"success": success_count, "failed": failed_count}


def main():
    parser = argparse.ArgumentParser(
        description="Import flashcards from CSV file to FlashCards application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python csv_to_flashcards.py german_words.csv

  # With custom group name and base URL
  python csv_to_flashcards.py words.csv --group-name "Spanish Vocabulary" --base-url http://flashcards.example.com

  # With AI image generation (OpenAI)
  python csv_to_flashcards.py words.csv --openai-key YOUR_OPENAI_API_KEY

  # With AI image generation (Replicate)
  python csv_to_flashcards.py words.csv --replicate-token YOUR_REPLICATE_TOKEN

  # Without image generation
  python csv_to_flashcards.py words.csv --no-images

CSV Format:
  The CSV should have columns for the word/term, translation/description, and optionally image description.
  Common column names are automatically detected (German Word, English Translation, Description for Image).
        """
    )
    
    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('--group-name', default=None, 
                       help='Name of the card group (default: derived from filename)')
    parser.add_argument('--base-url', default='http://5.161.100.20:8009',
                       help='Base URL of the FlashCards application (default: http://5.161.100.20:8009)')
    parser.add_argument('--openai-key', help='OpenAI API key for DALL-E image generation')
    parser.add_argument('--replicate-token', help='Replicate API token for Stable Diffusion')
    parser.add_argument('--no-images', action='store_true',
                       help='Skip image generation')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between API calls in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    # Validate CSV file
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file '{args.csv_file}' not found")
        sys.exit(1)
    
    # Determine group name
    group_name = args.group_name
    if not group_name:
        group_name = os.path.splitext(os.path.basename(args.csv_file))[0].replace('_', ' ').title()
    
    # Check for AI service availability
    generate_images = not args.no_images
    if generate_images:
        if args.openai_key and not OPENAI_AVAILABLE:
            print("Warning: OpenAI API key provided but openai library not installed")
            print("Install with: pip install openai")
        elif args.replicate_token and not REPLICATE_AVAILABLE:
            print("Warning: Replicate token provided but replicate library not installed")
            print("Install with: pip install replicate")
        elif not args.openai_key and not args.replicate_token:
            print("Info: No AI service configured. Cards will be created without images.")
            print("To enable image generation:")
            print("  - For OpenAI DALL-E: --openai-key YOUR_KEY")
            print("  - For Replicate: --replicate-token YOUR_TOKEN")
            generate_images = False
    
    # Initialize uploader
    uploader = FlashCardUploader(
        base_url=args.base_url,
        openai_api_key=args.openai_key,
        replicate_api_token=args.replicate_token
    )
    
    print(f"🚀 Starting FlashCard import")
    print(f"   CSV file: {args.csv_file}")
    print(f"   Group name: {group_name}")
    print(f"   Base URL: {args.base_url}")
    print(f"   Generate images: {generate_images}")
    print(f"   Delay: {args.delay}s")
    print("-" * 50)
    
    # Process the CSV
    results = uploader.process_csv(args.csv_file, group_name, generate_images, args.delay)
    
    print("-" * 50)
    print(f"📊 Import completed!")
    print(f"   ✓ Success: {results['success']} cards")
    print(f"   ✗ Failed: {results['failed']} cards")
    
    if results['success'] > 0:
        print(f"\n🎉 Cards are now available at: {args.base_url}")


if __name__ == "__main__":
    main()