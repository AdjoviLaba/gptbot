import os
import logging
from flask import current_app
import openai
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_image(image_path):
    """
    Process an image to identify the product in it using OpenAI's vision capabilities.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Identified product name or None if identification failed.
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
            
        # Set OpenAI API key
        openai.api_key = current_app.config['OPENAI_API_KEY']
        
        # If no API key is provided, use a simple fallback
        if not openai.api_key:
            logger.warning("No OpenAI API key provided. Using fallback method.")
            return extract_filename_as_product(image_path)
            
        # Encode the image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",  # Ensure you have access to this model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What product is shown in this image? Provide only the product name."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=100
        )
            
        product_name = response.choices[0].message['content'].strip()
        logger.info(f"Identified product from image: {product_name}")
            
        return product_name
            
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return extract_filename_as_product(image_path)

def extract_filename_as_product(image_path):
    """
    Fallback method to extract a product name from the filename.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Product name derived from the filename.
    """
    try:
        # Extract the filename without extension
        filename = os.path.splitext(os.path.basename(image_path))[0]
        
        # Replace underscores and hyphens with spaces
        product_name = filename.replace('_', ' ').replace('-', ' ')
        
        logger.info(f"Extracted product name from filename: {product_name}")
        return product_name
        
    except Exception as e:
        logger.error(f"Error extracting product name from filename: {str(e)}")
        return "Unknown Product"