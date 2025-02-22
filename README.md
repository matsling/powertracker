# Powertracker
Campaign financing tracking from local to national. Live example at https://sanangelopolitics.com

![alt text](https://raw.githubusercontent.com/matsling/powertracker/refs/heads/main/example.png)

## Description
Powertracker started as a way for me to digitize my local city campaign finance reports which were still hand written documents scanned as PDFs. However, the database design has been setup so data from any elections at any level from municipal up to national can be added in. And connections created between the people giving money, recieving money, and their relationships. It allows one to move through connections between donors to map power structures. Follow the money.

The database is broken down so everything should only exist in one place. Relying on linking people, campaigns, and money together. And if you were to view one page, you can click on any of the linking data to follow the money and relationships through. Almost any piece of data can be a clue into power relations, from property ownership to industries.

## Types of data tracked
- Addresses: Addresses of candidates, contributors, etc. from source documents.
- Assumed Names: Assumed names are titles of businesses and partnerships that may not be incorporated.
- Campaigns: Political campaigns for candidates or ballot initiatives.
- Documents: Source documents from which data is pulled.
- Elections: List of elections for different jurisdiction.
- Email Addresses: Emails from source documents.
- Entities: Any individual, corporation, government, or other organization.
- External IDs: IDs that have been assigned by an external agency like TEC or the IRS.
- Former Office Holders: A list of former office holders and the office they held.
- Industries: Specific categories of industry.
- Industry Sectors: Broad categories of industries.
- Offices: Government offices like mayors and council members.
- Phone Numbers: Phone numbers from source documents.
- Relationships: Relationships between people & organizations like spouses or employers.
- Reported Subtotals: Reported monetary and expenditure subtotals broken out by type from source documents.
- Reported Totals: Reported monetary and expenditure totals from source documents.
- Transactions: Money given to and spent by a campaign.
- Websites: Websites of candidates, campaigns, and organizations.

## Roadmap
- Moving the UI to a modern framework such as REACT
- Automating data entry from Texas Ethics Commission
- Automating data entry from Federal Elections Commission

## Installation
The production site is running in a collection of 3 podman/docker containers. See the podman.txt file for more information.

## License
GPL-3.0 license
