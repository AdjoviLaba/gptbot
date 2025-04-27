import os
import openai
from flask import current_app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_product_review(product_info):

    try:
        # Set OpenAI API key
        openai.api_key = current_app.config['OPENAI_API_KEY']
        
        # If no API key is provided, use a simple fallback
        if not openai.api_key:
            logger.warning("No OpenAI API key provided. Using fallback method.")
            return fallback_review_generator(product_info)
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful product review expert. "
                                             "Provide a concise, balanced summary of reviews "
                                             "for the specified product based on public opinions. "
                                             "Include pros, cons, and an overall rating out of 5 stars."},
                {"role": "user", "content": f"Provide a comprehensive review summary for: {product_info}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        review = response.choices[0].message['content'].strip()
        logger.info(f"Generated review for: {product_info}")
        
        return review
        
    except Exception as e:
        logger.error(f"Error generating review: {str(e)}")
        return f"Sorry, I couldn't generate a review for '{product_info}'. Error: {str(e)}"

def fallback_review_generator(product_info):

    return (f"Based on publicly available information about '{product_info}', "
            f"this product generally receives positive reviews. "
            f"Common pros include good value for money and reliable performance. "
            f"Some cons mentioned include limited features compared to premium alternatives. "
            f"Overall rating: 3.5/5 stars. "
            f"(Note: This is a simulated review as the OpenAI API is not configured.)")