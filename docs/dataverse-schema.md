
# Dataverse Table Configurations (Revised)

This document provides a comprehensive schema for Dataverse tables used in the Asset Request solution, including all recommended options, system columns, field properties, security, and automation samples.


## Asset Request Table

### Table Name: mcp_AssetRequest

#### Table Creation Steps
1. Set "Request Title" as the Primary Name Column.
2. Enable auditing and field-level security for sensitive columns.
3. Add alternate key if needed (e.g., Request Title + Created On).

### Columns
1. **Request Title** (Primary Column)
   - Type: Single line of text
   - Required: Yes
   - Max Length: 100
   - Set as Primary Name Column during table creation
   - Searchable: Yes
   - Auditing: Enabled
   - Field Security: Optional

2. **Request Details**
   - Type: Multiple lines of text
   - Required: Yes
   - Format: Text
   - Max Length: 2000
   - Searchable: Yes
   - Auditing: Enabled

3. **Status**
   - Type: Choice
   - Required: Yes
   - Options:
     - Pending (Value: 1)
     - Approved (Value: 2)
     - Rejected (Value: 3)
     - Completed (Value: 4)
   - Default: Pending (Value: 1)
   - Auditing: Enabled

4. **Priority**
   - Type: Whole Number
   - Format: None
   - Required: Yes
   - Default: 3
   - Validation: Must be between 1-5 (enforced by business rule)
   - Auditing: Enabled

5. **Category**
   - Type: Choice
   - Required: Yes
   - Options:
     - Hardware (Value: 1)
     - Software (Value: 2)
     - Access (Value: 3)
     - Network (Value: 4)
     - Other (Value: 5)
   - Default: Other (Value: 5)
   - Auditing: Enabled

6. **Requestor**
   - Type: Lookup
   - Related Table: User (systemuser)
   - Required: Yes
   - Relationship: Many-to-One
   - Relationship Name: mcp_AssetRequest_Requestor
   - Field Security: Optional

7. **Created On** (System Column)
   - Type: Date and Time
   - System-managed: Automatically set when record is created
   - Read-only: Yes

8. **Created By** (System Column)
   - Type: Lookup (systemuser)
   - System-managed: Automatically set when record is created
   - Read-only: Yes

9. **Modified On** (System Column)
   - Type: Date and Time
   - System-managed: Automatically updated when record changes
   - Read-only: Yes

10. **Modified By** (System Column)
    - Type: Lookup (systemuser)
    - System-managed: Automatically updated when record changes
    - Read-only: Yes

11. **Owner** (System Column)
    - Type: Lookup (systemuser/team)
    - System-managed: Record owner
    - Read-only: No

12. **Attachments** (Optional)
    - Type: File/Attachment
    - Relationship: One-to-Many (Asset Request to Attachment)

### Advanced Properties
- Auditing: Enabled for all columns except system columns.
- Field-level security: Enable for Request Details, Requestor if needed.
- Alternate Keys: Request Title + Created On (optional).
- Calculated/Rollup Fields: None defined, but can be added for reporting.

### Sample JSON for Table Creation (Dataverse Web API)
```json
{
  "Name": "mcp_AssetRequest",
  "PrimaryNameColumn": "Request Title",
  "Columns": [
    { "Name": "Request Title", "Type": "Text", "Required": true, "MaxLength": 100 },
    { "Name": "Request Details", "Type": "TextArea", "Required": true, "MaxLength": 2000 },
    { "Name": "Status", "Type": "Choice", "Options": [ {"Label": "Pending", "Value": 1}, {"Label": "Approved", "Value": 2}, {"Label": "Rejected", "Value": 3}, {"Label": "Completed", "Value": 4} ], "Default": 1 },
    { "Name": "Priority", "Type": "Integer", "Required": true, "Default": 3 },
    { "Name": "Category", "Type": "Choice", "Options": [ {"Label": "Hardware", "Value": 1}, {"Label": "Software", "Value": 2}, {"Label": "Access", "Value": 3}, {"Label": "Network", "Value": 4}, {"Label": "Other", "Value": 5} ], "Default": 5 },
    { "Name": "Requestor", "Type": "Lookup", "Target": "systemuser", "Required": true }
  ]
}
```


