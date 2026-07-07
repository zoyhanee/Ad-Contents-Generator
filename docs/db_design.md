# DB Design Draft

This document describes the initial database structure for AdMaker AI.
The current frontend stores most workflow data in `st.session_state`.
The goal of this design is to persist that workflow in database tables.

## Service Data Flow

```text
User
-> Product
-> Ad Project
-> Ad Strategy
-> Ad Drafts
-> Final Result
```

## 1. users

Stores account information.

| Column | Type | Description |
|---|---|---|
| id | integer | Internal user ID |
| email | string | Login email |
| password_hash | string | Hashed password |
| store_name | string | Store or business name |
| created_at | datetime | Created time |
| updated_at | datetime | Last updated time |

## 2. products

Stores product information entered by the user.

| Column | Type | Description |
|---|---|---|
| id | integer | Product ID |
| user_id | integer | Owner user ID |
| name | string | Product name |
| price | integer | Product price |
| description | text | Product description |
| industry | string | Business category |
| image_path | string | Uploaded image path |
| created_at | datetime | Created time |
| updated_at | datetime | Last updated time |

## 3. ad_projects

Stores one advertisement creation workflow.

| Column | Type | Description |
|---|---|---|
| id | integer | Project ID |
| user_id | integer | Owner user ID |
| product_id | integer | Product ID |
| status | string | Project status |
| created_at | datetime | Created time |
| updated_at | datetime | Last updated time |

Example status values:

```text
draft
strategy_selected
generating
completed
```

## 4. ad_strategies

Stores strategy options and AI recommendation results.

| Column | Type | Description |
|---|---|---|
| id | integer | Strategy ID |
| project_id | integer | Ad project ID |
| strategy_mode | string | faster or manual |
| reuse_tone | boolean | Whether to reuse previous tone |
| selected_platforms | json | Selected platforms |
| poster_size | string | Poster size for offline poster |
| selected_goal | string | Selected ad goal |
| selected_style | string | Selected visual style |
| strategy_title | string | AI recommendation title |
| strategy_description | text | AI recommendation description |
| slogans | json | Recommended slogan candidates |
| selected_slogan | string | User-selected slogan |
| created_at | datetime | Created time |
| updated_at | datetime | Last updated time |

## 5. ad_drafts

Stores generated ad draft variants.

| Column | Type | Description |
|---|---|---|
| id | integer | Draft ID |
| project_id | integer | Ad project ID |
| draft_label | string | A, B, C |
| title | string | Draft title |
| version | integer | Draft version |
| image_path | string | Generated image path |
| feedback | text | User feedback for regeneration |
| is_selected | boolean | Whether this draft is selected |
| created_at | datetime | Created time |
| updated_at | datetime | Last updated time |

## 6. final_results

Stores the final selected advertisement result.

| Column | Type | Description |
|---|---|---|
| id | integer | Final result ID |
| project_id | integer | Ad project ID |
| selected_draft_id | integer | Selected draft ID |
| image_path | string | Final image path |
| saved_at | datetime | Saved time |

## Relationships

```text
users 1 - N products
users 1 - N ad_projects
products 1 - N ad_projects
ad_projects 1 - 1 ad_strategies
ad_projects 1 - N ad_drafts
ad_projects 1 - 1 final_results
ad_drafts 1 - 0..1 final_results
```
