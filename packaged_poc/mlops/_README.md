# Illuminated Mullet 

## 27-Feb-2023

1. Import Libraries

2. Configure Notebook

3. Declare MetastoreTable Class

4. Setup catalog -> return CatalogHelper instance.

5. Setup schema within catalog

6. Instantiate MetastoreTable instance






## Archive material `pre 27-Feb-2023`

Data science use case

Dataset - California housing dataset

Tasks 
1. Create a catalog & database

2. Load data to database (in two separate tables)
    - Original dataset
        - Pull out uniqueness 
    - House data:
        - houseId (need to create)
        - latitudeOfHouse - a measure of how far north a house is
        - longitudeOfHouse - a measure of how far west a house is 
        - oceanProximityCategory - ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'] Does this change within a block?
    - Block data:
        - blockId (need to create)
        - noRoomsWithinBlock
        - medianHousingUnitAgeOfBlock
        - noBedroomsWithinBlock
        - populationWithinBlock
        - householdsWithinBlock
        - medianIncomeOfBlock
        - medianHouseValueOfBlock


3. Create Feature table
3. Train AutoML
4. Deploy model for serving
    - Real-time
    - Streaming
    - Batch
5. 

- Setup json stream, synthetic data creator based on existing data table.
- 