## Request Comment Table

### Table Name: mcp_RequestComment

#### Table Creation Steps
1. Create the table with "Name" as the Primary Column (Single line of text).
2. Enable auditing and field-level security for sensitive columns.
3. Add alternate key if needed (e.g., Name + Created On).

### Columns
1. **Name** (Primary Column)
   - Type: Single line of text
   - Required: Yes
   - Max Length: 100
   - Description: Auto-populated with a reference to the parent Asset Request
   - Searchable: Yes
   - Auditing: Enabled

2. **Comment Text**
   - Type: Multiple lines of text
   - Required: Yes
   - Format: Text
   - Max Length: 1000
   - Auditing: Enabled

3. **Asset Request**
   - Type: Lookup
   - Related Table: mcp_AssetRequest
   - Required: Yes
   - Relationship: Many-to-One
   - Relationship Name: mcp_AssetRequest_RequestComments

4. **Commenter**
   - Type: Lookup
   - Related Table: User (systemuser)
   - Required: Yes
   - Relationship: Many-to-One
   - Relationship Name: mcp_RequestComment_Commenter

5. **Created On** (System Column)
   - Type: Date and Time
   - System-managed: Automatically set when record is created
   - Read-only: Yes

6. **Created By** (System Column)
   - Type: Lookup (systemuser)
   - System-managed: Automatically set when record is created
   - Read-only: Yes

7. **Modified On** (System Column)
   - Type: Date and Time
   - System-managed: Automatically updated when record changes
   - Read-only: Yes

8. **Modified By** (System Column)
   - Type: Lookup (systemuser)
   - System-managed: Automatically updated when record changes
   - Read-only: Yes

9. **Owner** (System Column)
   - Type: Lookup (systemuser/team)
   - System-managed: Record owner
   - Read-only: No

### Advanced Properties
- Auditing: Enabled for all columns except system columns.
- Field-level security: Enable for Comment Text, Commenter if needed.
- Alternate Keys: Name + Created On (optional).

### Sample JSON for Table Creation (Dataverse Web API)
```json
{
  "Name": "mcp_RequestComment",
  "PrimaryNameColumn": "Name",
  "Columns": [
    { "Name": "Name", "Type": "Text", "Required": true, "MaxLength": 100 },
    { "Name": "Comment Text", "Type": "TextArea", "Required": true, "MaxLength": 1000 },
    { "Name": "Asset Request", "Type": "Lookup", "Target": "mcp_AssetRequest", "Required": true },
    { "Name": "Commenter", "Type": "Lookup", "Target": "systemuser", "Required": true }
  ]
}
```


## Security Roles & Permissions

### IT Asset Manager
- Full permissions on Asset Request and Request Comment tables
- User management permissions
- Can approve/reject requests
- Can delete any request or comment

### Regular User
- Can create new Asset Requests
- Can read/update own Asset Requests (Status=Pending)
- Can create comments on own requests
- Can read comments on own requests

### Table Permissions (Dataverse Security Role Mapping)

#### Asset Request Table
- Create: All users
- Read: Owner, IT Asset Manager
- Update: Owner (Status=Pending), IT Asset Manager
- Delete: IT Asset Manager
- Field-level security: Request Details, Requestor (optional)

#### Request Comment Table
- Create: Owner of parent Asset Request, IT Asset Manager
- Read: Owner of parent Asset Request, IT Asset Manager
- Update: Author of comment, IT Asset Manager
- Delete: IT Asset Manager

### Security Role Configuration Steps
1. Create two security roles: IT Asset Manager, Regular User.
2. Assign table permissions as above.
3. Enable field-level security profiles for sensitive columns.
4. Assign users to roles as needed.

---

## Additional Notes
- Enable auditing for all business columns.
- Use calculated fields for reporting if needed.
- Attachments can be enabled for Asset Request table.
- Use Power Automate for business logic enforcement (e.g., Priority validation).

---

