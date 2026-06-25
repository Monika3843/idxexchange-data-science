# Week 1 Notes — IDX Exchange Data Science Internship

## Dataset Access
I connected to the FTP server using FileZilla with the provided credentials and successfully downloaded 6 months of CRMLSSold files from /raw/California to my local data folder. Dataset access confirmed.

---

## Key Column Definitions (from Trestle Metadata)

These are the columns I think will matter most for building the price prediction model:

**Identifiers**
- `ListingKey` — unique ID for each listing record, like a primary key
- `ListingId` — the human-readable version of the listing ID

**Property Details**
- `PropertyType` — type of property (I'll be filtering to "Residential" only)
- `PropertySubType` — more specific type (filtering to "SingleFamilyResidence")
- `LivingArea` — interior square footage of the home, probably one of the biggest price drivers
- `BedroomsTotal` — total number of bedrooms
- `BathroomsTotalInteger` — total bathrooms counted as whole numbers (e.g., 2 full + 1 half = 3)
- `BathroomsFull` — rooms with all 4 elements: sink, toilet, tub, and shower
- `BathroomsHalf` — rooms with just sink + toilet
- `LotSizeSquareFeet` — total square footage of the land/lot
- `LotSizeAcres` — same as above but in acres
- `YearBuilt` — year the home was built, useful for calculating property age
- `Stories` — number of floors in the home
- `GarageSpaces` — number of garage spots included
- `PoolPrivateYN` — whether the home has a private pool (Y/N)
- `FireplacesTotal` — number of fireplaces

**Pricing (most important)**
- `ListPrice` — what the seller originally listed the home for
- `ClosePrice` — the actual final sale price → **this is my target variable**
- `OriginalListPrice` — the very first list price before any reductions

**Location**
- `Latitude` / `Longitude` — GPS coordinates, useful for mapping and geographic features
- `City` — city the property is in
- `PostalCode` — zip code
- `CountyOrParish` — county name
- `HighSchoolDistrict` — school district, which Week 6 says to use as a feature

**Dates & Market Timing**
- `ListingContractDate` — when the seller signed the listing agreement
- `PurchaseContractDate` — when an offer was accepted
- `CloseDate` — when the sale officially closed
- `DaysOnMarket` — how many days the listing was active before going under contract
- `CumulativeDaysOnMarket` — total days on market across all listing periods (accounts for relisted properties)

**Status**
- `StandardStatus` — current status of the listing (Active, Pending, Closed, Expired, etc.)
- I'll need to filter to Closed only when training the model since only those have a ClosePrice

**Agent/Brokerage Info**
- `ListAgentFullName` / `ListOfficeName` — who listed the property (seller's side)
- `BuyerAgentFullName` / `BuyerOfficeName` — who represented the buyer

---

## Notes to Self
- Always filter `PropertyType = Residential` AND `PropertySubType = SingleFamilyResidence` before doing anything
- `ClosePrice` is null for non-sold listings, so make sure I'm only using Closed records for training
- `LivingArea`, `BedroomsTotal`, `LotSizeSquareFeet`, `YearBuilt`, `Latitude`, `Longitude` are probably going to be my core features to start with
