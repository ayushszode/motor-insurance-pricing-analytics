# Data Dictionary

## Frequency table

| Field | Meaning |
|---|---|
| IDpol | Policy identifier |
| ClaimNb | Number of claims attached to the policy record |
| Exposure | Policy exposure in policy-year units |
| Area | Population-density category A–F |
| VehPower | Vehicle power category |
| VehAge | Vehicle age |
| DrivAge | Driver age |
| BonusMalus | Bonus-Malus rating value |
| VehBrand | Vehicle brand category |
| VehGas | Fuel type |
| Density | Population density |
| Region | French region category |

## Severity table

| Field | Meaning |
|---|---|
| IDpol | Policy identifier used to join to the frequency table |
| ClaimAmount | Estimated monetary cost of an individual claim |

## Derived fields

| Field | Formula / definition |
|---|---|
| Claim frequency | Claims / exposure |
| Claim rate per 100 | 100 × claims / exposure |
| Average severity | Claim amount / severity claim rows |
| Indicated pure premium | Claim frequency × average severity |
| Relativity | Segment pure premium / portfolio pure premium |
