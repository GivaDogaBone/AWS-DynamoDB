# main.py
import os
import uuid
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Create FastAPI app
app = FastAPI(title="Venues API")

# Get AWS region from environment variables
aws_region = os.environ.get("CUSTOM_AWS_REGION", os.environ.get("AWS_REGION", "us-west-2"))
table_name = os.environ.get("DYNAMODB_TABLE_NAME", "venues")

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table(table_name)


# Define data models
class VenueBase(BaseModel):
    venueDescription: str
    accountID: str
    accountDenomination: str
    accountDescription: str


class VenueCreate(VenueBase):
    pass


class Venue(VenueBase):
    venueID: str


# API endpoints
@app.get("/")
def read_root():
    """
    Root endpoint for health check
    """
    return {"status": "ok", "message": "Venues API is running"}


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


@app.post("/venues/", response_model=Venue)
async def create_venue(venue: VenueCreate):
    """
    Create a new venue
    """
    try:
        venue_id = str(uuid.uuid4())
        venue_item = {
            "venueID": venue_id,
            "venueDescription": venue.venueDescription,
            "accountID": venue.accountID,
            "accountDenomination": venue.accountDenomination,
            "accountDescription": venue.accountDescription
        }
        table.put_item(Item=venue_item)
        return {**venue_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create venue: {str(e)}")


@app.get("/venues/{venue_id}", response_model=Venue)
async def get_venue(venue_id: str):
    """
    Get a specific venue by ID
    """
    try:
        response = table.get_item(Key={"venueID": venue_id})
        venue = response.get('Item')
        if not venue:
            raise HTTPException(status_code=404, detail=f"Venue {venue_id} not found")
        return venue
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve venue: {str(e)}")


@app.put("/venues/{venue_id}", response_model=Venue)
async def update_venue(venue_id: str, venue: VenueBase):
    """
    Update a venue
    """
    try:
        # Check if venue exists
        response = table.get_item(Key={"venueID": venue_id})
        if not response.get('Item'):
            raise HTTPException(status_code=404, detail=f"Venue {venue_id} not found")

        # Update venue
        update_expression = "SET venueDescription = :vd, accountID = :aid, accountDenomination = :ad, accountDescription = :acd"
        expression_values = {
            ":vd": venue.venueDescription,
            ":aid": venue.accountID,
            ":ad": venue.accountDenomination,
            ":acd": venue.accountDescription
        }

        response = table.update_item(
            Key={"venueID": venue_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )

        updated_venue = response.get('Attributes')
        return updated_venue
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update venue: {str(e)}")


@app.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str):
    """
    Delete a venue
    """
    try:
        # Check if venue exists
        response = table.get_item(Key={"venueID": venue_id})
        if not response.get('Item'):
            raise HTTPException(status_code=404, detail=f"Venue {venue_id} not found")

        # Delete venue
        table.delete_item(Key={"venueID": venue_id})
        return {"message": f"Venue {venue_id} deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete venue: {str(e)}")
