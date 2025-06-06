# main.py
import os
import boto3
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI(title="Venues API", description="API for managing venue data in DynamoDB")

# Initialize DynamoDB client
# Use CUSTOM_AWS_REGION if set, otherwise fall back to AWS_REGION (provided by Lambda runtime)
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('CUSTOM_AWS_REGION', os.getenv('AWS_REGION', 'us-west-2'))
)

# Use the table name from environment variable or default to 'venues'
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'venues')
table = dynamodb.Table(table_name)

# Define data models
class VenueCreate(BaseModel):
    venueDescription: str
    accountID: str
    accountDenomination: str
    accountDescription: str

class Venue(VenueCreate):
    venueID: str

# API Endpoints
@app.post("/venues/", response_model=Venue)
async def create_venue(venue: VenueCreate):
    """
    Create a new venue record in DynamoDB
    """
    # Generate a unique ID for the venue
    venue_id = str(uuid.uuid4())
    
    # Prepare item for DynamoDB
    item = {
        'venueID': venue_id,
        'venueDescription': venue.venueDescription,
        'accountID': venue.accountID,
        'accountDenomination': venue.accountDenomination,
        'accountDescription': venue.accountDescription
    }
    
    # Insert item into DynamoDB
    try:
        table.put_item(Item=item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create venue: {str(e)}")
    
    # Return the created venue with its generated ID
    return Venue(venueID=venue_id, **venue.dict())

@app.get("/venues/{venue_id}", response_model=Venue)
async def get_venue(venue_id: str):
    """
    Retrieve a venue by its ID
    """
    try:
        response = table.get_item(Key={'venueID': venue_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve venue: {str(e)}")
    
    # Check if item exists
    if 'Item' not in response:
        raise HTTPException(status_code=404, detail=f"Venue with ID {venue_id} not found")
    
    return response['Item']

@app.get("/venues/")
async def list_venues():
    """
    List all venues (Note: This is a simple implementation and might need pagination for large datasets)
    """
    try:
        response = table.scan()
        venues = response.get('Items', [])
        return venues
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve venues: {str(e)}")

@app.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str):
    """
    Delete a venue by its ID
    """
    try:
        # Check if venue exists
        response = table.get_item(Key={'venueID': venue_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail=f"Venue with ID {venue_id} not found")
        
        # Delete the venue
        table.delete_item(Key={'venueID': venue_id})
        return {"message": f"Venue with ID {venue_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete venue: {str(e)}")

@app.put("/venues/{venue_id}", response_model=Venue)
async def update_venue(venue_id: str, venue: VenueCreate):
    """
    Update a venue by its ID
    """
    try:
        # Check if venue exists
        response = table.get_item(Key={'venueID': venue_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail=f"Venue with ID {venue_id} not found")
        
        # Update the venue
        item = {
            'venueID': venue_id,
            'venueDescription': venue.venueDescription,
            'accountID': venue.accountID,
            'accountDenomination': venue.accountDenomination,
            'accountDescription': venue.accountDescription
        }
        
        table.put_item(Item=item)
        return Venue(venueID=venue_id, **venue.dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update venue: {str(e)}")